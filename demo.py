import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import function_modules
import morph_module
import enhancement_module

def choose_pic():
    global path
    path = askopenfilename()
    print(path)
    img_ = Image.open(path)

    if img_.size[0] > img_.size[1]:
        scale = img_.size[0] / 585
    else:
        scale = img_.size[1] / 685
    new_w = int(img_.size[0] / scale)
    new_h = int(img_.size[1] / scale)
    img_ = img_.resize((new_w, new_h))

    global path_
    path_=path+'_resize.jpg'
    img_.save(path_)
    global src
    src = cv2.imread(path_)
    global img_choose
    img_choose = ImageTk.PhotoImage(img_)
    global x_start, y_start
    x_start = 10 if img_.size[0] > img_.size[1] else (585 - new_w) / 2
    y_start = 10 if img_.size[0] < img_.size[1] else (685 - new_h) / 2
    original_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose)

def gray_value():

    # global gray
    gray = function_modules.gray(src)
    path1 = path+'_gray.jpg'
    cv2.imwrite(path1, gray)
    img_ = Image.open(path1)
    global img_choose1
    img_choose1 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose1)

def gamma_correction():
    gray = function_modules.gray(src)
    gamma = function_modules.gamma(gray)
    path2 = path+'_gamma.jpg'
    cv2.imwrite(path2, gamma)
    img_ = Image.open(path2)
    global img_choose2
    img_choose2 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose2)

def bgr_adap():
    bgr_adap_merge = function_modules.bgr_adap(src)
    path3 = path+'_bgr_adap.jpg'
    cv2.imwrite(path3, bgr_adap_merge)
    img_ = Image.open(path3)
    global img_choose3
    img_choose3 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose3)

def remove_light():
    gray = function_modules.gray(src)
    dst = function_modules.removelight(gray, block=32)
    path4 = path + '_removelight.jpg'
    cv2.imwrite(path4, dst)
    img_ = Image.open(path4)
    global img_choose4
    img_choose4 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose4)

def color_balance():
    img = function_modules.color_balance(src)
    path5 = path + '_colorbalance.jpg'
    cv2.imwrite(path5, img)
    img_ = Image.open(path5)
    global img_choose5
    img_choose5 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose5)

def p_color_correction():
    src1 = function_modules.p_color_correction(src)
    path6 = path + '_p_color_correction.jpg'
    cv2.imwrite(path6, src1)
    img_ = Image.open(path6)
    global img_choose6
    img_choose6 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose6)

def bit_layer_split():
    gray = function_modules.gray(src)
    reconstruct = function_modules.bit_layer_split(gray)
    path7 = path + '_bitlayerreconstruct.jpg'
    cv2.imwrite(path7, reconstruct)
    img_ = Image.open(path7)
    global img_choose7
    img_choose7 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose7)

def hole_filling():
    gray = function_modules.gray(src)
    final_out = function_modules.hole_filling(gray)
    path8 = path + '_holefilling.jpg'
    cv2.imwrite(path8, final_out)
    img_ = Image.open(path8)
    global img_choose8
    img_choose8 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose8)

def remove_lines():
    gray = function_modules.gray(src)
    bins = morph_module.binary(gray)
    n_tab_lines = morph_module.removelines(bins)
    path9 = path + '_removelines.jpg'
    cv2.imwrite(path9, n_tab_lines)
    img_ = Image.open(path9)
    global img_choose9
    img_choose9 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose9)

def median_blur():
    gray = function_modules.gray(src)
    bins = morph_module.binary(gray)
    dilation = morph_module.open(bins)
    medianblur1 = morph_module.medianblur(dilation)
    path10 = path + '_medianblur.jpg'
    cv2.imwrite(path10, medianblur1)
    img_ = Image.open(path10)
    global img_choose10
    img_choose10 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose10)

def brightness():
    global image1
    image1 = Image.open(path_)
    brightness = enhancement_module.brightness(image1)
    path11=path+'_brightness.jpg'
    brightness.save(path11)
    img_ = Image.open(path11)
    global img_choose11
    img_choose11 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose11)

def contrast():
    contrast = enhancement_module.contrast(image1)
    path12=path+'_contrast.jpg'
    contrast.save(path12)
    img_ = Image.open(path12)
    global img_choose12
    img_choose12 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose12)

def sharpness():
    sharpness = enhancement_module.sharpness(image1)
    path13 = path+'_sharpness.jpg'
    sharpness.save(path13)
    img_ = Image.open(path13)
    global img_choose13
    img_choose13 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose13)

def color():
    color = enhancement_module.color(image1)
    path14 = path + '_color.jpg'
    color.save(path14)
    img_ = Image.open(path14)
    global img_choose14
    img_choose14 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose14)

def binary_value():
    gray = function_modules.gray(src)
    bins = morph_module.binary(gray)
    path15 = path + '_binary.jpg'
    cv2.imwrite(path15, bins)
    img_ = Image.open(path15)
    global img_choose15
    img_choose15 = ImageTk.PhotoImage(img_)
    enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=img_choose15)

root = tk.Tk()
root.title("Image Enhancement Demo")

width = 1400
height = 800

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
root.geometry(alignstr)

og_title = tk.Label(root, text='Original Image', width=20, height=5, font=("Arial", 12))
og_title.place(x=200, y=5)

enhance_title = tk.Label(root, text='Enhanced Image', width=20, height=5, font=("Arial", 12))
enhance_title.place(x=700, y=5)

original_canvas = tk.Canvas(root, width=600, height=700)
original_canvas.create_rectangle(5, 5, 600, 700)
original_canvas.place(x=0, y=50)


enhanced_canvas = tk.Canvas(root, width=600, height=700)
enhanced_canvas.create_rectangle(5, 5, 600, 700)
enhanced_canvas.place(x=605, y=50)

button1 = tk.Button(root, text="Choose Picture", command=choose_pic)
button1.place(x=1250, y=50)

button2 = tk.Button(root, text="gray value", command=gray_value)
button2.place(x=1250, y=80)

button16 = tk.Button(root, text="adaptive binary", command=binary_value)
button16.place(x=1250, y=110)

button3 = tk.Button(root, text="gamma correction", command=gamma_correction)
button3.place(x=1250, y=140)

button4 = tk.Button(root, text="bgr adaptive hist", command=bgr_adap)
button4.place(x=1250, y=170)

button5 = tk.Button(root, text="remove light", command=remove_light)
button5.place(x=1250, y=200)

button6 = tk.Button(root, text="color balance", command=color_balance)
button6.place(x=1250, y=230)

button7 = tk.Button(root, text="p color correction", command=p_color_correction)
button7.place(x=1250, y=260)

button8 = tk.Button(root, text="bit layer split", command=bit_layer_split)
button8.place(x=1250, y=290)

button9 = tk.Button(root, text="hole filling", command=hole_filling)
button9.place(x=1250, y=320)

button10 = tk.Button(root, text="remove lines", command=remove_lines)
button10.place(x=1250, y=350)

button11 = tk.Button(root, text="median blur", command=median_blur)
button11.place(x=1250, y=380)

button12 = tk.Button(root, text="brightness", command=brightness)
button12.place(x=1250, y=410)

button13 = tk.Button(root, text="contrast", command=contrast)
button13.place(x=1250, y=440)

button14 = tk.Button(root, text="sharpness", command=sharpness)
button14.place(x=1250, y=470)

button15 = tk.Button(root, text="color", command=color)
button15.place(x=1250, y=500)



root.mainloop()