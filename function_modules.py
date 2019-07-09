# -*- coding:utf-8 -*-
import cv2
from skimage import exposure
import numpy as np
import copy
import math

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

#灰度图
def gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # if isShowImage:
    #     showCV2Image('gray', gray)
    # cv2.imwrite('Johns_DL_contrast_gray.jpg', gray)
    return gray

#gamma校正，输入必须为灰度图
def gamma(grey):
    gamma = exposure.adjust_gamma(grey, gamma=2.5)
    # if isShowImage:
    #     showCV2Image('gamma', gamma)
    # cv2.imwrite('Johns_DL_contrast_gamma2.5.jpg', gamma)
    return gamma

#直方图均衡化
def bgr_equ_hist(image):
    bgr = cv2.split(image)#分离通道
    bgr_equ_hists = []
    for i in range(len(bgr)):#直方图均衡化
        equ_hist = cv2.equalizeHist(bgr[i])
        bgr_equ_hists.append(equ_hist)

    bgr_equ_merge = cv2.merge(bgr_equ_hists)
    # if isShowImage:
    #     showCV2Image('bgr_equ_merge', bgr_equ_merge)
    # cv2.imwrite('4_2.jpg', bgr_equ_merge)
    return bgr_equ_merge

#自适应直方图均衡化
def bgr_adap(image):
    bgr = cv2.split(image)  # 分离通道
    bgr_adaps = []#自适应直方图均衡化
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(32, 32))
    for i in range(len(bgr)):
        adap_hist = clahe.apply(bgr[i])
        bgr_adaps.append(adap_hist)

    bgr_adap_merge = cv2.merge(bgr_adaps)
    # if isShowImage:
    #     showCV2Image('bgr_adap_merge', bgr_adap_merge)
    # cv2.imwrite('c1_contrast1.jpg', bgr_adap_merge)
    return bgr_adap_merge

#去除光照，输入为灰度图
def removelight(gray, block):
    average = np.mean(gray)  # 求原图的平均灰度
    rows, cols = gray.shape
    rows_new = int(np.ceil(rows / block))
    cols_new = int(np.ceil(cols / block))  # 将原图根据block大小，划分为rows_new*cols_new大小的块
    block_image = np.zeros((rows_new, cols_new), dtype=np.float32)  # 求每一块的灰度均值，构成矩阵
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
            imageROI = gray[row_min:row_max, colmin:colmax]  # 当前块
            block_mean = np.mean(imageROI)  # 求每一块的灰度均值
            block_image[r, c] = block_mean  # 构成矩阵
    block_image = block_image - average  # 亮度矩阵差
    # INTER_CUBIC 4*4像素邻域的双三次插值
    # 将rows_new*cols_new的图像恢复到与原图一样大小
    block_image2 = cv2.resize(block_image, (cols, rows), interpolation=cv2.INTER_CUBIC)
    gray2 = gray.astype(np.float32)
    dst = gray2 - block_image2
    dst = dst.astype(np.uint8)
    dst = cv2.GaussianBlur(dst, (3, 3), 0)
    return dst

#色彩均衡
def color_balance(image):
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 彩色转灰度图
    rows, cols = grey.shape
    bgr = cv2.split(image)
    gray_mean = []
    for i in range(len(bgr)):
        gray_mean.append(np.mean(bgr[i]))  # 各通道的灰度值
    gray_aver = np.sum(gray_mean) / 3  # 整个图片的平均灰度值

    # 调整每个像素的bgr值，使其与平均灰度值接近
    times = []
    for i in range(len(bgr)):
        times.append(gray_aver / gray_mean[i])

    bgr1 = copy.deepcopy(bgr)
    for i in range(len(bgr)):
        for j in range(rows):
            for s in range(cols):
                bgr1[i][j][s] = bgr[i][j][s] * times[i]

    # 调整像素到可示范区间
    max1 = []
    new = copy.deepcopy(bgr1)
    for i in range(len(new)):
        maxmax = np.array(new[i]).flatten()
        mm = max(maxmax)
        max1.append(mm)
    max1.sort()
    factor = max1[-1] / 255
    if factor > 1:
        bgr1 = bgr1 / factor

    img = cv2.merge(bgr1)
    return img
    # if isShowImage:
    #     showCV2Image('img', img)

#偏色校正
def p_color_correction(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # if isShowImage:
    #     showCV2Image('l', l)
    #     showCV2Image('a', a)
    #     showCV2Image('b', b)

    rows, cols, _ = lab.shape
    da = a.sum() / (rows * cols) - 128  # 归一化至[-128, 127]
    db = b.sum() / (rows * cols) - 128
    # print('da', da)
    # print('db', db)
    # da>0偏红，否则偏绿；db>0偏黄，否则偏蓝
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

    # 矫正
    if k > 1.4:  # 判断是否存在偏色，是否需要矫正
        # 根据a,b均值，判断到底是哪一种偏色
        if abs(da) > abs(db):  # 偏红绿
            # 根据不同的偏色情况，分别采用线性拉伸策略，把a,b的均值等效移位到分布中心附近
            da = da - m + 128
            # da = int((da+db)/2)+128
            for i in range(rows):
                for j in range(cols):
                    a[i][j] = da
        else:  # 偏黄蓝
            db = db - m + 128
            # db = int((da+db)/2)+128
            for i in range(rows):
                for j in range(cols):
                    b[i][j] = b[i][j] + (db - d) + 128
                    # b[i][j] = b[i][j]-m
    lab1 = cv2.merge([l, a, b])
    src1 = cv2.cvtColor(lab1, cv2.COLOR_LAB2BGR)
    # if isShowImage:
    #     showCV2Image('src1', src1)
    # cv2.imwrite('Johns_Form_copy_equ_hist_s1.jpg', src1)
    return src1

#bit平面分层，起到图像压缩和去除部分背景的作用
def bit_layer_split(grey):
    rows, cols = grey.shape

    # 比特分层
    # 将每个灰度像素十进制转为八位二进制
    bits = np.zeros((rows, cols, 8), np.uint8)
    for i in range(rows):
        for j in range(cols):
            # bits[i][j] = '{:08b}'.format(gray[i][j])
            tmp = list('{:08b}'.format(grey[i][j]))
            for s in range(8):
                bits[i][j][s] = int(tmp[s])

    # 分离为8层
    layers = []
    for i in range(8):
        layer = np.zeros((rows, cols), np.uint8)
        layer1 = np.zeros((rows, cols), np.uint8)
        for j in range(rows):
            for k in range(cols):
                # 此处为了突出显示，将平面值为1的用255代替
                if bits[j][k][i] > 0:
                    layer[j][k] = 255
                layer1[j][k] = bits[j][k][i]
        # if isShowImage:
        #     showCV2Image('layers' + str(i), layer)
        layers.append(layer1)

    # 层面重建，4个高层的比特面即可很好重建，乘以对应层数的2的幂次
    reconstruct = np.zeros((rows, cols), np.uint8)
    for j in range(rows):
        for k in range(cols):
            tmp = 0
            for i in range(4):
                tmp += bits[j][k][i] * pow(2, 8 - i)
            reconstruct[j][k] = tmp
    # if isShowImage:
    #     showCV2Image('re', reconstruct)
    # cv2.imwrite('chart_4_bit.jpg', reconstruct)
    return reconstruct

#空洞填充
def hole_filling(grey):
    binary = cv2.adaptiveThreshold(~grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -10)
    # if isShowImage:
    #     showCV2Image('binary', binary)

    binary1 = cv2.adaptiveThreshold(~grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, -10)
    # if isShowImage:
    #     showCV2Image('binary1', binary1)

    a = cv2.bitwise_xor(grey, binary1)
    # if isShowImage:
    #     showCV2Image('a', a)

    # a反色
    a1 = cv2.bitwise_not(a)
    # if isShowImage:
    #     showCV2Image('a1', a1)
    # cv2.imwrite('APT003_a1.jpg', a1)  # 需要反色的区域

    rows, cols = binary.shape
    mask = np.zeros((rows + 2, cols + 2), np.uint8)
    cv2.floodFill(a, mask, (0, 0), 255)
    # if isShowImage:
    #     showCV2Image('fill', a)

    scale = 20
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
    # if isShowImage:
    #     showCV2Image("Dilated Image", dilatedcol)

    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
    # if isShowImage:
    #     showCV2Image("Dilated Image", dilatedrow)

    # 识别表格线
    table = cv2.bitwise_or(dilatedcol, dilatedrow)
    # if isShowImage:
    #     showCV2Image("table line", table)

    # 去掉表格线
    no_tab_line = cv2.bitwise_xor(binary, table)
    # if isShowImage:
    #     showCV2Image("no table line", no_tab_line)

    # 黑白反色
    n_tab_line = cv2.bitwise_not(no_tab_line)
    # if isShowImage:
    #     showCV2Image("n_table line", n_tab_line)

    # cv2.imwrite('APT003_a2.jpg', n_tab_line)  # 去线后的图

#     src = a1
#         cv2.imread('APT003_a1.jpg', cv2.IMREAD_GRAYSCALE)  # 直接返回一个灰度图
#     if isShowImage:
#         showCV2Image('src', src)
#
#     src1 = \
#         n_tab_line
# cv2.imread('APT003_a2.jpg', cv2.IMREAD_GRAYSCALE)
#     if isShowImage:
#         showCV2Image('src1', src1)

    th, im_th = cv2.threshold(a1, 220, 255, cv2.THRESH_BINARY_INV)
    h, w = im_th.shape

    im_floodfill = im_th.copy()

    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)

    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    im_out = im_th | im_floodfill_inv

    out = cv2.bitwise_xor(im_floodfill, n_tab_line)
    # if isShowImage:
    #     showCV2Image('out1', out)

    final_out = cv2.bitwise_not(out)
    # if isShowImage:
    #     showCV2Image('f_out', final_out)
    #
    # cv2.imwrite('APT003_out.jpg', final_out)
    return final_out
