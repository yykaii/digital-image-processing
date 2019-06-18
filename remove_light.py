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
    brightness = 1.5
    gf_brightened = enh_bri.enhance(brightness)
    gf_brightened.show(title='gf_brightened')
    # gf_brightened.save('Johns_check_brightened1.jpg')

    #对比度增强
    enh_con = ImageEnhance.Contrast(gf_brightened)
    contrast = 2
    gf_contrast = enh_con.enhance(contrast)
    gf_contrast.show(title='gf_contrast')
    # gf_contrast.save('Johns_check_contrast.jpg')

    #锐化增强
    enh_sha = ImageEnhance.Sharpness(gf_contrast)
    sharpness = 2
    gf_sharped = enh_sha.enhance(sharpness)
    gf_sharped.show(title='gf_sharped')
    gf_sharped.save('chart_4.jpg')
    #
    #色度增强
    # enh_col = ImageEnhance.Color(gf_contrast)
    # color = 2
    # gf_colored = enh_col.enhance(color)
    # gf_colored.show(title='gf_colored')
    # gf_colored.save('Johns_DL_colored.jpg')

    return gf_contrast

if __name__ == '__main__':
    src = cv2.imread('Johns_Form.jpg')#原始图像

    # (b, g, r) = cv2.split(src)#分离通道
    # gf = cv2.merge([b, g, r])#通道合并

    #图像归一化
    #若光照不均非常明显，则归一化可起到一些作用
    # [rows, cols, depth] = src.shape
    # dst = np.zeros([rows, cols, depth], dtype='uint8')
    # dst = cv2.normalize(src, dst=dst, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    # if isShowImage:
    #     showCV2Image('dst_b', dst)


    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)#彩色转灰度图
    if isShowImage:
        showCV2Image('gray', gray)

    # 需要去除光照的影响
    dst = removelight(gray, block=32)
    cv2.imwrite('Johns_Form_1.jpg', dst)

    #dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    #此处需要注意灰度图转彩色图的伪彩色技术，需要继续处理，否则出来的仍为灰度图，是一种彩色图的索引


    # 下面进行图像增强操作
    src1 = Image.open('Johns_Form_1.jpg')  # imread的图像为数组，image其自带的open方法无法处理，mode不对应，open返回一个pil对象
    img = image_enhancement(src1)
    cv2.imwrite('Johns_Form_2.jpg', img)





