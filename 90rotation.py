# -*- coding:utf-8 -*-
import cv2
import numpy as np
import math
#正常和顺时针90度可以搞定，90和-90可以区分了

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    image = cv2.imread('z14_-90.png')
    if isShowImage:
        showCV2Image('input', image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if isShowImage:
        showCV2Image('gray', gray)

    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)#黑纸白字
    if isShowImage:
        showCV2Image('binary', binary)

    canny_edges = cv2.Canny(binary, 50, 150)
    if isShowImage:
        showCV2Image('canny edges', canny_edges)

    kernel = np.ones((15, 15), np.uint8)
    dilation = cv2.dilate(binary, kernel)
    if isShowImage:
        showCV2Image('dilation', dilation)

    #先做膨胀，然后找横线，若为90度，则横线在上部，若为-90度，则横线在下部
    rows, cols = binary.shape
    scale = 8
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(dilation, kernel, iterations=1)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
    if isShowImage:
        showCV2Image("Dilated Image", dilatedcol)

    for i in range(rows):
        for j in range(cols):
            if dilatedcol[i][j] == 255:
                # print('j', j)
                if i < (1/3*rows):#说明在上半部，为90度
                    ang = 90
                elif i >= (2/3*rows):#说明在下半部，为-90度
                    ang = -90
                break
    print('ang', ang)

    # hough_lines = cv2.HoughLinesP(binary, 1, np.pi/180, 200)
    hough_lines = cv2.HoughLines(binary, 1, np.pi / 180, 350)
    lines_shape = hough_lines.shape

    angles = 0#倾斜角度
    for i in range(lines_shape[0]):
        rho = hough_lines[i][0][0]
        theta = hough_lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)

        x0 = a * rho
        y0 = b * rho

        x1 = int(round(x0+1000*(-b)))
        y1 = int(round(y0+1000*a))
        x2 = int(round(x0-1000*(-b)))
        y2 = int(round(y0-1000*a))

        angles += theta

        lines = cv2.line(image, (x1, y1), (x2, y2), (55, 100, 195), 2)
    if isShowImage:
        showCV2Image('linesss', lines)

    average_angles = angles/lines_shape[0]
    angle = average_angles/np.pi*180#检测出的最终角度
    print('angle', angle)

    if abs(angle-90) <= 10:
        final_angle = 0
    elif angle <= 10:
        final_angle = ang
    print('final angle', final_angle)

    rows, cols = gray.shape
    x_c = cols//2
    y_c = rows//2
    length = math.sqrt(pow(cols, 2)+pow(rows, 2))

    img = cv2.copyMakeBorder(gray, int((length-rows)/2), int((length-rows)/2), int((length-cols)/2), int((length-cols)/2), cv2.BORDER_CONSTANT, value=(255, 255, 255))
    if isShowImage:
        showCV2Image('img', img)


    rows1, cols1 = img.shape[:2]
    center = (cols1//2, rows1//2)

    transform = cv2.getRotationMatrix2D(center, final_angle, 1)
    rotate = cv2.warpAffine(img, transform, (cols1, rows1), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    if isShowImage:
        showCV2Image('rotate', rotate)


    x1 = int(cols1 / 2) - int(cols / 2)
    y1 = int(rows1 / 2) - int(rows / 2)
    x2 = int(cols1 / 2) + int(cols / 2)
    y2 = int(rows1 / 2) + int(rows / 2)

    if final_angle == 90 or -90:
        img2 = rotate[x1:x2, y1:y2]
    elif final_angle == 0:
        img2 = rotate[y1:y2, x1:x2]
    if isShowImage:
        showCV2Image('img2', img2)

