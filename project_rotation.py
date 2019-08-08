# -*- coding:utf-8 -*-
import cv2
import numpy as np
import math

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    image = cv2.imread('1.png')
    if isShowImage:
        showCV2Image('input', image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if isShowImage:
        showCV2Image('gray', gray)

    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)#黑纸白字
    if isShowImage:
        showCV2Image('binary', binary)

    #通过投影分析，如果为±90°，则在纵轴投影，若为±180°，则在横轴投影
    #若为+90°，则大部分情况应该是图片上半部分的平均值大于下半部分的
    #若为180°，则右半部较大，0°则左半部较大
    #基于文字的排布，皆是从左到右，但对于论文这种通篇排布紧密，或有表格或公式的情况，容易出错

    rows, cols = binary.shape
    print(rows, cols)
    newimg = np.zeros((rows, cols), np.uint8)

    #纵轴投影
    #先求和
    rowsum = binary.sum(axis=1)
    for i in range(rows):
        if rowsum[i] == 0:
            for x in range(cols):
                newimg[i][x] = 0
        else:
            t = int(rowsum[i] / 255)
            for p in range(t):
                newimg[i][p] = 255
    if isShowImage:
        showCV2Image("newimg", newimg)  # 纵轴投影
    # np.set_printoptions(threshold=np.inf)
    # print('new img', newimg)

    #判断投影起终点时，需要加一定的偏差，可能是图片的边界也被当做了一条线
    start = 0#投影起点
    for i in range(rows-5):
        if newimg[i][0] != 0:
            if (newimg[i + 5][0] - newimg[i][0]) != 0:
                continue
            else:
                start = i
                break

    print('start', start)

    end = 0#投影终点
    for i in range(rows-1, 4, -1):
        if newimg[i][0] != 0:
            if (newimg[i - 5][0] - newimg[i][0]) != 0:
                continue
            else:
                end = i
                break
    print('end', end)

    mid = int((start+end)/2)
    #分别求上下两区间内投影量的均值
    count_up = 0
    for i in range(start, mid):
        for j in range(cols):
            if newimg[i][j] != 0:
                count_up += 1
    print('count up', count_up)

    count_down = 0
    for i in range(mid, end+1):
        for j in range(cols):
            if newimg[i][j] != 0:
                count_down += 1
    print('count down', count_down)

    aver_up = int(count_up/mid)
    aver_down = int(count_down/mid)
    print(aver_up, aver_down)

    if aver_up > aver_down:
        print('+90°')
        ang = 90
    elif aver_up < aver_down:
        print('-90°')
        ang = -90

    length = math.sqrt(pow(cols, 2)+pow(rows, 2))

    img = cv2.copyMakeBorder(gray, int((length-rows)/2), int((length-rows)/2), int((length-cols)/2), int((length-cols)/2), cv2.BORDER_CONSTANT, value=(255, 255, 255))
    if isShowImage:
        showCV2Image('img', img)

    rows1, cols1 = img.shape[:2]
    center = (cols1//2, rows1//2)

    transform = cv2.getRotationMatrix2D(center, ang, 1)
    rotate = cv2.warpAffine(img, transform, (cols1, rows1), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    if isShowImage:
        showCV2Image('rotate', rotate)

    x1 = int(cols1 / 2) - int(cols / 2)
    y1 = int(rows1 / 2) - int(rows / 2)
    x2 = int(cols1 / 2) + int(cols / 2)
    y2 = int(rows1 / 2) + int(rows / 2)

    img2 = rotate[x1:x2, y1:y2]
    if isShowImage:
        showCV2Image('img2', img2)