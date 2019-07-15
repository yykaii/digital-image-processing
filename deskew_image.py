# -*- coding:utf-8 -*-
import cv2
import numpy as np
from skimage import transform

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('alex_check.jpg')
    if isShowImage:
        showCV2Image('src', src)

    # 灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    if isShowImage:
        showCV2Image('gray', gray)

    rows, cols = gray.shape

    #二值化
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
    if isShowImage:
        showCV2Image('binary', binary)

    #滤波
    # medianblur = cv2.medianBlur(binary, 3)
    # if isShowImage:
    #     showCV2Image('blur', medianblur)

    # kernel1 = np.ones((3, 3), np.uint8)
    # kernel2 = np.ones((5, 5), np.uint8)
    # eroded = cv2.erode(binary, kernel1)
    # dilation = cv2.dilate(eroded, kernel1)
    # if isShowImage:
    #     showCV2Image('dila', dilation)

    # wiener =

    #canny边缘检测
    canny_edges = cv2.Canny(binary, 100, 500)
    if isShowImage:
        showCV2Image('canny', canny_edges)

    #霍夫变换，得到纸的边缘线条
    # lines = cv2.HoughLinesP(canny_edges, 1, np.pi/180, 50, minLineLength=90, maxLineGap=10)


    #randon变换
    # theta = np.arange(179)
    # print('thet', theta)

    randon = transform.radon(canny_edges)
    if isShowImage:
        showCV2Image('radon', randon)


    c = 1
    for i in range(1, rows):
        for j in range(1, cols):
            if randon[1, 1] < randon[i, j]:
                randon[1, 1] = randon[i, j]
                c = j
    print('c', c)
    rot = 90-c
    i5 = cv2.rotate(src, rot)
    if isShowImage:
        showCV2Image('i5', i5)






