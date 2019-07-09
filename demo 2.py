import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk


def choose_pic():
    path_=askopenfilename()
    cache['path'] = path_
    img_ = Image.open(path_)
    print(img_.size[0], img_.size[1])
    if img_.size[0] > img_.size[1]:
        scale = img_.size[0] / 1000
    else:
        scale = img_.size[1] / 800

    new_w = int(img_.size[0] / scale)
    new_h = int(img_.size[1] / scale)
    img_ = img_.resize((new_w, new_h))
    print(new_w, new_h)

    img_choose=ImageTk.PhotoImage(img_)

    label.configure(image=img_choose)
    label.image = img_choose
    print(cache['path'])


root = tk.Tk()
root.title("Image Enhancement Demo")
cache = {}

width = 1000
height = 1100

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
root.geometry(alignstr)


image_area = tk.Frame(width=500, height=800,bg="red")
image_area.pack_propagate(0)
image_area.pack(side="left")

image_area1 = tk.Frame(width=500, height=800,bg="black")
image_area1.pack_propagate(0)
image_area1.pack(side="right")

label = tk.Label(image_area)
label.pack()

button = tk.Button(root, text = "Choose Picture", command = choose_pic)
button.pack()

root.mainloop()