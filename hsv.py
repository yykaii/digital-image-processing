# -*- coding:utf-8 -*-
import cv2
import numpy as np

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('c14.jpg')
    if isShowImage:
        showCV2Image('src', src)

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    median = cv2.medianBlur(gray, 3)
    if isShowImage:
        showCV2Image('median', median)

    # kernel = np.ones((3, 3), np.uint8)
    #
    # #先腐蚀，再膨胀
    # dilation = cv2.dilate(gray, kernel)
    # if isShowImage:
    #     showCV2Image('dilation', dilation)
    #
    # eroded = cv2.erode(dilation, kernel)
    # if isShowImage:
    #     showCV2Image('eroded', eroded)
    cv2.imwrite('c14_.jpg', median)







