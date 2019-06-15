# -*- coding:utf-8 -*-
import cv2
import math
import numpy as np
#图像分块偏色检测
isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

def block_split(img, block):
    rows, cols, _ = img.shape
    rows_new = int(np.ceil(rows / block))
    cols_new = int(np.ceil(cols / block))  # 将原图根据block大小，划分为rows_new*cols_new大小的块
    block_image = []
    for r in range(rows_new):
        for c in range(cols_new):
            row_min = r * block
            row_max = (r + 1) * block
            if row_max > rows:
                row_max = rows
            colmin = c * block
            colmax = (c + 1) * block
            if colmax > cols:
                colmax = cols
            imageROI = img[row_min:row_max, colmin:colmax]  # 当前块
            block_image.append(imageROI)
    return rows_new, cols_new, block_image

if __name__ == '__main__':
    src = cv2.imread('Johns_Form.jpg')
    lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)

    rows_new, cols_new, block_image = block_split(lab, block=32)
    K = []
    dab = []
    for i in range(rows_new*cols_new):
        l, a, b = cv2.split(block_image[i])
        rows, cols, _ = block_image[i].shape
        da = a.sum() / (rows * cols) - 128  # 归一化至[-128, 127]
        db = b.sum() / (rows * cols) - 128
        dab.append((da, db))
        hist_a = [0] * 256
        hist_b = [0] * 256
        for i in range(rows):
            for j in range(cols):
                ta = a[i][j]
                tb = b[i][j]
                hist_a[ta] += 1
                hist_b[tb] += 1
        msqa = 0
        msqb = 0
        for i in range(256):
            msqa += float(abs(i - 128 - da)) * hist_a[i] / (rows * cols)
            msqb += float(abs(i - 128 - db)) * hist_b[i] / (rows * cols)
        d = math.sqrt(da * da + db * db)  # 平均色度
        m = math.sqrt(msqa * msqa + msqb * msqb)  # 色度中心距
        k = d / m  # 偏色因子,综合来说k<=1.5可认为整体图像偏色可能性不大
        K.append(k)
    print('dab', dab)#da>0偏红，否则偏绿；db>0偏黄，否则偏蓝
    print('K', K)



