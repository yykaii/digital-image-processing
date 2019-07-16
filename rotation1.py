# -*- coding:utf-8 -*-
from PIL import Image, ExifTags
import cv2
isShowImage = True

def showCV2Image(title, img):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # 调整窗口大小并保持比例
    cv2.imshow(title, img)
    cv2.waitKey(0)

if __name__ == '__main__':

   img = Image.open('r0.jpg')
   try:
       print('a')
       for orientation in ExifTags.TAGS.keys() :
           if ExifTags.TAGS[orientation]=='Orientation' : break
       print('b')
       exif=dict(img._getexif().items())
       print('c')
       print(exif[orientation])
       if   exif[orientation] == 3 :
           img=img.rotate(180, expand = True)
       elif exif[orientation] == 6 :
           img=img.rotate(270, expand = True)
       elif exif[orientation] == 8 :
           img=img.rotate(90, expand = True)
   except:
       pass
   img.show()
