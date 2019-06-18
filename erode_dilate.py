# -*- coding:utf-8 -*-
import cv2
import numpy as np

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)


if __name__ == '__main__':
    src = cv2.imread('c2.jpg')
    if isShowImage:
        showCV2Image('src', src)

    kernel = np.ones((3, 3), np.uint8)
    # 填洞，先膨胀再腐蚀
    # src1 = cv2.erode(src, kernel=kernel)
    # if isShowImage:
    #     showCV2Image('src1', src1)
    #
    # src2 = cv2.dilate(src1, kernel=kernel)
    # if isShowImage:
    #     showCV2Image('src2', src2)
    # cv2.imwrite('c1_e_d.jpg', src2)

    #消除小区域，先腐蚀再膨胀
    src1 = cv2.dilate(src, kernel=kernel)
    if isShowImage:
        showCV2Image('src1', src1)

    src2 = cv2.erode(src1, kernel=kernel)
    if isShowImage:
        showCV2Image('src2', src2)
    cv2.imwrite('c2_e_d.jpg', src2)

