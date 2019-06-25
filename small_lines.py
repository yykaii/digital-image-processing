# -*- coding:utf-8 -*-
import cv2
import os
import numpy as np
from skimage import measure, color, morphology
#Done

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('APT003.tif')

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
    # binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    if isShowImage:
       showCV2Image('binary', binary)

    rows, cols = binary.shape

    scale1 = 25
    scale2 = 40
    scale3 = 45

    #第一次识别
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale1, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
    if isShowImage:
        showCV2Image("Dilated col", dilatedcol)

    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
    if isShowImage:
        showCV2Image("Dilated row", dilatedrow)

    # 识别表格线
    table1 = cv2.bitwise_or(dilatedcol, dilatedrow)
    if isShowImage:
        showCV2Image("table line1", table1)

    # 第2次识别
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale2, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
    if isShowImage:
        showCV2Image("Dilated col2", dilatedcol)

    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale2))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
    if isShowImage:
        showCV2Image("Dilated row2", dilatedrow)

    # 识别表格线
    table2 = cv2.bitwise_or(dilatedcol, dilatedrow)
    if isShowImage:
        showCV2Image("table line2", table2)

    # 第3次识别
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale3, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
    if isShowImage:
        showCV2Image("Dilated col3", dilatedcol)

    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale3))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
    if isShowImage:
        showCV2Image("Dilated row3", dilatedrow)

    # 识别表格线
    table3 = cv2.bitwise_or(dilatedcol, dilatedrow)
    if isShowImage:
        showCV2Image("table line3", table3)

    not_detect1 = cv2.subtract(table3, table2)
    if isShowImage:
        showCV2Image('not_detect1', not_detect1)

    add_table = cv2.add(table1, not_detect1)
    if isShowImage:
        showCV2Image('add_table', add_table)

    remove_lines = cv2.bitwise_xor(binary, add_table)
    remove_lines = cv2.bitwise_not(remove_lines)
    if isShowImage:
        showCV2Image('remove_lines', remove_lines)
    cv2.imwrite('APT003_removeline.jpg', remove_lines)

    # median = cv2.medianBlur(binary, 9)
    # if isShowImage:
    #     showCV2Image('median', median)
    #
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    #
    # erodation = cv2.erode(binary, kernel)
    # if isShowImage:
    #     showCV2Image('erodation', erodation)
    #
    # dilation = cv2.dilate(erodation, kernel)
    # if isShowImage:
    #     showCV2Image('dilation', dilation)

