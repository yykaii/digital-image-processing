# -*- coding:utf-8 -*-
import cv2
import numpy as np
from skimage import measure, color,morphology


isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    #原图
    src = cv2.imread('3.jpg')
    if isShowImage:
        showCV2Image('src', src)

    #灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)


    #二值化
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
    if isShowImage:
        showCV2Image('binary', binary)

    # 腐蚀/膨胀
    kernel1 = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)

    # 填洞，先膨胀再腐蚀，闭运算
    #先找连通域，去除小的点，然后再做膨胀腐蚀
    eroded = cv2.erode(binary, kernel1)
    if isShowImage:
        showCV2Image('eroded', eroded)

    dilation = cv2.dilate(eroded, kernel2)
    if isShowImage:
        showCV2Image('dilation', dilation)

    #中值滤波
    medianblur = cv2.medianBlur(binary, 3)
    if isShowImage:
        showCV2Image('median', medianblur)
    medianblur1 = cv2.bitwise_not(medianblur)
    if isShowImage:
        showCV2Image('median1', medianblur1)
    cv2.imwrite('3_median.jpg', medianblur1)

    #膨胀
    dilation2 = cv2.dilate(medianblur, kernel1)
    if isShowImage:
        showCV2Image('dilation2_', dilation2)

    eroded2 = cv2.erode(dilation2, kernel1)
    if isShowImage:
        showCV2Image('erode2', eroded2)
    dilation2 = cv2.bitwise_not(eroded2)
    if isShowImage:
        showCV2Image('dilation2_1', dilation2)
    cv2.imwrite('3_median_dilation2.jpg', dilation2)
















