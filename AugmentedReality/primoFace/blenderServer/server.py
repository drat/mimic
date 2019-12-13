from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import argparse, asyncio, json, logging
from matplotlib import pyplot as plt
import matplotlib.animation
import os, ssl, uuid, math
from av import VideoFrame
from aiohttp import web
import pandas as pd
import numpy as np
import pprint
import dlib
import cv2
import bpy

resources = "Useful Resources:" + "\n" + "https://www.programcreek.com/python/example/89450/cv2.Rodrigues" + "\n" + "https://manualzz.com/doc/27121231/blender-index---blender-documentation"
print(resources)

# PROJECT BASE
ROOT = os.path.dirname(__file__)

# LOGGING
logger = logging.getLogger("pc")

# A SET..
pcs = set()

# font for landmark labels and other items
font = cv2.FONT_HERSHEY_SIMPLEX

#countr ued for misc items..
countr = 0

########################################################################################################################
############################################# AI Tracking Algorithms ###################################################
########################################################################################################################

# Channel One, Face Landmarks
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Channel Two, Hand/Digit Tracking
# Space for body and hand tracking
# HAND - https://github.com/google/mediapipe/blob/master/mediapipe/docs/hand_tracking_mobile_gpu.md

# Channel Three, Body Tracking
# BODY - https://github.com/MVIG-SJTU/AlphaPose

########################################################################################################################
############################################### Mimic Functions ########################################################
########################################################################################################################

# Constraints
visualization = True  # view the camera feed with annotations
face_armature = True  # move face landmarks
body_armature = True  # move body bones
hand_armature = True  # move hand bones
neck_armature = True  # move head pose by neck cSpine bone
save_renderFs = True  # capture 3D world camera view into frames

# Refresh Format
k = 2

# weak
sensitivity = 20

# Landmark List
FACIAL_LANDMARKS_IDXS = [
    ("mouth", (48, 68)),
    ("right_eyebrow", (17, 22)),
    ("left_eyebrow", (22, 27)),
    ("right_eye", (36, 42)),
    ("left_eye", (42, 48)),
    ("nose", (27, 35)),
    ("jaw", (0, 17))
]

# Landmark List (Subset for Performance)
lm_groups = [
    ("mouth", (50, 52, 58, 56, 60, 64)),
    ("right_eyebrow", (18, 20)),
    ("left_eyebrow", (22, 24)),
    ("right_eye", (38, 40)),
    ("left_eye", (44, 48)),
    ("nose", (30, 32, 34, 36)),
    ("jaw", (2, 7, 11, 16))
]

sub = list()

for l in lm_groups:
    sub += l[1]

_lm = set(sub)

# Neck Bone for head rotation
neck_bone = ["cSpine"]

# testing focus
# _lm = lm_groups[0][1]

# Full LandMark Range
lm_full = set(list(range(0, 69)))

# data printer
p = pprint.PrettyPrinter(indent=1, width=80, depth=None, stream=None, compact=False)

# print the algorithm landmark setup
print("The full set of landmarks are:", lm_full)
print("The landmarks included in app:", _lm)
print("Landmark areas include:")
p.pprint(lm_groups)

def setMode(newMode):
    bpy.ops.object.mode_set(mode=newMode)
    return True
def setActiveBone(obj):
    obj.bone.select = True
    return True
def unSetActiveBone(obj):
    obj.bone.select = False
    return False
def force_redraw(k):
    if k == 0:
        bpy.context.scene.update()
    if k == 1:
        bpy.ops.wm.redraw_timer(type='DRAW', iterations=1)
    if k == 2:
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
def translateBoneXYZ(armatureName, modeName, boneName, x_offset, y_offset, z_offset=0):
    # Get Armature
    arm = bpy.data.objects[armatureName]

    # POSE mode allows translation
    setMode(modeName)

    # Get Bone
    targetBone = arm.pose.bones[boneName]

    # Select Bone
    setActiveBone(targetBone)
    # targetBone.bone.select_tail=True
    # targetBone.bone.select_head=True     # Make Bone Cursor Focus
    # print("Bone, Arm, position, details", targetBone, armatureName, (x_offset/100, y_offset/100, z_offset),)

    # Translate Bone
    bpy.ops.transform.translate(  # Translate Bone
        value=(x_offset / sensitivity, y_offset / sensitivity, z_offset),
        orient_type='GLOBAL',
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        orient_matrix_type='GLOBAL',
        mirror=True,
        use_proportional_edit=False,
        proportional_edit_falloff='SMOOTH',
        proportional_size=1,
        use_proportional_connected=False,
        use_proportional_projected=False,
        release_confirm=True
    )

    unSetActiveBone(targetBone)
    # targetBone.bone.select=False

    return True
def positionBoneXYZ(armatureName, modeName, x, y, z=0):
    scene = bpy.context.scene

    arm = scene.objects[armatureName]
    avatar = scene.objects["male head.obj"]
    cam = scene.objects["Camera"]

    arm = bpy.data.objects[armatureName]  # Get Armature
    setMode("POSE")  # need POSE mode to set armature bones

    for i in range(min(_lm), max(_lm) + 1):
        targetBone = arm.pose.bones["Bone." + str(i)]
        pb.location[0] = x
        pb.location[2] = y

    return True
def return_frame(f):
    # capture scene as a matrix as output
    scn = bpy.context.scene

    # go to frame f
    scn.frame_set(0)

    if save_renderFs:
        # set the filepath
        scn.render.filepath = os.path.join('C:/Users/tony/Documents/projects/mimic/AugmentedReality/recordings',
                                           str(f).zfill(4))

        # render the current frame
        bpy.ops.render.render(write_still=True)

        # bpy.ops.render.opengl(animation=False, sequencer=False, write_still=False, view_context=True)

    # output the camera matrix on the current frame
    return scn.camera.matrix_world
def rotateBoneEuler(armatureName, modeName, boneName, rotation_vector):
    # Get Armature
    arm = bpy.data.objects[armatureName]

    # POSE mode allows translation
    setMode(modeName)

    # Get Bone
    targetBone = arm.pose.bones[boneName]

    # Select Bone
    setActiveBone(targetBone)

    # xv print("Rotating the bone ->", boneName)
    armFace = bpy.data.objects["Armature.face"]

    # Set rotation mode to Euler XYZ, easier to understand
    targetBone.rotation_mode = 'XYZ'
    armFace.rotation_mode = 'XYZ'

    # select axis in ['X','Y','Z']  <--bone local
    print("Rotation vector: ", rotation_vector)

    # normalize Euler Roll
    if abs(rotation_vector[2]) > 0.1:
        rotation_vector[2] = 0.1

    targetBone.rotation_euler = rotation_vector
    armFace.rotation_euler = rotation_vector
    unSetActiveBone(targetBone)
    # m=0
    # for axis in euler:
    #    angle = rotation_vector[m]
    #    m+=1
    #    print("Rotation:", axis, angle, "(radians)")
    #    targetBone.rotation_euler.rotate_axis(axis, angle)

    # Refresh 3D View
    # force_redraw(k)

    return True
def rotationMatrixToEulerAngles(R):
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    euler_angles = np.array([x + 3.14, y * -1.0, z * -1.0])

    # xv print( "Euler Angles [yaw, pitch, roll]:", euler_angles )

    return euler_angles
def headPoseEstimation(frame, landmarks):
    # "Head-and-Face Anthropometric Survey of U.S. Respirator Users"
    #  X-Y-Z with X pointing forward and Y on the left and Z up.
    # The X-Y-Z coordinates used are like the standard
    #  coordinates of ROS (robotic operative system)
    # OpenCV uses the reference usually used in computer vision:
    #  X points to the right, Y down, Z to the front
    # The Male mean interpupillary distance is 64.7 mm (https://en.wikipedia.org/wiki/Interpupillary_distance)

    # lazy coding Image
    im = frame

    # Image dimensions in pixels
    size = im.shape

    # Landmark ID's for coordinate system reference points
    lm_nose, lm_leftMouth, lm_rightMouth = 30, 64, 60
    lm_chin, lm_leftEye, lm_rightEye = 8, 46, 37

    # 2D image points. If you change the image, you need to change vector
    landmarks_2D = np.array([
        (
            landmarks.part(lm_nose).x,
            landmarks.part(lm_nose).y),  # Nose tip
        (
            landmarks.part(lm_chin).x,
            landmarks.part(lm_chin).y),  # Chin
        (
            landmarks.part(lm_leftEye).x,
            landmarks.part(lm_leftEye).y),  # Left eye left corner
        (
            landmarks.part(lm_rightEye).x,
            landmarks.part(lm_rightEye).y),  # Right eye right corne
        (
            landmarks.part(lm_leftMouth).x,
            landmarks.part(lm_leftMouth).y),  # Left Mouth corner
        (
            landmarks.part(lm_rightMouth).x,
            landmarks.part(lm_rightMouth).y)  # Right mouth corner
    ], dtype="double")

    # 3D model points.
    landmarks_3D = np.array([
        (0.000000, -0.019541, 0.107310),  # Nose tip
        (0.000000, -0.074454, 0.064616),  # Chin
        (0.038825, 0.0068930, 0.0498460),  # Left eye left corner
        (-0.0395610, 0.0067520, 0.047923),  # Right eye right corner
        (0.021485, -0.046539, 0.0827440),  # Left Mouth corner
        (-0.0217970, -0.047244, 0.081981),  # Right mouth corner
    ])

    # Camera geometry
    focal_length = size[1] / 2
    center = (size[1] / 2, size[0] / 2)

    # Camera Matrix
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    # Distances
    camera_distortion = np.zeros((4, 1))  # Assuming no lens distortion

    # Print some red dots on the image
    for point in landmarks_2D:
        cv2.circle(frame, (int(point[0]), int(point[1])), 2, (0, 0, 255), -1)

    # retval - bool
    # rvec - Output rotation vector that, together with tvec, brings
    # points from the world coordinate system to the camera coordinate system.
    # tvec - Output translation vector. It is the position of the world origin (SELLION) in camera co-ords

    retval, rvec, tvec = cv2.solvePnP(landmarks_3D, landmarks_2D, camera_matrix, camera_distortion)

    # Get as input the rotational vector
    # Return a rotational matrix
    rmat, _ = cv2.Rodrigues(rvec)

    head_pose = [
        rmat[0, 0], rmat[0, 1], rmat[0, 2], tvec[0],
        rmat[1, 0], rmat[1, 1], rmat[1, 2], tvec[1],
        rmat[2, 0], rmat[2, 1], rmat[2, 2], tvec[2],
        0.0, 0.0, 0.0, 1.0
    ]

    # euler_angles contain (pitch, yaw, roll)
    euler_angles = rotationMatrixToEulerAngles(rmat)

    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 10.0)]), rvec, tvec, camera_matrix,
                                                     camera_distortion)

    # Points to plot vector normal to the landmarks_2d plane, p1->head, p2->tail
    p1 = (
        int(landmarks_2D[0][0]),
        int(landmarks_2D[0][1])
    )

    p2 = (
        int(nose_end_point2D[0][0][0]),
        int(nose_end_point2D[0][0][1])
    )

    cv2.line(im, p1, p2, (255, 0, 0), 3)
    cv2.putText(frame, "P1: " + str(p1) + "P2: " + str(p2), p1, font, .5, (255, 0, 0), 1, cv2.LINE_AA)

    # xv print( "Vector [(p1: x, y), (p2: x, y)] for Euler Calculation", p1, p2 )
    # xv print( "Camera Matrix :\n {0}".format(camera_matrix) )
    # xv print( "Rotation Vector:\n {0}".format(rvec) )
    # xv print( "Translation Vector:\n {0}".format(tvec) )

    return frame, euler_angles
def tracking(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    item = []
    countr = 0
    for face in faces:
        countr += 1
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        landmarks = predictor(gray, face)
        coords = {}

        for n in [2, 7, 11, 16, 18, 20, 22, 24, 30, 32, 34, 36, 38, 40, 44, 48, 50, 52, 56, 58, 60, 64]:
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)

        # Face Position Information
        info = "Frame:" + str(countr) + " x1:" + str(x1) + " y1:" + str(y1) + " x2:" + str(x2) + " y2:" + str(y2)

        # Draw face Bounding Box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(frame, info, (x1, y1), font, .25, (255, 0, 0), 1, cv2.LINE_AA)
        print("X" * 1000)

        # get angles of head pose [rotation and translation vectors]
        frame, e_a = headPoseEstimation(frame, landmarks)

    return frame

########################################################################################################################
################################################ Main Tx Class #########################################################
########################################################################################################################

class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform

    async def recv(self):
        frame = await self.track.recv()

        if self.transform == "cartoon":
            img = frame.to_ndarray(format="bgr24")

            # prepare color
            img_color = cv2.pyrDown(cv2.pyrDown(img))
            for _ in range(6):
                img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
            img_color = cv2.pyrUp(cv2.pyrUp(img_color))

            # prepare edges
            img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img_edges = cv2.adaptiveThreshold(
                cv2.medianBlur(img_edges, 7),
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                9,
                2,
            )
            img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

            # combine color and edges
            img = cv2.bitwise_and(img_color, img_edges)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        elif self.transform == "edges2":
            # perform edge detection
            img = frame.to_ndarray(format="bgr24")
            img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame

        elif self.transform == "edges":
            # perform edge detection
            img = frame.to_ndarray(format="bgr24")
            try:
                img = tracking(img)
            except Exception as e:
                print("*" * 1000)
                print(e)
                print("*" * 1000)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame

        elif self.transform == "rotate":
            # rotate image
            img = frame.to_ndarray(format="bgr24")
            rows, cols, _ = img.shape
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), frame.time * 45, 1)
            img = cv2.warpAffine(img, M, (cols, rows))

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        else:
            return frame

########################################################################################################################
############################################### Asyncronous Tx #########################################################
########################################################################################################################

async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)
async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)
async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.remote)

    # prepare local media
    player = MediaPlayer(os.path.join(ROOT, "demo-instruct.wav"))
    if args.write_audio:
        recorder = MediaRecorder(args.write_audio)
    else:
        recorder = MediaBlackhole()

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        log_info("ICE connection state is %s", pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        if track.kind == "audio":
            pc.addTrack(player.audio)
            recorder.addTrack(track)
        elif track.kind == "video":
            local_video = VideoTransformTrack(
                track, transform=params["video_transform"]
            )
            pc.addTrack(local_video)

        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )
async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

########################################################################################################################
################################################ Run __main__ ##########################################################
########################################################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebRTC audio / video / data-channels demo")
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument("--port", type=int, default=8080, help="Port for HTTP server (default: 8080)")
    parser.add_argument("--verbose", "-v", action="count")
    parser.add_argument("--write-audio", help="Write received audio to a file")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_get("/", index)
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)
    web.run_app(app, access_log=None, port=args.port, ssl_context=ssl_context)