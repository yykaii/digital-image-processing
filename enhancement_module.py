# -*- coding:utf-8 -*-
import cv2
from PIL import Image
from PIL import ImageEnhance
import numpy as np

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

# 亮度增强
def brightness(img):
    enh_bri = ImageEnhance.Brightness(img)
    brightness = 1.5
    gf_brightened = enh_bri.enhance(brightness)
    gf_brightened.show(title='gf_brightened')
    gf_brightened.save('c1_brightened.jpg')
    return gf_brightened

#对比度增强
def contrast(img):
    enh_con = ImageEnhance.Contrast(img)
    contrast = 2.5
    gf_contrast = enh_con.enhance(contrast)
    gf_contrast.show(title='gf_contrast')
    gf_contrast.save('c1_contrast.jpg')
    return gf_contrast

#锐化增强
def sharpness(img):
    enh_sha = ImageEnhance.Sharpness(img)
    sharpness = 1.5
    gf_sharped = enh_sha.enhance(sharpness)
    gf_sharped.show(title='gf_sharped')
    gf_sharped.save('c1_sharp.jpg')
    return gf_sharped

#色度增强
def color(img):
    enh_col = ImageEnhance.Color(img)
    color = 2
    gf_colored = enh_col.enhance(color)
    gf_colored.show(title='gf_colored')
    gf_colored.save('c1_colored.jpg')
    return gf_colored

if __name__ == '__main__':
    # imread的图像为数组，image其自带的open方法无法处理，mode不对应，open返回一个pil对象
    #所以必须用open的方法打开图片
    src1 = Image.open('c1.jpg')







