import cv2
import numpy as np

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)#调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
    src = cv2.imread('APT003_a1.jpg', cv2.IMREAD_GRAYSCALE)#直接返回一个灰度图
    if isShowImage:
        showCV2Image('src', src)

    src1 = cv2.imread('APT003_a2.jpg', cv2.IMREAD_GRAYSCALE)
    if isShowImage:
        showCV2Image('src1', src1)

    th, im_th = cv2.threshold(src, 220, 255, cv2.THRESH_BINARY_INV)
    h, w = im_th.shape

    im_floodfill = im_th.copy()

    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)

    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    im_out = im_th | im_floodfill_inv

    out = cv2.bitwise_xor(im_floodfill, src1)
    if isShowImage:
        showCV2Image('out1', out)

    final_out = cv2.bitwise_not(out)
    if isShowImage:
        showCV2Image('f_out', final_out)

    cv2.imwrite('APT003_out.jpg', final_out)

    if isShowImage:
        showCV2Image('threshold', im_th)
        showCV2Image('fill', im_floodfill)
        showCV2Image('inv fill', im_floodfill_inv)
        showCV2Image('out', im_out)

