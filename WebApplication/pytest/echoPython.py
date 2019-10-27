import cv2 as cv
import numpy as np
import pickle

def echoThis(image, show):
    height, width, channels = image.shape
    center = (int(width/2), int(height/2))
    radius = height/2
    edge = int(height*0.01)
    print("Height, Width, Channel, Center:", height, width, channels, center)


    img = np.zeros((height, width, 3), np.uint8)
    img[:, :] = [255, 255, 255]

    cv.circle(img, center, radius, (115, 255, 115), edge)
    if show == True:
        cv.imshow("IMAGE:", img)
        cv.waitKey(3000)

    return image
def pickleImage():
    image = cv.imread("cam.jpg")
    pkl_file = open('img.pkl','wb')
    pickle.dump(image,pkl_file)
def usePickle():
    with open('img.pkl', 'rb') as f:
        echoThis(pickle.load(f), True)


usePickle()