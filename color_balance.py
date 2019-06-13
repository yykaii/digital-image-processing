# -*- coding:utf-8 -*-
import cv2
import numpy as np
import copy
from PIL import Image
from remove_light import image_enhancement

isShowImage = True
def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('Johns_check.jpg')
    if isShowImage:
        showCV2Image('src', src)

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)  # 彩色转灰度图
    rows, cols = gray.shape
    if isShowImage:
        showCV2Image('gray', gray)

    bgr = cv2.split(src)
    gray_mean = []
    for i in range(len(bgr)):
        gray_mean.append(np.mean(bgr[i]))#各通道的灰度值
    print('gray_mean', gray_mean)
    gray_aver = np.sum(gray_mean)/3#整个图片的平均灰度值
    print('gray_aver', gray_aver)

    #调整每个像素的bgr值，使其与平均灰度值接近
    times = []
    for i in range(len(bgr)):
        times.append(gray_aver/gray_mean[i])
    print('times', times)

    bgr1 = copy.deepcopy(bgr)
    for i in range(len(bgr)):
        for j in range(rows):
            for s in range(cols):
                bgr1[i][j][s] = bgr[i][j][s]*times[i]

    #调整像素到可示范区间
    max1 = []
    new = copy.deepcopy(bgr1)
    for i in range(len(new)):
        maxmax = np.array(new[i]).flatten()
        mm = max(maxmax)
        print('maxmax', maxmax)
        max1.append(mm)
    print('max1', max1)
    max1.sort()
    factor = max1[-1]/255
    print('factor', factor)
    if factor > 1:
        bgr1 = bgr1/factor

    img = cv2.merge(bgr1)
    if isShowImage:
        showCV2Image('img', img)

    cv2.imwrite('Johns_check_colorbalance.jpg', img)
    src1 = Image.open('Johns_check_colorbalance.jpg')
    enh = image_enhancement(src1)


