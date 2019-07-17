# import the necessary packages
import numpy as np
import cv2
import math
#先做正常旋转判断，再通过判断长宽比判断是否需要旋转90度

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

image = cv2.imread('0.png')
if isShowImage:
    showCV2Image('input', image)

gray1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
if isShowImage:
    showCV2Image('gray1', gray1)
# gray1 = cv2.bitwise_not(gray1)


# thresh = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
thresh = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
if isShowImage:
    showCV2Image('thresh', thresh)
# print('thresh', thresh)

coords = np.column_stack(np.where(thresh > 0))#列合并，相当于把二值图像中255的地方都输出

rect = cv2.minAreaRect(coords)
angle = rect[2]
width = int(rect[1][0])
height = int(rect[1][1])

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
rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# draw the correction angle on the image so we can validate it
cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# show the output image
print("[INFO] angle: {:.3f}".format(angle))
if isShowImage:
    showCV2Image('rotated', rotated)
cv2.imwrite('deskewed_r0.jpg', rotated)



gray2 = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
rows, cols = gray2.shape

dia_length = int(math.sqrt(rows*rows+cols*cols))
img_ex = cv2.copyMakeBorder(rotated, int((dia_length-rows)/2), int((dia_length-rows)/2), int((dia_length-cols)/2), int((dia_length-cols)/2), cv2.BORDER_CONSTANT, value=(255, 255, 255))


rows1, cols1 = img_ex.shape[:2]
center = (int(cols1/2), int(rows1/2))

if isShowImage:
    showCV2Image('img_ex1', img_ex) #加了边框的图


coords = np.column_stack(np.where(thresh > 0))

rect = cv2.minAreaRect(coords)
angle = rect[2]
width = int(rect[1][0])
height = int(rect[1][1])
print('rect', rect)

# if width > height:
rotate = cv2.getRotationMatrix2D(center, 0-angle, 1)  # 旋转转换矩阵，第三个参数是缩放系数，1表示保持原图大小
img_ex_rotate = cv2.warpAffine(img_ex, rotate, (cols1, rows1))
if isShowImage:
    showCV2Image('img_rotate', img_ex_rotate)
# else:
#     img_ex_rotate = img_ex

x1 = int(cols1/2)-int(cols/2)
y1 = int(rows1/2)-int(rows/2)
x2 = int(cols1/2)+int(cols/2)
y2 = int(rows1/2)+int(rows/2)

img2 = img_ex_rotate[x1:x2, y1:y2]
if isShowImage:
    showCV2Image('img2', img2)















