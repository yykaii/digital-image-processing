# import the necessary packages
import numpy as np
import argparse
import cv2
from PIL import Image
import math


isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,help="path to input image file")
# args = vars(ap.parse_args())

# load the image from disk

# image = cv2.imread(args["image"])
image = cv2.imread('r0.jpg')

# convert the image to grayscale and flip the foreground and background to ensure foreground is now "white" and the background is "black"
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)

rows, cols = gray.shape
dia_length = int(math.sqrt(rows*rows+cols*cols))
img_ex = cv2.copyMakeBorder(image, int((dia_length-rows)), int((dia_length-rows)), int((dia_length-cols)), int((dia_length-cols)), cv2.BORDER_CONSTANT, value=(255, 255, 255))
cv2.imwrite('r0_1.jpg', img_ex)
if isShowImage:
    showCV2Image('img_ex', img_ex) #加了边框的图
rows1, cols1 = img_ex.shape[:2]
center = (int(cols1/2), int(rows1/2))

img = Image.open('r0_1.jpg')

# threshold the image, setting all foreground pixels to 255 and all background pixels to 0
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# grab the (x, y) coordinates of all pixel values that are greater than zero, then use these coordinates to
# compute a rotated bounding box that contains all coordinates
coords = np.column_stack(np.where(thresh > 0))

rect = cv2.minAreaRect(coords)
angle = rect[2]
width = int(rect[1][0])
height = int(rect[1][1])

if width < height:

    img = img.rotate(-90)
    img.show()

x1 = int(cols1/2)-int(cols/2)
y1 = int(rows1/2)-int(rows/2)
x2 = int(cols1/2)+int(cols/2)
y2 = int(rows1/2)+int(rows/2)
img.crop((y1, x1), (y2, x2))
img.save('r0_90.jpg')


# the `cv2.minAreaRect` function returns values in the range [-90, 0); as the rectangle rotates clockwise the
# returned angle trends to 0 -- in this special case we need to add 90 degrees to the angle
if angle < -45:
    angle = -(90 + angle)
# otherwise, just take the inverse of the angle to make it positive
else:
    angle = -angle

# rotate the image to deskew it
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h),flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# draw the correction angle on the image so we can validate it
cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# show the output image
print("[INFO] angle: {:.3f}".format(angle))
if isShowImage:
    showCV2Image('input', image)
    showCV2Image('rotated', rotated)

cv2.imwrite('deskewed_r0.jpg', rotated)











