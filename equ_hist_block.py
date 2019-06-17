# -*- coding:utf-8 -*-
import cv2
from PIL import Image
from PIL import ImageEnhance
import remove_light
import numpy as np
from skimage import morphology, measure

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

def block_split(img, block):
    rows, cols, _ = img.shape
    rows_new = int(np.ceil(rows / block))
    cols_new = int(np.ceil(cols / block))
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
    src = cv2.imread('Johns_Form.jpg')#原始图像
    #分离通道

    # bgr_equ_hist = []
    # for i in range(len(bgr)):#直方图均衡化
    #     equ_hist = cv2.equalizeHist(bgr[i])
    #     bgr_equ_hist.append(equ_hist)
    #
    # bgr_equ_merge = cv2.merge(bgr_equ_hist)
    # if isShowImage:
    #     showCV2Image('bgr_equ_merge', bgr_equ_merge)
    # cv2.imwrite('4_2.jpg', bgr_equ_merge)

    rows_new, cols_new, block_image = block_split(src, block=32)
    for i in range(rows_new*cols_new):
        bgr = cv2.split(block_image[i])
        rows, cols, _ = block_image[i].shape

        bgr_adap = []  # 自适应直方图均衡化
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(1024, 1024))
        for j in range(len(bgr)):
            adap_hist = clahe.apply(bgr[j])
            bgr_adap.append(adap_hist)

        bgr_adap_merge = cv2.merge(bgr_adap)
        if isShowImage:
            showCV2Image('bgr_adap_merge', bgr_adap_merge)






    # cv2.imwrite('Johns_form_equhist_b.jpg', bgr_adap_merge)





    # src1 = Image.open('Johns_form_equhist_b.jpg')  # imread的图像为数组，image其自带的open方法无法处理，mode不对应，open返回一个pil对象
    #
    # # 亮度增强
    # enh_bri = ImageEnhance.Brightness(src1)
    # brightness = 1.5
    # gf_brightened = enh_bri.enhance(brightness)
    # gf_brightened.show(title='gf_brightened')
    # # gf_brightened.save('gf_brightened.jpg')
    #
    # #对比度增强
    # enh_con = ImageEnhance.Contrast(gf_brightened)
    # contrast = 1.5
    # gf_contrast = enh_con.enhance(contrast)
    # gf_contrast.show(title='gf_contrast')
    # #gf_contrast.save('gf_contrast.jpg')
    #
    # #锐化增强
    # enh_sha = ImageEnhance.Sharpness(gf_contrast)
    # sharpness = 5.0
    # gf_sharped = enh_sha.enhance(sharpness)
    # gf_sharped.show(title='gf_sharped')
    # #gf_sharped.save('gf_sharped.jpg')
    #
    # #色度增强
    # enh_col = ImageEnhance.Color(gf_sharped)
    # color = 1
    # gf_colored = enh_col.enhance(color)
    # gf_colored.show(title='gf_colored')
    # gf_colored.save('Johns_form_copy_s_pp2.jpg')
