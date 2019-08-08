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
    image = cv2.imread('d0.png_180.png')
    if isShowImage:
        showCV2Image('input', image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if isShowImage:
        showCV2Image('gray', gray)

    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)#黑纸白字
    if isShowImage:
        showCV2Image('binary', binary)

    rows, cols = binary.shape
    print(rows, cols)
    scale = 20

    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
    if isShowImage:
        showCV2Image("Dilated Image", dilatedrow)

    binary = cv2.bitwise_xor(binary, dilatedrow)
    if isShowImage:
        showCV2Image('binary2', binary)

    #通过投影分析，如果为±90°，则在纵轴投影，若为±180°，则在横轴投影
    #若为+90°，则大部分情况应该是图片上半部分的平均值大于下半部分的
    #若为180°，则右半部较大，0°则左半部较大
    #基于文字的排布，皆是从左到右，但对于论文这种通篇排布紧密，或有表格或公式的情况，容易出错

    newimg = np.zeros((rows, cols), np.uint8)

    #纵轴投影
    #先求和
    rowsum = binary.sum(axis=0)
    # max_value = int(max(rowsum) / 255)
    max_value = []
    for i in range(cols):
        if rowsum[i] == 0:
            for x in range(rows):
                newimg[x][i] = 0
        else:
            t = int(rowsum[i] / 255)
            max_value.append(t)
            for p in range(t):
                newimg[p][i] = 255
            # if t == max_value:
            #     point = i
    maxx = max(max_value)
    print('maxx', max_value)
    point = max_value.index(maxx)
    print('point', point)
    if isShowImage:
        showCV2Image("newimg", newimg)  # 纵轴投影
    # np.set_printoptions(threshold=np.inf)
    # print('new img', newimg)

    #判断投影起终点时，需要加一定的偏差，可能是图片的边界也被当做了一条线
    start = 0#投影起点
    for i in range(cols-5):
        if newimg[0][i] != 0:
            if (newimg[0][i+5] - newimg[0][i]) != 0:
                continue
            else:
                start = i
                break
    print('start', start)

    end = 0#投影终点
    for i in range(cols-1, 4, -1):
        if newimg[0][i] != 0:
            if (newimg[0][i-5] - newimg[0][i]) != 0:
                continue
            else:
                end = i
                break
    print('end', end)

    mid = int((start+end)/2)
    print('mid', mid)
    #分别求上下两区间内投影量的均值
    # count_left = 0
    # for i in range(start, mid):
    #     for j in range(rows):
    #         if newimg[j][i] != 0:
    #             count_left += 1
    # print('count up', count_left)
    #
    # count_right = 0
    # for i in range(mid, end+1):
    #     for j in range(rows):
    #         if newimg[j][i] != 0:
    #             count_right += 1
    # print('count down', count_right)
    #
    # aver_left = int(count_left/mid)
    # aver_right = int(count_right/mid)
    # print(aver_left, aver_right)
    #
    # if aver_left > aver_right:
    #     print('0°')
    #     ang = 0
    # elif aver_left < aver_right:
    #     print('180°')
    #     ang = 180
    if point > start and point <= mid:
        print('0°')
        ang = 0
    elif point > mid and point <= end:
        print('180°')
        ang = 180

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

    img2 = rotate[y1:y2, x1:x2]
    if isShowImage:
        showCV2Image('img2', img2)