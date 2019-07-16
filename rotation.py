# -*- coding:utf-8 -*-
import cv2
import math
import numpy as np

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('Alex_dl.jpg')
    if isShowImage:
        showCV2Image('src', src)

    # 灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    if isShowImage:
        showCV2Image('gray', gray)

    rows, cols = gray.shape

    #以对角线的长度，为原图加边框，防止旋转后图片不能完整展示
    dia_length = int(math.sqrt(rows*rows+cols*cols))

    img_ex = cv2.copyMakeBorder(src, dia_length-rows, dia_length-rows, dia_length-cols, dia_length-cols, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    if isShowImage:
        showCV2Image('img_ex', img_ex) #加了边框的图

    rows1, cols1 = img_ex.shape[:2]
    center = (int(cols1/2), int(rows1/2))#寻找质心，即旋转中心

    rotate = cv2.getRotationMatrix2D(center, -89, 1)#旋转转换矩阵，第三个参数是缩放系数，1表示保持原图大小
    img_ex_rotate = cv2.warpAffine(img_ex, rotate, (cols1, rows1))

    if isShowImage:
        showCV2Image('img_rotate', img_ex_rotate)

    cv2.imwrite('Alex_dl_r.jpg', img_ex_rotate)



