# -*- coding:utf-8 -*-
import cv2
import numpy as np
import copy

isShowImage = True
def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('johns_letter.jpg')
    [b, g, r] = cv2.split(src)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    if isShowImage:
        showCV2Image('gray', gray)

    rows, cols = gray.shape

    gray_list = gray.flatten()
    gray_list = list(set(gray_list))#每个像素的灰度值
    print('gray_list', gray_list)

    gray_num = []
    gray_list1 = gray.flatten()
    gray_list1 = list(gray_list1)
    for i in range(len(gray_list)):
        counts = gray_list1.count(gray_list[i])
        gray_num.append(counts)
    print('gray_num', gray_num)#每个灰度值的像素个数

    gray_list.reverse()
    index = int(len(gray_list)*0.05)
    maxpixel = gray_list[:index]#参考白
    print('maxpixel', maxpixel)
    mean_pixel = np.mean(maxpixel)#参考白的平均灰度
    print('mean_pixel', mean_pixel)
    coe = 255/mean_pixel#光照补偿系数
    print('coe', coe)

    for i in range(rows):
        for j in range(cols):
            b[i][j] = b[i][j]*coe
            g[i][j] = g[i][j]*coe
            r[i][j] = r[i][j]*coe

    src1 = cv2.merge([b, g, r])
    if isShowImage:
        showCV2Image('src1', src1)






