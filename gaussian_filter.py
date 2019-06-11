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

    # 需要去除光照的影响
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)#彩色转灰度图
    if isShowImage:
        showCV2Image('gray', gray)
    average = np.mean(gray)#求原图的平均灰度
    rows, cols = gray.shape
    block = 16
    rows_new = int(np.ceil(rows/block))
    cols_new = int(np.ceil(cols/block))#将原图根据block大小，划分为rows_new*cols_new大小的块
    block_image = np.zeros((rows_new, cols_new), dtype=np.float32)#求每一块的灰度均值，构成矩阵
    for r in range(rows_new):
        for c in range(cols_new):
            row_min = r*block
            row_max = (r+1)*block
            if row_max > rows:
                row_max = rows
            colmin = c*block
            colmax = (c+1)*block
            if colmax > cols:
                colmax = cols
            imageROI = gray[row_min:row_max, colmin:colmax]#当前块
            block_mean = np.mean(imageROI)#求每一块的灰度均值
            block_image[r, c] = block_mean#构成矩阵
    block_image = block_image - average#亮度矩阵差
    # INTER_CUBIC 4*4像素邻域的双三次插值
    #将rows_new*cols_new的图像恢复到与原图一样大小
    block_image2 = cv2.resize(block_image, (cols, rows), interpolation=cv2.INTER_CUBIC)
    gray2 = gray.astype(np.float32)
    dst = gray2 - block_image2
    dst = dst.astype(np.uint8)
    dst = cv2.GaussianBlur(dst, (3, 3), 0)
    dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cv2.imwrite('4_1.jpg', dst)
    if isShowImage:
        showCV2Image('dst', dst)

    # 下面进行图像增强操作
    src1 = Image.open('4_1.jpg')  # imread的图像为数组，image其自带的open方法无法处理，mode不对应，open返回一个pil对象

    # 亮度增强
    enh_bri = ImageEnhance.Brightness(src1)
    brightness = 1.5
    gf_brightened = enh_bri.enhance(brightness)
    gf_brightened.show(title='gf_brightened')
    gf_brightened.save('gf_brightened.jpg')

    #对比度增强
    enh_con = ImageEnhance.Contrast(gf_brightened)
    contrast = 25
    gf_contrast = enh_con.enhance(contrast)
    gf_contrast.show(title='gf_contrast')
    gf_contrast.save('gf_contrast.jpg')

    #锐化增强
    enh_sha = ImageEnhance.Sharpness(gf_contrast)
    sharpness = 10.0
    gf_sharped = enh_sha.enhance(sharpness)
    gf_sharped.show(title='gf_sharped')
    gf_sharped.save('gf_sharped.jpg')

    #色度增强
    enh_col = ImageEnhance.Color(gf_sharped)
    color = 1.5
    gf_colored = enh_col.enhance(color)
    gf_colored.show(title='gf_colored')
    gf_colored.save('gf_colored.jpg')




