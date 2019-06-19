# -*- coding:utf-8 -*-
import cv2
import numpy as np
from skimage import measure, color,morphology


isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    #原图
    src = cv2.imread('chart_contrast.jpg')
    if isShowImage:
        showCV2Image('src', src)
    #灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    if isShowImage:
        showCV2Image('gray', gray)
    #二值化
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
    if isShowImage:
        showCV2Image('binary', binary)

    #腐蚀/膨胀
    kernel = np.ones((5, 5), np.uint8)
    #
    # # 填洞，先膨胀再腐蚀，闭运算
    # src1 = cv2.erode(src, kernel=kernel)
    # if isShowImage:
    #     showCV2Image('src1', src1)
    #
    # src2 = cv2.dilate(src1, kernel=kernel)
    # if isShowImage:
    #     showCV2Image('src2', src2)
    # cv2.imwrite('c1_e_d.jpg', src2)

    # 消除小区域，先腐蚀再膨胀，开运算
    # dilation = cv2.dilate(binray, kernel=kernel)
    # if isShowImage:
    #     showCV2Image('dilation', dilation)
    #
    # erodation = cv2.erode(dilation, kernel=kernel)
    # if isShowImage:
    #     showCV2Image('erodation', erodation)

    #利用连通域消除小区域
    # labels, nums = measure.label(erodation, connectivity=2, return_num=True)
    # props = measure.regionprops(labels)
    # print(labels.shape)
    # print(labels)
    # areas = []
    # for i in range(nums):
    #     areas.append(props[i]['area'])
    # print('areas', areas)
    # max_value = max(areas)
    # print('max_value', max_value)
    # image = morphology.remove_small_objects(labels, min_size=1, connectivity=1)  # 去除小的连通域
    # cv2.imwrite('remove_area.jpg', image)

    #识别横竖线，并消除
    rows, cols = binary.shape
    scale = 20
    # 识别横线
    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(binary, kernel_h, iterations=1)
    dilatedcol = cv2.dilate(eroded, kernel_h, iterations=1)
    if isShowImage:
        showCV2Image("Dilated Image", dilatedcol)

    # 识别竖线
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(binary, kernel_v, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel_v, iterations=1)
    if isShowImage:
        showCV2Image("Dilated Image", dilatedrow)



    # 识别表格线
    table = cv2.bitwise_or(dilatedcol, dilatedrow)
    if isShowImage:
        showCV2Image("table line", table)

    # 去掉表格线
    no_tab_line = cv2.bitwise_xor(binary, table)
    if isShowImage:
        showCV2Image("no table line", no_tab_line)

    # erode1 = cv2.erode(no_tab_line, kernel)
    # if isShowImage:
    #     showCV2Image("erode1", erode1)

    # d = cv2.bitwise_xor(erode1, binary)
    # if isShowImage:
    #     showCV2Image('d', d)

    kernel_d = np.ones((13, 13), np.uint8)
    dilation1 = cv2.dilate(binary, kernel)
    if isShowImage:
        showCV2Image("dilation1", dilation1)

    # # 黑白反色
    # n_tab_line = cv2.bitwise_not(no_tab_line)
    # if isShowImage:
    #     showCV2Image("n_table line", n_tab_line)










