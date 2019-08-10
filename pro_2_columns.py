# -*- coding:utf-8 -*-
import os
import cv2
import math
import numpy as np
#for 2 columns image
#单纯针对2列的图片较好，但是如果和单列的图片混合，效果反而不好
#本方法是假设峰值在[0,1/4]和[1/2,3/4]部分为0度

def rotate90(image, file):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)  # 黑纸白字

    # 通过投影分析，如果为±90°，则在纵轴投影，若为±180°，则在横轴投影
    # 若为+90°，则大部分情况应该是图片上半部分的平均值大于下半部分的
    # 若为180°，则右半部较大，0°则左半部较大
    # 基于文字的排布，皆是从左到右，但对于论文这种通篇排布紧密，或有表格或公式的情况，容易出错

    rows, cols = binary.shape
    print(rows, cols)

    scale = 20
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)

    binary = cv2.bitwise_xor(binary, dilatedcol)

    newimg = np.zeros((rows, cols), np.uint8)

    # 纵轴投影
    # 先求和
    rowsum = binary.sum(axis=1)
    max_value = int(max(rowsum) / 255)
    print('max', max_value)
    for i in range(rows):
        if rowsum[i] == 0:
            for x in range(cols):
                newimg[i][x] = 0
        else:
            t = int(rowsum[i] / 255)
            for p in range(t):
                newimg[i][p] = 255
            if t == max_value:
                point = i
    print('point', point)

    #保存投影图片
    cv2.imwrite('rotation_test/90_wrong_projectionimage/' + str(file), newimg)

    # 纵轴投影
    # np.set_printoptions(threshold=np.inf)
    # print('new img', newimg)

    # 判断投影起终点时，需要加一定的偏差，可能是图片的边界也被当做了一条线
    start = 0  # 投影起点
    for i in range(rows - 5):
        if newimg[i][0] != 0:
            if (newimg[i + 5][0] - newimg[i][0]) != 0:
                continue
            else:
                start = i
                break
    print('start', start)

    end = 0  # 投影终点
    for i in range(rows - 1, 4, -1):
        if newimg[i][0] != 0:
            if (newimg[i - 5][0] - newimg[i][0]) != 0:
                continue
            else:
                end = i
                break
    print('end', end)

    mid = int((start + end) / 2)
    print('mid', mid)
    quater = int((start + end) / 4)
    print('quater', quater)
    behind = int((start + end) * 3 / 4)
    print('behind', behind)
    # #分别求上下两区间内投影量的均值
    # count_up = 0
    # for i in range(start, mid):
    #     for j in range(cols):
    #         if newimg[i][j] != 0:
    #             count_up += 1
    # print('count up', count_up)
    #
    # count_down = 0
    # for i in range(mid, end+1):
    #     for j in range(cols):
    #         if newimg[i][j] != 0:
    #             count_down += 1
    # print('count down', count_down)
    #
    # aver_up = int(count_up/mid)
    # aver_down = int(count_down/mid)
    # print(aver_up, aver_down)
    #
    # if aver_up > aver_down:
    #     print('+90°')
    #     ang = 90
    # elif aver_up < aver_down:
    #     print('-90°')
    #     ang = -90

    # if point > start and point <= mid:
    #     print('+90°')
    ang = 90
    # if point > mid and point <= end:
    #     print('-90°')
    #     ang = -90
    if (point < mid and point >= quater) or (point <= end and point >= behind):
        print('-90°')
        ang = -90

    length = math.sqrt(pow(cols, 2) + pow(rows, 2))

    img = cv2.copyMakeBorder(gray, int((length - rows) / 2), int((length - rows) / 2), int((length - cols) / 2),
                             int((length - cols) / 2), cv2.BORDER_CONSTANT, value=(255, 255, 255))

    rows1, cols1 = img.shape[:2]
    center = (cols1 // 2, rows1 // 2)

    transform = cv2.getRotationMatrix2D(center, ang, 1)
    rotate = cv2.warpAffine(img, transform, (cols1, rows1), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    x1 = int(cols1 / 2) - int(cols / 2)
    y1 = int(rows1 / 2) - int(rows / 2)
    x2 = int(cols1 / 2) + int(cols / 2)
    y2 = int(rows1 / 2) + int(rows / 2)

    img2 = rotate[x1:x2, y1:y2]

    log = open('rotation_test/90_result_log.txt', 'a+')
    log.write(str(file)+':'+'\n')
    log.write('angle:'+str(ang) +'\n')
    log.write('start:' + str(start) + '\n')
    log.write('quater:' + str(quater) + '\n')
    log.write('mid:' + str(mid) + '\n')
    log.write('behind:' + str(behind) + '\n')
    log.write('end:' + str(end) + '\n')
    log.write('point:' + str(point) +'\n')
    log.write('\n')
    log.close()
    return ang, img2

def rotate180(image, file):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)  # 黑纸白字

    rows, cols = binary.shape
    print(rows, cols)
    scale = 20

    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)

    binary = cv2.bitwise_xor(binary, dilatedrow)

    newimg = np.zeros((rows, cols), np.uint8)

    # 纵轴投影
    # 先求和
    rowsum = binary.sum(axis=0)
    max_value = int(max(rowsum) / 255)
    for i in range(cols):
        if rowsum[i] == 0:
            for x in range(rows):
                newimg[x][i] = 0
        else:
            t = int(rowsum[i] / 255)
            for p in range(t):
                newimg[p][i] = 255
            if t == max_value:
                point = i
    print('point', point)

    #保存投影图片
    cv2.imwrite('rotation_test/180_wrong_projectionimage/' + str(file), newimg)

    # 纵轴投影
    # np.set_printoptions(threshold=np.inf)
    # print('new img', newimg)

    # 判断投影起终点时，需要加一定的偏差，可能是图片的边界也被当做了一条线
    start = 0  # 投影起点
    for i in range(cols - 5):
        if newimg[0][i] != 0:
            if (newimg[0][i + 5] - newimg[0][i]) != 0:
                continue
            else:
                start = i
                break
    print('start', start)

    end = 0  # 投影终点
    for i in range(cols - 1, 4, -1):
        if newimg[0][i] != 0:
            if (newimg[0][i - 5] - newimg[0][i]) != 0:
                continue
            else:
                end = i
                break
    print('end', end)

    mid = int((start + end) /2)
    print('mid', mid)
    quater = int((start + end) / 4)
    print('quater', quater)
    behind = int((start + end) *3/ 4)
    print('behind', behind)

    # 分别求上下两区间内投影量的均值
    # count_left = 0
    # for i in range(start, mid):
    #     for j in range(rows):
    #         if newimg[j][i] != 0:
    #             count_left += 1
    # print('count up', count_left)
    #
    # count_right = 0
    # for i in range(mid, end + 1):
    #     for j in range(rows):
    #         if newimg[j][i] != 0:
    #             count_right += 1
    # print('count down', count_right)
    #
    # aver_left = int(count_left / mid)
    # aver_right = int(count_right / mid)
    # print(aver_left, aver_right)
    #
    # if aver_left > aver_right:
    #     print('0°')
    #     ang = 0
    # elif aver_left < aver_right:
    #     print('180°')
    #     ang = 180

    # if point > start and point <= mid:
    #     print('0°')
    #单峰值，考虑最大值在左侧为正
    # ang = 0
    # if point > mid and point <= end:
    #     print('180°')
    #     ang = 180
    #
    #2列的情况，需考虑双峰值，峰值有可能在左侧，有可能在右侧
    # if (point > start and point <= quater) or (point >= mid and point < behind):
    ang = 0
    if (point < mid and point >= quater) or (point <= end and point >= behind):
        print('180°')
        ang = 180

    length = math.sqrt(pow(cols, 2) + pow(rows, 2))

    img = cv2.copyMakeBorder(gray, int((length - rows) / 2), int((length - rows) / 2), int((length - cols) / 2),
                             int((length - cols) / 2), cv2.BORDER_CONSTANT, value=(255, 255, 255))

    rows1, cols1 = img.shape[:2]
    center = (cols1 // 2, rows1 // 2)

    transform = cv2.getRotationMatrix2D(center, ang, 1)
    rotate = cv2.warpAffine(img, transform, (cols1, rows1), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


    x1 = int(cols1 / 2) - int(cols / 2)
    y1 = int(rows1 / 2) - int(rows / 2)
    x2 = int(cols1 / 2) + int(cols / 2)
    y2 = int(rows1 / 2) + int(rows / 2)

    img2 = rotate[y1:y2, x1:x2]
    log = open('rotation_test/180_result_log.txt', 'a+')
    log.write(str(file) + ':' + '\n')
    log.write('angle:' + str(ang) + '\n')
    log.write('start:' + str(start) + '\n')
    log.write('quater:' + str(quater) + '\n')
    log.write('mid:' + str(mid) + '\n')
    log.write('behind:' + str(behind) + '\n')
    log.write('end:' + str(end) + '\n')
    log.write('point:' + str(point) + '\n')
    log.write('\n')
    log.close()
    return ang, img2


if __name__ == '__main__':
    # relevant_path = "rotation_test/90_/"
    relevant_path = "rotation_test/180_/"
    included_extensions = ['jpg', 'jpeg', 'bmp', 'png', 'gif']
    file_names = [fn for fn in os.listdir(relevant_path)
                  if any(fn.endswith(ext) for ext in included_extensions)]

    for file in file_names:
        # file1 = open('rotation_test/90_result.txt', 'a+')
        file1 = open('rotation_test/180_result.txt', 'a+')
        print('file name', file)
        image = cv2.imread(relevant_path + file, 1)
        # ang, img2 = rotate90(image, file)
        ang, img2 = rotate180(image, file)
        # cv2.imwrite('rotation_test/90_r_2c/'+str(file)+'_r.png', img2)
        cv2.imwrite('rotation_test/180_r_2c/' + str(file) + '_r.png', img2)
        file1.write(str(file)+':'+str(ang) + '\n')
        file1.close()






