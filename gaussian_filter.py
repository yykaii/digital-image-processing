# -*- coding:utf-8 -*-
import cv2
from PIL import Image
from PIL import ImageEnhance, ImageFilter
import numpy as np


isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('4.jpeg')#原始图像
    # (b, g, r) = cv2.split(src)#分离通道
    # if isShowImage:
    #     showCV2Image('src_b', b)
    #     showCV2Image('src_g', g)
    #     showCV2Image('src_r', r)

    # gf = cv2.merge([gf_b, gf_g, gf_r])#通道合并
    # if isShowImage:
    #     showCV2Image('gf', gf)

    #图像归一化
    # [rows, cols, depth] = src.shape
    # dst = np.zeros([rows, cols, depth], dtype='uint8')
    # dst = cv2.normalize(src, dst=dst, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    # if isShowImage:
    #     showCV2Image('dst_b', dst)

    #下面进行图像增强操作
    src1 = Image.open('4.jpg')#imread的图像为数组，image其自带的open方法无法处理，mode不对应，open返回一个pil对象

    # 需要去除光照的影响
    

    # # 亮度增强
    # enh_bri = ImageEnhance.Brightness(src1)
    # brightness = 1.5
    # gf_brightened = enh_bri.enhance(brightness)
    # gf_brightened.show(title='gf_brightened')
    # gf_brightened.save('gf_brightened.jpg')
    #
    # #对比度增强
    # enh_con = ImageEnhance.Contrast(gf_brightened)
    # contrast = 1.5
    # gf_contrast = enh_con.enhance(contrast)
    # gf_contrast.show(title='gf_contrast')
    # gf_contrast.save('gf_contrast.jpg')
    #
    # #锐化增强
    # enh_sha = ImageEnhance.Sharpness(gf_contrast)
    # sharpness = 3.0
    # gf_sharped = enh_sha.enhance(sharpness)
    # gf_sharped.show(title='gf_sharped')
    # gf_sharped.save('gf_sharped.jpg')
    #
    # #色度增强
    # enh_col = ImageEnhance.Color(gf_sharped)
    # color = 1.5
    # gf_colored = enh_col.enhance(color)
    # gf_colored.show(title='gf_colored')
    # gf_colored.save('gf_colored.jpg')




