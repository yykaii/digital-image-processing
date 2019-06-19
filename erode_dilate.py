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
    cv2.imshow('src', src)
    cv2.waitKey(0)

    #灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    cv2.waitKey(0)
    #二值化
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
    cv2.imshow('binary', binary)
    cv2.waitKey(0)

    # 腐蚀/膨胀
    kernel1 = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)

    # 填洞，先膨胀再腐蚀，闭运算
    #先找连通域，去除小的点，然后再做膨胀腐蚀
    eroded = cv2.erode(binary, kernel1)
    cv2.imshow('eroded', eroded)
    cv2.waitKey(0)
    dilation = cv2.dilate(eroded, kernel2)
    cv2.imshow('dilation', dilation)
    cv2.waitKey(0)

    # if isShowImage:
    #     showCV2Image('dilation', dilation)

    medianblur = cv2.medianBlur(binary, 3)
    cv2.imshow('median', medianblur)
    cv2.waitKey(0)

    dilation2 = cv2.dilate(medianblur, kernel1)
    cv2.imshow('dilation2', dilation2)
    cv2.waitKey(0)
    if isShowImage:
        showCV2Image('dilation2_', dilation2)
















