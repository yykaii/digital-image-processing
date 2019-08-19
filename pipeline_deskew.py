# -*- coding:utf-8 -*-
import numpy as np
import cv2
import os
import math
import copy

isShowImage = True
def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

def angle_detect(gray, file):
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    print('origin angle', angle)

    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle

    if angle < -45:
        angle = -(90 + angle)
        # otherwise, just take the inverse of the angle to make
        # it positive
    else:
        angle = -angle

    print("[INFO] angle：", angle)

    log = open('deskew_pipeline/log.txt', 'a+')
    log.write(str(file) + ':' + '\n')
    log.write('deskew angle: ' + str(angle) + '\n')
    log.close()

    return angle

def deskew(angle, image):
    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    rotated = cv2.warpAffine(image, M, (w, h), borderValue=(255, 255, 255))
    # draw the correction angle on the image so we can validate it
    # cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return rotated

def rotate90(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
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

    #保存投影图片
    # cv2.imwrite('rotation_test/pro_judge_2/90_wrong_projectionimage/' + str(file), newimg)

    # 判断投影起终点时，需要加一定的偏差，可能是图片的边界也被当做了一条线
    start = 0  # 投影起点
    for i in range(rows - 5):
        if newimg[i][0] != 0:
            if (newimg[i + 5][0] - newimg[i][0]) != 0:
                continue
            else:
                start = i
                break


    end = 0  # 投影终点
    for i in range(rows - 1, 4, -1):
        if newimg[i][0] != 0:
            if (newimg[i - 5][0] - newimg[i][0]) != 0:
                continue
            else:
                end = i
                break

    mid = int((start + end) / 2)
    quater = int((start + end) / 4)
    behind = int((start + end) * 3 / 4)

    #先判断是单列还是双列，若为双列，则图片中间位置投影量为0（此处给与偏移量20）
    #但是对于论文来说，可能部分双列，图表可能在页面的中间，会有影响
    mid_value = int(rowsum[int(len(rowsum)/2)]/255)
    ang = 90
    if mid_value > 20:#单列
        if point > mid and point <= end:
            print('-90°')
            ang = -90
    else:#双列
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

    log = open('deskew_pipeline/log.txt', 'a+')
    log.write('rotation90 angle: ' + str(ang) + '\n')
    log.close()
    return ang, img2

def rotate180(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2:
        gray = image
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
    # print('point', point)

    #保存投影图片
    # cv2.imwrite('rotation_test/pro_judge_2/180_wrong_projectionimage/' + str(file), newimg)

    # 判断投影起终点时，需要加一定的偏差，可能是图片的边界也被当做了一条线
    start = 0  # 投影起点
    for i in range(cols - 5):
        if newimg[0][i] != 0:
            if (newimg[0][i + 5] - newimg[0][i]) != 0:
                continue
            else:
                start = i
                break

    end = 0  # 投影终点
    for i in range(cols - 1, 4, -1):
        if newimg[0][i] != 0:
            if (newimg[0][i - 5] - newimg[0][i]) != 0:
                continue
            else:
                end = i
                break

    mid = int((start + end) /2)
    quater = int((start + end) / 4)
    behind = int((start + end) *3/ 4)

    mid_value = int(rowsum[int(len(rowsum) / 2)] / 255)
    ang = 0
    if mid_value > 20:  # 单列
        if point > mid and point <= end:
            print('180°')
            ang = 180
    else:  # 双列
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

    log = open('deskew_pipeline/log.txt', 'a+')
    log.write('rotation180 angle: ' + str(ang) + '\n')
    log.close()

    return ang, img2

def hough(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)  # 黑纸白字

    hough_lines = cv2.HoughLines(binary, 1, np.pi / 180, 400)
    lines_shape = hough_lines.shape

    angles = 0  # 倾斜角度
    line_num = lines_shape[0]
    for i in range(line_num):
        rho = hough_lines[i][0][0]
        theta = hough_lines[i][0][1]
        # print('line theta', theta)
        a = math.cos(theta)
        b = math.sin(theta)

        x0 = a * rho
        y0 = b * rho

        x1 = int(round(x0 + 1000 * (-b)))
        y1 = int(round(y0 + 1000 * a))
        x2 = int(round(x0 - 1000 * (-b)))
        y2 = int(round(y0 - 1000 * a))

        angles += theta

        lines = cv2.line(image, (x1, y1), (x2, y2), (55, 100, 195), 2)
    if isShowImage:
        showCV2Image('lines', lines)

    print('hough angle', angles)
    return angles, line_num

if __name__ == '__main__':
    # relevant_path = "baca_test180/"
    # included_extensions = ['jpg', 'jpeg', 'bmp', 'png', 'gif']
    # file_names = [fn for fn in os.listdir(relevant_path)
    #               if any(fn.endswith(ext) for ext in included_extensions)]

    # for file in file_names:
    file = 'image_enhancement/1.png'
    image = cv2.imread(file)
    if isShowImage:
        showCV2Image('image', image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    angle = angle_detect(gray, file)
    # angle = math.ceil(angle)

    img = deskew(angle, image)
    img3 = copy.deepcopy(img)
    if isShowImage:
        showCV2Image('img', img)

    # deskew只能返回-90°到0°之间的角度，所以后续还需跟上±90°和180°的检测
    # 但需要判断，如果是转正了的图片，再送去转90°，可能会错

    angle0, line_num = hough(img)
    angles = int(angle0 / line_num)

    print('angle0', angle0, line_num)
    print('angles', angles)
    # angle0 = math.ceil(angle0)

    #第一种判断方法，以80°为分界线，将deskew检测的角度与hough变换检测的角度求和与90°做差，若小于10°，则直接进行180度判断
    if angle0 <= 1:
        angle1, img1 = rotate90(img3)
        if isShowImage:
            showCV2Image('img1', img1)
        angle2, img2 = rotate180(img1)
        if isShowImage:
            showCV2Image('img2', img2)
        final_angle = angle + angle2 + angle1
        print('angle2', angle2)
        print('final angle', final_angle)
    else:
        angle2, img2 = rotate180(img3)
        if isShowImage:
            showCV2Image('img2', img2)
        final_angle = angle + angle2
        print('angle2', angle2)
        print('final angle', final_angle)

    log = open('deskew_pipeline/log.txt', 'a+')
    log.write('final angle: ' + str(final_angle) + '\n')
    log.write('\n')
    log.close()

    cv2.imwrite('deskew_pipeline/1_15_deskewed.png', img2)



