# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import os
import shutil

if __name__ == '__main__':
    file = open('rotation_test/90_result.txt', 'r')
    lines = file.readlines()
    result = []
    for line in lines:
        lineData = line.strip().split(',')
        result.append(lineData)
    print('result', result)

    images = []
    angles = []
    rotate = []
    wrong_img = []
    right = 0#正确检测的个数
    total_num = len(result)#总个数
    cannot_detect = 0
    for i in range(len(result)):
        image, angle = result[i][0].split(':')
        angles.append(angle)#检测出的旋转角度
        images.append(image)  # 每个图片的文件名

        img1 = image.split('_')
        if len(img1) == 1:
            img1.append('0')

        a = img1[1].split('.')
        rotate.append(a[0])#正确的旋转角度

        if a[0] == angle:
            right += 1
        elif angle == '*':
            cannot_detect += 1
            wrong_img.append(image)
        else:
            wrong_img.append(image)
    wrong = total_num - cannot_detect - right

    print('images', images)
    print('angles', angles)
    print('rotate', rotate)
    print('right', right)
    print('total', total_num)
    print('cannot', cannot_detect)
    print('wrong', wrong)
    print('wrong img', wrong_img)
    print('wrong num', len(wrong_img))

    #把错误的图片单独拎出来
    ori_path = 'rotation_test/90_-90'
    wro_path = 'rotation_test/90_-90_wrong'
    for i in range(len(wrong_img)):
          old_name = ori_path + '/' + wrong_img[i]
          new_name = wro_path + '/' + wrong_img[i]
          shutil.copyfile(old_name, new_name)

    #画饼图分析
    fig = plt.figure()
    labels = ['cannot detect', 'right', 'wrong']
    nums = [cannot_detect, right, wrong]
    colors = ['yellow', 'green', 'red']
    plt.pie(nums, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('90 rotation result analysis')
    plt.savefig('rotation_test/0_90_rotation_result_analysis.jpg')
    plt.show()






