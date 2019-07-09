import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
import cv2
import function_modules
import morph_module
import enhancement_module

def show_image1(img_):
    img_choose = ImageTk.PhotoImage(img_)
    label1.configure(image=img_choose)
    label1.image = img_choose

def show_image2(img_):
    img_choose = ImageTk.PhotoImage(img_)
    label2.configure(image=img_choose)
    label2.image = img_choose

def choose_pic():
    global path
    path = askopenfilename()
    print(path)
    img_ = Image.open(path)

    if img_.size[0] > img_.size[1]:
        scale = img_.size[0] / 450
    else:
        scale = img_.size[1] / 700

    new_w = int(img_.size[0] / scale)
    new_h = int(img_.size[1] / scale)

    img_ = img_.resize((new_w, new_h))
    global path_
    path_=path+'_resize.jpg'
    img_.save(path_)
    # img_ = Image.open(path_)
    show_image1(img_)

def gray_value():
    global src
    src = cv2.imread(path_)
    global gray
    gray = function_modules.gray(src)
    path1 = path+'_gray.jpg'
    cv2.imwrite(path1, gray)
    img_ = Image.open(path1)
    show_image2(img_)

def gamma_correction():
    gamma = function_modules.gamma(gray)
    path2 = path+'_gamma.jpg'
    cv2.imwrite(path2, gamma)
    img_ = Image.open(path2)
    show_image2(img_)

def bgr_adap():
    bgr_adap_merge = function_modules.bgr_adap(src)
    path3 = path+'_bgr_adap.jpg'
    cv2.imwrite(path3, bgr_adap_merge)
    img_ = Image.open(path3)
    show_image2(img_)

def remove_light():
    dst = function_modules.removelight(gray, block=32)
    path4 = path + '_removelight.jpg'
    cv2.imwrite(path4, dst)
    img_ = Image.open(path4)
    show_image2(img_)

def color_balance():
    img = function_modules.color_balance(src)
    path5 = path + '_colorbalance.jpg'
    cv2.imwrite(path5, img)
    img_ = Image.open(path5)
    show_image2(img_)

def p_color_correction():
    src1 = function_modules.p_color_correction(src)
    path6 = path + '_p_color_correction.jpg'
    cv2.imwrite(path6, src1)
    img_ = Image.open(path6)
    show_image2(img_)

def bit_layer_split():
    reconstruct = function_modules.bit_layer_split(gray)
    path7 = path + '_bitlayerreconstruct.jpg'
    cv2.imwrite(path7, reconstruct)
    img_ = Image.open(path7)
    show_image2(img_)

def hole_filling():
    final_out = function_modules.hole_filling(gray)
    path8 = path + '_holefilling.jpg'
    cv2.imwrite(path8, final_out)
    img_ = Image.open(path8)
    show_image2(img_)

def remove_lines():
    bins = morph_module.binary(gray)
    n_tab_lines = morph_module.removelines(bins)
    path9 = path + '_removelines.jpg'
    cv2.imwrite(path9, n_tab_lines)
    img_ = Image.open(path9)
    show_image2(img_)

def median_blur():
    bins = morph_module.binary(gray)
    dilation = morph_module.open(bins)
    medianblur1 = morph_module.medianblur(dilation)
    path10 = path + '_medianblur.jpg'
    cv2.imwrite(path10, medianblur1)
    img_ = Image.open(path10)
    show_image2(img_)

def brightness():
    global image1
    image1 = Image.open(path_)
    brightness = enhancement_module.brightness(image1)
    brightness.save(path+'_brightness.jpg')
    show_image2(brightness)

def contrast():
    contrast = enhancement_module.contrast(image1)
    contrast.save(path+'_contrast.jpg')
    show_image2(contrast)

def sharpness():
    sharpness = enhancement_module.sharpness(image1)
    sharpness.save(path+'_sharpness.jpg')
    show_image2(sharpness)

def color():
    color = enhancement_module.color(image1)
    color.save(path+'_color.jpg')
    show_image2(color)

root = tk.Tk()
root.title("Image Enhancement Demo")

width = 1000
height = 800

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
root.geometry(alignstr)

image_area = tk.Frame(width=900, height=700, padx=10, pady=10)
# image_area.pack_propagate(0)
image_area.grid(row=0)

label1 = tk.Label(image_area)
label1.grid(row=0, column=0, rowspan=10)
button1 = tk.Button(root, text="Choose Picture", command=choose_pic)
button1.grid(row=0, column=2)

label2 = tk.Label(image_area)
label2.grid(row=0, column=1, rowspan=10)
button2 = tk.Button(root, text="gray value", command=gray_value)
button2.grid(row=1, column=2)

label3 = tk.Label(image_area)
label3.grid(row=0, column=1, rowspan=10)
button3 = tk.Button(root, text="gamma correction", command=gamma_correction)
button3.grid(row=2, column=2)

label4 = tk.Label(image_area)
label4.grid(row=0, column=1, rowspan=10)
button4 = tk.Button(root, text="bgr adaptive hist", command=bgr_adap)
button4.grid(row=3, column=2)

label5 = tk.Label(image_area)
label5.grid(row=0, column=1, rowspan=10)
button5 = tk.Button(root, text="remove light", command=remove_light)
button5.grid(row=4, column=2)

label6 = tk.Label(image_area)
label6.grid(row=0, column=1, rowspan=10)
button6 = tk.Button(root, text="color balance", command=color_balance)
button6.grid(row=5, column=2)

label7 = tk.Label(image_area)
label7.grid(row=0, column=1, rowspan=10)
button7 = tk.Button(root, text="p color correction", command=p_color_correction)
button7.grid(row=6, column=2)

label8 = tk.Label(image_area)
label8.grid(row=0, column=1, rowspan=10)
button8 = tk.Button(root, text="bit layer split", command=bit_layer_split)
button8.grid(row=7, column=2)

label9 = tk.Label(image_area)
label9.grid(row=0, column=1, rowspan=10)
button9 = tk.Button(root, text="hole filling", command=hole_filling)
button9.grid(row=8, column=2)

label10 = tk.Label(image_area)
label10.grid(row=0, column=1, rowspan=10)
button10 = tk.Button(root, text="remove lines", command=remove_lines)
button10.grid(row=9, column=2)

label11 = tk.Label(image_area)
label11.grid(row=0, column=1, rowspan=10)
button11 = tk.Button(root, text="median blur", command=median_blur)
button11.grid(row=10, column=2)

label12 = tk.Label(image_area)
label12.grid(row=0, column=1, rowspan=10)
button12 = tk.Button(root, text="brightness", command=brightness)
button12.grid(row=11, column=2)

label13 = tk.Label(image_area)
label13.grid(row=0, column=1, rowspan=10)
button13 = tk.Button(root, text="contrast", command=contrast)
button13.grid(row=12, column=2)

label14 = tk.Label(image_area)
label14.grid(row=0, column=1, rowspan=10)
button14 = tk.Button(root, text="sharpness", command=sharpness)
button14.grid(row=13, column=2)

label15 = tk.Label(image_area)
label15.grid(row=0, column=1, rowspan=10)
button15 = tk.Button(root, text="color", command=color)
button15.grid(row=14, column=2)

root.mainloop()