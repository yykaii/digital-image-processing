# -*- coding:utf-8 -*-
import cv2
import math
from skimage import filters

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('Johns_Form_copy_equ_hist_s.jpg')
    lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    if isShowImage:
        showCV2Image('l', l)
        showCV2Image('a', a)
        showCV2Image('b', b)

    rows, cols, _ = lab.shape
    da = a.sum()/(rows*cols)-128#归一化至[-128, 127]
    db = b.sum()/(rows*cols)-128
    print('da', da)
    print('db', db)#da>0偏红，否则偏绿；db>0偏黄，否则偏蓝
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
    print('d=%s' % d)
    print('m=%s' % m)

    #矫正
    if k >1.4:#判断是否存在偏色，是否需要矫正
        # 根据a,b均值，判断到底是哪一种偏色
        if abs(da) >abs(db):#偏红绿
            #根据不同的偏色情况，分别采用线性拉伸策略，把a,b的均值等效移位到分布中心附近
            da = da-m+128
            #da = int((da+db)/2)+128
            print('da1', da)
            for i in range(rows):
                for j in range(cols):
                    a[i][j] = da
        else:#偏黄蓝
            db = db-m+128
            # db = int((da+db)/2)+128
            print('db1', db)
            for i in range(rows):
                for j in range(cols):
                    b[i][j] = b[i][j]+(db-d)+128
                    # b[i][j] = b[i][j]-m
    lab1 = cv2.merge([l, a, b])
    src1 = cv2.cvtColor(lab1, cv2.COLOR_LAB2BGR)
    if isShowImage:
        showCV2Image('src1', src1)

    cv2.imwrite('Johns_Form_copy_equ_hist_s1.jpg', src1)




