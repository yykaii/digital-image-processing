import cv2
import numpy as np

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('8.jpg', cv2.IMREAD_GRAYSCALE)#直接返回一个灰度图
    if isShowImage:
        showCV2Image('src', src)
    src1 = cv2.bitwise_not(src)
    if isShowImage:
        showCV2Image('src1', src1)

    rows, cols = src.shape
    new = np.zeros((rows, cols), np.uint8)+255
    if isShowImage:
        showCV2Image('new', new)

    yu = cv2.bitwise_and(src1, new)
    if isShowImage:
        showCV2Image('yu', yu)