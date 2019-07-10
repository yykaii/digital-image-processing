# -*- coding:utf-8 -*-
import cv2
from skimage import exposure
import numpy as np
import copy
import math

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)


#二值化
def binary(gray):
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
    return binary

#开操作，先腐蚀小的噪点，再膨胀，输入为二值图像
def open(bins):
    kernel1 = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(bins, kernel1)
    dilation = cv2.dilate(eroded, kernel2)
    return dilation

#中值滤波，去椒盐噪声，输入为二值图像
def medianblur(bins):
    medianblur = cv2.medianBlur(bins, 3)
    medianblur1 = cv2.bitwise_not(medianblur)
    return medianblur1

# 填洞，先膨胀再腐蚀，闭运算，输入为二值图像
#先找连通域，去除小的点，然后再做膨胀腐蚀
def close(bins):
    kernel1 = np.ones((3, 3), np.uint8)
    dilation2 = cv2.dilate(bins, kernel1)
    eroded2 = cv2.erode(dilation2, kernel1)
    dilation2 = cv2.bitwise_not(eroded2)
    return dilation2

#输入为二值图像，去除横竖表格线
def removelines(bins):
    rows, cols = bins.shape
    scale = 20
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(bins, kernel, iterations=1)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)

    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(bins, kernel, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)

    # 识别表格线
    table = cv2.bitwise_or(dilatedcol, dilatedrow)

    # 去掉表格线
    no_tab_line = cv2.bitwise_xor(bins, table)

    # 黑白反色
    n_tab_line = cv2.bitwise_not(no_tab_line)
    return n_tab_line

def wrap_perspective(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # canny边缘检测
    canny_edges = cv2.Canny(gray, 50, 250)

    # 霍夫变换，得到纸的边缘线条
    lines = cv2.HoughLinesP(canny_edges, 1, np.pi / 180, 50, minLineLength=90, maxLineGap=10)

    # for x1, y1, x2, y2 in lines[0]:
    #     print(x1, y1), (x2, y2)
    # for x1, y1, x2, y2 in lines[1]:
    #     print(x1, y1), (x2, y2)

    # 绘制边缘
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(gray, (x1, y1), (x2, y2), (0, 0, 255), 1)
    # 根据四个顶点设置图像透视变换矩阵
    pos1 = np.float32([[114, 82], [287, 156], [8, 322], [216, 333]])
    pos2 = np.float32([[0, 0], [188, 0], [0, 262], [188, 262]])
    M = cv2.getPerspectiveTransform(pos1, pos2)
    # 图像透视变换
    result = cv2.warpPerspective(image, M, (190, 272))
    # 显示图像
    return result



