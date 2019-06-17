# -*- coding:utf-8 -*-
import cv2
import numpy as np

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('Johns_Form_equ_hist.jpg')
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    if isShowImage:
        showCV2Image('h', h)
        showCV2Image('s', s)
        showCV2Image('v', v)

    lower_blue = np.array([78, 43, 46])
    upper_blue = np.array([110, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    if isShowImage:
        showCV2Image('mask', mask)

    res = cv2.bitwise_and(src, src, mask=mask)
    if isShowImage:
        showCV2Image('res', res)

    hun = cv2.bitwise_xor(res, src)
    if isShowImage:
        showCV2Image('hun', hun)

    hun1 = cv2.bitwise_not(res, src)
    if isShowImage:
        showCV2Image('hun1', hun1)





