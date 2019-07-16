import cv2
import numpy as np
import matplotlib.pylab as plt
import time

#注意，此处只适于[-90, 90]的旋转

isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':

   img = cv2.imread('r0.jpg')
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
   binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
   if showCV2Image:
       showCV2Image('bin', binary)

   contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   #cv2.RETR_TREE检索所有轮廓并创建完整的族层次结构列表

   print("num of contours: {}".format(len(contours)))

   rect = cv2.minAreaRect(contours[1])  #获取蓝色矩形的中心点、宽高、角度
   print('rect', rect)

   '''
   retc=((202.82777404785156, 94.020751953125),
    (38.13406753540039, 276.02105712890625),
    -75.0685806274414)
   '''

   width = int(rect[1][0])
   height = int(rect[1][1])
   angle = rect[2]
   print(angle)

   if width < height:  #计算角度，为后续做准备
     angle = angle - 90
   print(angle)
   # if angle < 0:
   #     angle += 90.0
# if  angle < -45:
#     angle += 90.0
#        #保证旋转为水平
# width,height = height,width
   src_pts = cv2.boxPoints(rect)

# box = cv2.boxPoints(rect)
# box = np.int0(box)
# cv2.drawContours(img_box, [box], 0, (0,255,0), 2) 
#

   dst_pts = np.array([[0, height],
                    [0, 0],
                    [width, 0],
                    [width, height]], dtype="float32")
   M = cv2.getPerspectiveTransform(src_pts, dst_pts)
   warped = cv2.warpPerspective(img, M, (width, height))

   rows1, cols1 = img.shape[:2]

   # angle = 0-angle
   # print('rangle', angle)

   rotate = cv2.getRotationMatrix2D((int(cols1/2), int(rows1/2)), angle, 1)  # 旋转转换矩阵，第三个参数是缩放系数，1表示保持原图大小
   img_ex_rotate = cv2.warpAffine(img, rotate, (rows1, cols1))
   if isShowImage:
       showCV2Image('img_ex', img_ex_rotate)


   if angle <=  -90:  #对-90度以上图片的竖直结果转正
       warped = cv2.transpose(warped)
       warped = cv2.flip(warped, 0)  # 逆时针转90度，如果想顺时针，则0改为1
    # warped=warped.transpose
   # if isShowImage:
   #     showCV2Image('wr1', warped)
