# -*- coding:utf-8 -*-
import cv2
import numpy as np
import argparse

#construct the argument parse and parse the arguments
#从命令行中捕获所需的信息，即输入图像的路径
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='path to input image file')
args = vars(ap.parse_args())

#load image from disk
image = cv2.imread(args['image'])

#把文本从图片中分离出来
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)#确保字是白色，背景是黑色

thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#捕获所有像素点的角度（角度大于零的像素），然后找一个最大的旋转角度可以把所有的包含在其中
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]#返回的角度在[-90，0）按顺时针计算
if angle < -45:
    angle = -(90+angle)
else:
    angle = -angle

#找到角度之后进行仿射变换矫正
#rotate the image to deskew it
(h, w) = image.shape[:2]
center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

cv2.putText(rotated, 'Angle:{:.2f} degrees'.format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

print('[INFO] angle:{:.3f}'.format(angle))
cv2.imshow('input', image)
cv2.waitKey(0)
cv2.imshow('rotate', rotated)
cv2.waitKey(0)

