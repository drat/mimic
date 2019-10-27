#CGMatter Face Mocap Script
import bpy

iter = 1

#rename trackers
FaceTrackers = bpy.data.collections.new('FaceTrackers')
bpy.context.scene.collection.children.link(FaceTrackers)
for trackers in bpy.data.objects:
   if trackers.type != 'EMPTY':
       continue
   else:
       iter = iter + 1
       FaceTrackers.objects.link(trackers)
if FaceTrackers:
    for i, o in enumerate(FaceTrackers.objects):
        o.name = "Tracker%d" % (i+1)

#face mesh setup
bpy.context.scene.frame_set(1)
for obj in bpy.context.selected_objects:
    obj.name = "Head"
    obj.data.name = "Head"
bpy.ops.object.transform_apply()

#trackers with depth
for value in range(1,iter):
    selectname = "Tracker" + str(value)
    ob = bpy.data.objects[selectname]
    bpy.context.view_layer.objects.active = ob
    bpy.context.object.constraints["Follow Track"].depth_object = bpy.data.objects["Head"]

#add armatures to trackers
for value in range(1,iter):
    selectname = "Tracker" + str(value)
    ob = bpy.data.objects[selectname]
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.armature_add(enter_editmode=False, location=ob.matrix_world.translation)

#select armatures
for bones in bpy.data.objects:
   if bones.type != 'ARMATURE':
       continue
   else:
       bones.select_set(state=True)

#join armatures in correct order
bpy.context.view_layer.objects.active = ob = bpy.data.objects['Armature']
bpy.ops.object.join()
bpy.ops.object.transform_apply()

#rename bones in armature
for value in range(1,iter):
    if value == 1:
        bonename = "Bone"
    elif value > 1 and value < 11:
        bonename = "Bone.00" + str(value-1)
    elif value >= 11:
        bonename = "Bone.0" + str(value-1)
    bone = bpy.data.objects['Armature'].data.bones.get(bonename)
    bpy.data.objects['Armature'].data.bones[bonename].name = 'Bone' + str(value)

#parent face to bones
bpy.data.objects['Head'].select_set(True)
bpy.data.objects['Armature'].select_set(True)
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

#parent bones to trackers
bpy.ops.object.posemode_toggle()
for value in range(1,iter):
    trackname = "Tracker" + str(value)
    bonename = "Bone" + str(value)
    bone = bpy.data.objects['Armature'].data.bones.get(bonename)
    bpy.data.objects['Armature'].data.bones.active = bone
    bpy.ops.pose.constraint_add(type='COPY_LOCATION')
    bpy.context.object.pose.bones[bonename].constraints["Copy Location"].use_z = False
    bpy.context.object.pose.bones[bonename].constraints["Copy Location"].target = bpy.data.objects[trackname]
    bone.select = False