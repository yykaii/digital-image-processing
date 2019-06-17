# -*- coding:utf-8 -*-
import cv2
import numpy as np

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

def whiteBalance(img):
    #rows = img.shape[0]
    #cols = img.shape[1]
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(lab[:, :, 1])
    avg_b = np.average(lab[:, :, 2])
    for x in range(lab.shape[0]):
        for y in range(lab.shape[1]):
            l, a, b = lab[x, y, :]
            l *= 100/255.0
            lab[x, y, 1] = a - ((avg_a-128)*(1/100.0)*1.1)
            lab[x, y, 2] = b - ((avg_b - 128) * (1 / 100.0) * 1.1)
    lab = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return lab

if __name__ == '__main__':
    src = cv2.imread('r.png')
    f = whiteBalance(src)
    cv2.imwrite('awb_r.jpg', f)