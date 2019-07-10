import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2


def choose_pic():
    global og_pic_path
    path = askopenfilename()
    if path == "":
        return
    og_pic_path = path

    global og_pic
    img = Image.open(path)
    if img.size[0] > img.size[1]:
        scale = img.size[0] / 585
    else:
        scale = img.size[1] / 685
    new_w = int(img.size[0] / scale)
    new_h = int(img.size[1] / scale)
    img = img.resize((new_w, new_h))

    og_pic = ImageTk.PhotoImage(image=img)
    x_start = 10 if img.size[0] > img.size[1] else (585 - new_w) / 2
    y_start = 10 if img.size[0] < img.size[1] else (685 - new_h) / 2
    original_canvas.create_image(x_start, y_start, anchor='nw', image=og_pic)


def binary():
    if og_pic_path:
        img = cv2.imread(og_pic_path, 0)
        ret, img_b = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img = Image.fromarray(cv2.cvtColor(img_b, cv2.COLOR_BGR2RGB))
        if img.size[0] > img.size[1]:
            scale = img.size[0] / 585
        else:
            scale = img.size[1] / 685
        new_w = int(img.size[0] / scale)
        new_h = int(img.size[1] / scale)
        img = img.resize((new_w, new_h))

        global enhanced_pic
        enhanced_pic = ImageTk.PhotoImage(image=img)
        x_start = 10 if img.size[0] > img.size[1] else (585 - new_w) / 2
        y_start = 10 if img.size[0] < img.size[1] else (685 - new_h) / 2
        enhanced_canvas.create_image(x_start, y_start, anchor='nw', image=enhanced_pic)


window = tk.Tk()
window.title("Image Enhancement Demo")
cache = {}

width = 1410
height = 1000

screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
window.geometry(alignstr)

og_title = tk.Label(window, text='Original Image', width=20, height=5, font=("Arial", 10))
og_title.place(x=200, y=25)

enhance_title = tk.Label(window, text='Enhanced Image', width=20, height=5, font=("Arial", 10))
enhance_title.place(x=800, y=25)


original_canvas = tk.Canvas(window, width=600, height=700)
original_canvas.create_rectangle(5, 5, 600, 700)
original_canvas.place(x=0, y=100)


enhanced_canvas = tk.Canvas(window, width=600, height=700)
enhanced_canvas.create_rectangle(5, 5, 600, 700)
enhanced_canvas.place(x=605, y=100)

button_cho_pic = tk.Button(window, text = "Choose Picture", command = choose_pic)
button_cho_pic.place(x=1250, y=120)

button_binary = tk.Button(window, text = "To Binary", command = binary)
button_binary.place(x=1250, y=170)

window.resizable(0,0)
window.mainloop()