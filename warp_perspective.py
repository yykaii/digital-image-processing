# -*- coding:utf-8 -*-
import cv2
import numpy as np

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('alex_check.jpg')
    if isShowImage:
        showCV2Image('src', src)

    # 灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    rows, cols = gray.shape

    #canny边缘检测
    canny_edges = cv2.Canny(gray, 50, 250)
    if isShowImage:
        showCV2Image('canny', canny_edges)

    #霍夫变换，得到纸的边缘线条
    lines = cv2.HoughLinesP(canny_edges, 1, np.pi/180, 50, minLineLength=90, maxLineGap=10)

    for x1, y1, x2, y2 in lines[0]:
        print(x1, y1), (x2, y2)
    for x1, y1, x2, y2 in lines[1]:
        print(x1, y1), (x2,y2)

    # 绘制边缘
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(src, (x1,y1), (x2,y2), (0,255,0), 1)
        if isShowImage:
            showCV2Image('src', src)
    #根据四个顶点设置图像透视变换矩阵
    pos1 = np.float32([[114, 82], [287, 156], [8, 322], [216, 333]])
    pos2 = np.float32([[0, 0], [188, 0], [0, 262], [188, 262]])
    M = cv2.getPerspectiveTransform(pos1, pos2)
    #图像透视变换
    result = cv2.warpPerspective(src, M, (cols, rows))
    #显示图像
    if isShowImage:
        showCV2Image('reuslt', result)

    cv2.imwrite('wrap_re.jpg', result)

