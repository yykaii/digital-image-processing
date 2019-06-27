import cv2
import os
from matplotlib import pyplot as plt
from skimage import measure, color, morphology
import numpy as np
import math
#Done

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
        image = cv2.imread('c1.jpg')
        if isShowImage:
            showCV2Image('image', image)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if isShowImage:
            showCV2Image('gray', gray)

        rows, cols = gray.shape

        #比特分层
        bits = []
        for i in range(8):
            ret, binary = cv2.threshold(gray, pow(2, i)-1, 255, cv2.THRESH_BINARY)
            bits.append(binary)
            if isShowImage:
                showCV2Image('binary'+str(i), binary)

        #重建，4个高层的比特面即可很好重建
        bits.reverse()

        re = bits[0]
        for s in range(4):
            re = cv2.bitwise_and(bits[s], re)

        if isShowImage:
            showCV2Image('re', re)

        cv2.imwrite('c1_bit.jpg', re)

