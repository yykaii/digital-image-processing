import cv2
import numpy as np
#这个代码写的有问题，并不能是正规的bit平面分层操作

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':
        image = cv2.imread('Johns_DL_contrast.jpg')
        if isShowImage:
            showCV2Image('image', image)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if isShowImage:
            showCV2Image('gray', gray)

        rows, cols = gray.shape

        #比特分层
        #将每个灰度像素十进制转为八位二进制
        bits = np.zeros((rows, cols, 8), np.uint8)
        for i in range(rows):
            for j in range(cols):
                # bits[i][j] = '{:08b}'.format(gray[i][j])
                tmp = list('{:08b}'.format(gray[i][j]))
                for s in range(8):
                    bits[i][j][s] = int(tmp[s])

        #分离为8层
        layers = []
        for i in range(8):
            layer = np.zeros((rows, cols), np.uint8)
            layer1 = np.zeros((rows, cols), np.uint8)
            for j in range(rows):
                for k in range(cols):
                    #此处为了突出显示，将平面值为1的用255代替
                    if bits[j][k][i] > 0:
                        layer[j][k] = 255
                    layer1[j][k] = bits[j][k][i]
            if isShowImage:
                showCV2Image('layers'+str(i), layer)
            layers.append(layer1)

        #层面重建，4个高层的比特面即可很好重建，乘以对应层数的2的幂次
        reconstruct = np.zeros((rows, cols), np.uint8)
        for j in range(rows):
            for k in range(cols):
                tmp = 0
                for i in range(4):
                    tmp += bits[j][k][i]*pow(2, 8-i)
                reconstruct[j][k] = tmp
        if isShowImage:
            showCV2Image('re', reconstruct)

        cv2.imwrite('chart_4_bit.jpg', reconstruct)

