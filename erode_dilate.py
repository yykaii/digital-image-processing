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
    src = cv2.imread('1.tif')
    if isShowImage:
        showCV2Image('src', src)
    #灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    if isShowImage:
        showCV2Image('gray', gray)
    #二值化
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
    if isShowImage:
        showCV2Image('binary', binary)

    # 腐蚀/膨胀
    kernel = np.ones((3, 3), np.uint8)

    # 填洞，先膨胀再腐蚀，闭运算
    #先找连通域，去除小的点，然后再做膨胀腐蚀














