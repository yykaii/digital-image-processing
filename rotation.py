# -*- coding:utf-8 -*-
import cv2
import math
import numpy as np
import os

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

def rotation(src):

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # if isShowImage:
    #     showCV2Image('gray', gray)

    rows, cols = gray.shape

    #以对角线的长度，为原图加边框，防止旋转后图片不能完整展示
    dia_length = int(math.sqrt(rows*rows+cols*cols))

    img_ex = cv2.copyMakeBorder(src, int((dia_length-rows)/2), int((dia_length-rows)/2), int((dia_length-cols)/2), int((dia_length-cols)/2), cv2.BORDER_CONSTANT, value=(255, 255, 255))
    # if isShowImage:
    #     showCV2Image('img_ex', img_ex) #加了边框的图

    rows1, cols1 = img_ex.shape[:2]
    center = (cols1//2, rows1//2)#寻找质心，即旋转中心

    rotate = cv2.getRotationMatrix2D(center, -90, 1)#旋转转换矩阵，第三个参数是缩放系数，1表示保持原图大小
    img_ex_rotate = cv2.warpAffine(img_ex, rotate, (cols1, rows1))
    # if isShowImage:
    #     showCV2Image('img_rotate', img_ex_rotate)

    x1 = cols1 // 2 - cols // 2
    y1 = rows1 // 2 - rows // 2
    x2 = cols1 // 2 + cols // 2
    y2 = rows1 // 2 + rows // 2

    img2 = img_ex_rotate[x1:x2, y1:y2]
    # if isShowImage:
    #     showCV2Image('img2', img2)

    return img_ex_rotate
    # cv2.imwrite('r0_90.png', img_ex_rotate)

if __name__ == '__main__':
    relevant_path = "rotation_test/"
    included_extensions = ['jpg', 'jpeg', 'bmp', 'png', 'gif']
    file_names = [fn for fn in os.listdir(relevant_path)
                  if any(fn.endswith(ext) for ext in included_extensions)]

    for file in file_names:
        image = cv2.imread(relevant_path + file, 1)
        img_ex_rotate = rotation(image)
        cv2.imwrite(str(file)+'_-90.png', img_ex_rotate)


     # src = cv2.imread('rotation_test/c10.png')
     # img_ex_rotate = rotation(src)
     # cv2.imwrite('0_180.png', img_ex_rotate)


