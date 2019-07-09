import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk


def choose_pic():
    path_=askopenfilename()
    print(path_)
    img_ = Image.open(path_)
    img_choose=ImageTk.PhotoImage(img_)
    label.configure(image=img_choose)
    label.image = img_choose


root = tk.Tk()
root.title("Image Enhancement Demo")


width = 1000
height = 800

screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
root.geometry(alignstr)


image_area = tk.Frame(root, padx=10, pady=10)
image_area.pack()

label = tk.Label(image_area)
label.pack()

button = tk.Button(root, text = "Choose Picture", command = choose_pic)
button.pack()


root.mainloop()