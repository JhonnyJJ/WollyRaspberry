import os
import tkinter
from tkinter import *
from PIL import Image, ImageTk

t = Tk()

x = 1
img = ImageTk.PhotoImage(Image.open("img/faces/default/1.png"))


def update(expression):
    global x, img
    DIR = 'img/faces/' + expression + "/"
    count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    if x != count:
        img = ImageTk.PhotoImage(Image.open(DIR + str(x) + ".png"))
        print(DIR + str(x) + ".png")
        l.configure(image=img)
        x += 1
        t.after(5, update, expression)
    else:
        print("exit if")


l = Label(t, font="bold")
l.pack()
t.after(0, update, "fear")
tkinter.mainloop()
