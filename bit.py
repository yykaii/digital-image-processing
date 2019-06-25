import cv2
import os
from matplotlib import pyplot as plt
from skimage import measure, color, morphology
#Done

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
        image = cv2.imread('2.jpg')
        if isShowImage:
            showCV2Image('image', image)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if isShowImage:
            showCV2Image('gray', gray)

        for i in range(8):
            ret, binary = cv2.threshold(gray, pow(2, i)/2-1, 255, cv2.THRESH_BINARY)
            if isShowImage:
                showCV2Image('binary', binary)
