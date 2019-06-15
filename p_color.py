# -*- coding:utf-8 -*-
import cv2
import math
#偏色检测
isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('Johns_Form.jpg')
    lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    if isShowImage:
        showCV2Image('l', l)
        showCV2Image('a', a)
        showCV2Image('b', b)

    rows, cols, _ = lab.shape
    da = a.sum()/(rows*cols)-128#归一化至[-128, 127]
    db = b.sum()/(rows*cols)-128
    hist_a = [0]*256
    hist_b = [0]*256
    for i in range(rows):
        for j in range(cols):
            ta = a[i][j]
            tb = b[i][j]
            hist_a[ta] += 1
            hist_b[tb] += 1
    msqa = 0
    msqb = 0
    for i in range(256):
        msqa += float(abs(i-128-da))*hist_a[i]/(rows*cols)
        msqb += float(abs(i - 128 - db)) * hist_b[i] / (rows * cols)
    d = math.sqrt(da*da + db*db)#平均色度
    m = math.sqrt(msqa*msqa + msqb*msqb)#色度中心距
    k = d/m#偏色因子,综合来说k<=1.5可认为整体图像偏色可能性不大
    print('k=%s'%k)
