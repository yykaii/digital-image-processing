import cv2
from skimage import exposure

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
        cv2.imwrite('Johns_DL_contrast_gray.jpg', gray)

        #gamma矫正，可让亮的部分，适当变暗或者暗的地方适当变亮
        gamma = exposure.adjust_gamma(gray, gamma=2.5)
        if isShowImage:
            showCV2Image('gamma', gamma)
        cv2.imwrite('Johns_DL_contrast_gamma2.5.jpg', gamma)

