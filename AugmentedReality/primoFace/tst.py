import numpy as np
import cv2

# load image and set the bounds
img = cv2.imread("C:\\Users\\tony\\Desktop\\ColorPallette.jpg")
lower =(0, 0, 255) # lower bound for each channel
upper = (255, 0, 0) # upper bound for each channel

# create the mask and use it to change the colors
mask = cv2.inRange(img, lower, upper)
img[mask != 0] = [0,0,255]

scale_percent = 60  # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

# display it
cv2.imshow("frame", resized)
cv2.waitKey(0)

# import the necessary packages
import scipy.spatial as sp
import matplotlib.pyplot as plt


# Stored all RGB values of main colors in a array
main_colors = [(0, 0, 0),
               (255, 255, 255),
               (255, 0, 0),
               (0, 255, 0),
               (0, 0, 255),
               (255, 255, 0),
               (0, 255, 255),
               (255, 0, 255),
               ]

image = cv2.imread("C:\\Users\\tony\\Desktop\\ColorPallette.jpg")
# convert BGR to RGB image
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

h, w, bpp = np.shape(image)

# Change colors of each pixel
# reference :https://stackoverflow.com/a/48884514/9799700
for py in range(0, h):
    for px in range(0, w):
        ########################
        # Used this part to find nearest color
        # reference : https://stackoverflow.com/a/22478139/9799700
        input_color = (image[py][px][0], image[py][px][1], image[py][px][2])
        tree = sp.KDTree(main_colors)
        ditsance, result = tree.query(input_color)
        nearest_color = main_colors[result]
        ###################

        image[py][px][0] = nearest_color[0]
        image[py][px][1] = nearest_color[1]
        image[py][px][2] = nearest_color[2]

# show image
plt.figure()
plt.axis("off")
plt.imshow(image)