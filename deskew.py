import cv2
import os
import numpy as np
from skimage import measure, color
#Done

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
        image = cv2.imread('APT001.tif')
        #二值化
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if isShowImage:
            showCV2Image('gray', gray)

        binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -3)
        if isShowImage:
            showCV2Image('binary', binary)

        binary1 = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, -3)
        if isShowImage:
            showCV2Image('binary1', binary1)

        a = cv2.bitwise_xor(gray, binary1)
        if isShowImage:
            showCV2Image('a', a)

        a1 = cv2.bitwise_not(a)
        if isShowImage:
            showCV2Image('a1', a1)

        b = cv2.bitwise_xor(a, binary1)
        if isShowImage:
            showCV2Image('b', b)

        rows, cols = binary.shape
        scale = 20
        #识别横线
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols//scale, 1))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
        if isShowImage:
            showCV2Image("Dilated Image", dilatedcol)

        #识别竖线
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows//scale))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
        if isShowImage:
            showCV2Image("Dilated Image", dilatedrow)

        #识别表格线
        table = cv2.bitwise_or(dilatedcol, dilatedrow)
        if isShowImage:
            showCV2Image("table line", table)

        #去掉表格线
        no_tab_line = cv2.bitwise_xor(binary, table)
        if isShowImage:
            showCV2Image("no table line", no_tab_line)

        #黑白反色
        n_tab_line = cv2.bitwise_not(no_tab_line)
        if isShowImage:
            showCV2Image("n_table line", n_tab_line)

        # contours = cv2.findContours(n_tab_line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = contours[0]
        # print('cnts', np.array(cnts).shape )

        # pts = np.zeros((rows, cols))
        # for c in cnts:
        #     cv2.drawContours(pts, [c], (255, 255, 255))

        # if isShowImage:
        #     showCV2Image('pts', pts)
        # cv2.imwrite('APT004_1.jpg', n_tab_line)

        c = cv2.subtract(a1, binary1)
        if isShowImage:
            showCV2Image('c', c)

        d = cv2.subtract(n_tab_line, a1)
        if isShowImage:
            showCV2Image('d', d)