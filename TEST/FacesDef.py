import os
import time
from tkinter import *
from PIL import Image, ImageTk

espressione = "crazy"
x = 1

#initialize a Tk structure
root = Tk()
root.attributes('-fullscreen', True)

# this are the dimension of the screen connected
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#we create the label and then configure it with the image
label = Label(root)
label.pack()

resized_image = Image.open("/home/wolly/Desktop/WollyRaspberry/img/faces/" + espressione + "/1.png").resize((width, height))
imag = ImageTk.PhotoImage(resized_image)
    
def loop():
    global espressione, x, imag
    DIR = "/home/wolly/Desktop/WollyRaspberry/img/faces/" + espressione + "/"
    face = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and ".png" in name]
    lenght = len(face)
    if x <= 33:
        img_temp = Image.open(DIR + str(x) + ".png")
        resized_image = img_temp.resize((width,height))
        imag = ImageTk.PhotoImage(resized_image)
        label.configure(image=imag)
        x += 1
        root.after(1, loop)
    else:
        x = 1
        espressione = "default" 
    
    
def niamPool():
    loop()
    root.after(20000, niamPool)
        

def change_face(esprex):
    global espressione
    espressione = esprex
    
    
def main():
    root.after(0,niamPool)
    root.mainloop()
    
if __name__ =="__main__":
    main()
    
