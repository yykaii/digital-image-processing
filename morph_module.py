# -*- coding:utf-8 -*-
import cv2
from skimage import exposure
import numpy as np
import copy
import math

#二值化
def binary(gray):
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
    # if isShowImage:
    #     showCV2Image('binary', binary)
    return binary

#开操作，先腐蚀小的噪点，再膨胀，输入为二值图像
def open(bins):
    kernel1 = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(bins, kernel1)
    # if isShowImage:
    #     showCV2Image('eroded', eroded)
    dilation = cv2.dilate(eroded, kernel2)
    # if isShowImage:
    #     showCV2Image('dilation', dilation)
    return dilation

#中值滤波，去椒盐噪声，输入为二值图像
def medianblur(bins):
    medianblur = cv2.medianBlur(bins, 3)
    # if isShowImage:
    #     showCV2Image('median', medianblur)
    medianblur1 = cv2.bitwise_not(medianblur)
    # if isShowImage:
    #     showCV2Image('median1', medianblur1)
    cv2.imwrite('3_median.jpg', medianblur1)

# 填洞，先膨胀再腐蚀，闭运算，输入为二值图像
#先找连通域，去除小的点，然后再做膨胀腐蚀
def close(bins):
    kernel1 = np.ones((3, 3), np.uint8)
    dilation2 = cv2.dilate(bins, kernel1)
    # if isShowImage:
    #     showCV2Image('dilation2_', dilation2)
    eroded2 = cv2.erode(dilation2, kernel1)
    # if isShowImage:
    #     showCV2Image('erode2', eroded2)
    dilation2 = cv2.bitwise_not(eroded2)
    # if isShowImage:
    #     showCV2Image('dilation2_1', dilation2)
    # cv2.imwrite('3_median_dilation2.jpg', dilation2)
    return dilation2

#输入为二值图像，去除横竖表格线
def removelines(bins):
    rows, cols = bins.shape
    scale = 20
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(bins, kernel, iterations=1)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
    # if isShowImage:
    #     showCV2Image("Dilated Image", dilatedcol)

    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(bins, kernel, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
    # if isShowImage:
    #     showCV2Image("Dilated Image", dilatedrow)

    # 识别表格线
    table = cv2.bitwise_or(dilatedcol, dilatedrow)
    # if isShowImage:
    #     showCV2Image("table line", table)

    # 去掉表格线
    no_tab_line = cv2.bitwise_xor(bins, table)
    # if isShowImage:
    #     showCV2Image("no table line", no_tab_line)

    # 黑白反色
    n_tab_line = cv2.bitwise_not(no_tab_line)
    # if isShowImage:
    #     showCV2Image("n_table line", n_tab_line)
    # cv2.imwrite(str(file) + '_removelines.jpg', n_tab_line)
    return n_tab_line


