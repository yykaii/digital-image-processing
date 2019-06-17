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

def image_enhancement(img):
    # 亮度增强
    enh_bri = ImageEnhance.Brightness(img)
    brightness = 1.5
    gf_brightened = enh_bri.enhance(brightness)
    gf_brightened.show(title='gf_brightened')
    # gf_brightened.save('Johns_check_brightened1.jpg')

    #对比度增强
    enh_con = ImageEnhance.Contrast(gf_brightened)
    contrast = 1.5
    gf_contrast = enh_con.enhance(contrast)
    gf_contrast.show(title='gf_contrast')
    # gf_contrast.save('Johns_check_contrast.jpg')

    #锐化增强
    enh_sha = ImageEnhance.Sharpness(gf_contrast)
    sharpness = 0.5
    gf_sharped = enh_sha.enhance(sharpness)
    gf_sharped.show(title='gf_sharped')
    gf_sharped.save('Johns_form_copy_s_pp_cb_ie.jpg')

    #色度增强
    # enh_col = ImageEnhance.Color(gf_sharped)
    # color = 2
    # gf_colored = enh_col.enhance(color)
    # gf_colored.show(title='gf_colored')
    # gf_colored.save('Johns_DL_colored.jpg')

    return gf_contrast

if __name__ == '__main__':

    # 下面进行图像增强操作
    src1 = Image.open('Johns_form_copy_s_pp_cb.jpg')  # imread的图像为数组，image其自带的open方法无法处理，mode不对应，open返回一个pil对象
    img = image_enhancement(src1)
    #cv2.imwrite('Johns_form_copy_s_p_cb_ie.jpg', img)





