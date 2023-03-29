import os
import tkinter
# from threading import Timer
from tkinter import *
import urllib3
from PIL import Image, ImageTk
# create a tkinter window
t = Tk()
t.attributes('-fullscreen', False)

# Create a size for tkinter window
t.geometry("800x480")  # here use alphabet 'x' not '*' this one

# Create a label
label = Label(t, font="bold")
label.pack()
x=1
global espressione
espressione = "crazy"
img = ImageTk.PhotoImage(Image.open("../img/faces/crazy/1.png"))



def expression():
    global x, img, espressione
    DIR = '../img/faces/' + espressione + "/"
    faces = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and ".png" in name]
    count = len(faces)
    if x <= count:
        img = ImageTk.PhotoImage(Image.open(DIR + str(x) + ".png"))
        label.configure(image=img)
        x += 1
        t.after(1, expression)
    else:
        x = 1
        espressione = "default"
        t.after(500, expression)
        
def main():
    expression()
    