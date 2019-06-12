# -*- coding:utf-8 -*-
import cv2
import numpy as np
from PIL import Image
from PIL import ImageEnhance
from skimage import measure, color,morphology

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('equ_colored.jpg')
    if isShowImage:
        showCV2Image('src', src)

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    if isShowImage:
        showCV2Image('gray', gray)

    #法2：腐蚀膨胀，去除小的连通域
    rows, cols = gray.shape
    area = 40
    for i in range(rows):
        for j in range(cols):
            if gray[i, j] < area:
                gray[i, j] = 255
            else:
                gray[i, j] = 0

    kernel = np.ones((3, 3), np.uint8)
    kernel[1] = 0
    gray1 = cv2.erode(gray, kernel)
    gray1 = cv2.dilate(gray1, kernel)
    if isShowImage:
        showCV2Image('gray1', gray1)

    # for i in range(rows):
    #     for j in range(cols):
    #         if gray1[i, j] == 255:
    #             src[i, j] = 255
    # if isShowImage:
    #     showCV2Image('gray_', src)
    #
    # cv2.imwrite('remove_small1.jpg', src)

    labels, nums = measure.label(gray1, connectivity=2, return_num=True)
    props = measure.regionprops(labels)
    print(labels.shape)
    print(labels)
    areas = []
    for i in range(nums):
        areas.append(props[i]['area'])
    print('areas', areas)
    max_value = max(areas)
    print('max_value', max_value)
    image = morphology.remove_small_objects(labels, min_size=1, connectivity=1)#去除小的连通域
    cv2.imwrite('remove_area.jpg', image)


    for i in range(rows):
        for j in range(cols):
            if image[i, j] != 0:
                src[i, j] = 255
    if isShowImage:
        showCV2Image('gray_', src)

    cv2.imwrite('remove_small1.jpg', src)



