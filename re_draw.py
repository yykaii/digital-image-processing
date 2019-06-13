# -*- coding:utf-8 -*-
import cv2
import numpy as np
from skimage import exposure
from remove_light import removelight, image_enhancement
from PIL import Image
from PIL import ImageEnhance


isShowImage = True
def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)


def adap_hist(img):
    bgr = cv2.split(img)
    bgr_adap = []  # 自适应直方图均衡化
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(32, 32))
    for i in range(len(bgr)):
        adap_hist = clahe.apply(bgr[i])
        bgr_adap.append(adap_hist)

    bgr_adap_merge = cv2.merge(bgr_adap)
    if isShowImage:
        showCV2Image('bgr_adap_merge', bgr_adap_merge)
    # cv2.imwrite('Johns_Form_2.jpg', bgr_adap_merge)

    return bgr_adap_merge

def removelight(img, block):
    average = np.mean(img)  # 求原图的平均灰度
    rows, cols = img.shape
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
            imageROI = img[row_min:row_max, colmin:colmax]  # 当前块
            block_mean = np.mean(imageROI)  # 求每一块的灰度均值
            block_image[r, c] = block_mean  # 构成矩阵
    block_image = block_image - average  # 亮度矩阵差
    # INTER_CUBIC 4*4像素邻域的双三次插值
    # 将rows_new*cols_new的图像恢复到与原图一样大小
    block_image2 = cv2.resize(block_image, (cols, rows), interpolation=cv2.INTER_CUBIC)
    gray2 = img.astype(np.float32)
    dst = gray2 - block_image2
    dst = dst.astype(np.uint8)
    dst = cv2.GaussianBlur(dst, (3, 3), 0)
    return dst

def image_enhancement(img):
    # 亮度增强
    enh_bri = ImageEnhance.Brightness(img)
    brightness = 1.3
    gf_brightened = enh_bri.enhance(brightness)
    gf_brightened.show(title='gf_brightened')
    gf_brightened.save('Johns_check_brightened1.jpg')

    #对比度增强
    enh_con = ImageEnhance.Contrast(gf_brightened)
    contrast = 1.3
    gf_contrast = enh_con.enhance(contrast)
    gf_contrast.show(title='gf_contrast')
    gf_contrast.save('Johns_check_contrast.jpg')

    # #锐化增强
    # enh_sha = ImageEnhance.Sharpness(gf_contrast)
    # sharpness = 0.5
    # gf_sharped = enh_sha.enhance(sharpness)
    # gf_sharped.show(title='gf_sharped')
    # # gf_sharped.save('gf_sharped.jpg')
    #
    #色度增强
    enh_col = ImageEnhance.Color(gf_contrast)
    color = 2
    gf_colored = enh_col.enhance(color)
    gf_colored.show(title='gf_colored')
    gf_colored.save('Johns_DL_colored.jpg')

    return gf_contrast

