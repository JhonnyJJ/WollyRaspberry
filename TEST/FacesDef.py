import os
import time
from tkinter import *
from PIL import Image, ImageTk

global label, x, espressione, root
    
root = Tk()
espressione = "default"
x = 1
#initialize a Tk structure
root.attributes('-fullscreen', False)

root.geometry("800x480")

# this are the dimension of the screen connected
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#we create the label and then configure it with the image

label = Label(root)
label.pack()

def loop():
    global espressione, x, imag
    DIR = "/home/wolly/Desktop/WollyRaspberry/img/faces/" + espressione + "/"
    face = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and ".png" in name]
    lenght = len(face)
    print(x)
    if x <= lenght:
        resized_image = Image.open(DIR + str(x) + ".png")
        imag = ImageTk.PhotoImage(resized_image)
        label.configure(image=imag)
        x += 1
        root.after(10, loop)
    else:
        x = 1
        espressione = "default"
    
    
def niamPool():
    loop()
    root.after(7000, niamPool)
    print("prova")
    
def main():
    root.after(0,niamPool)
    root.mainloop()
    
if __name__ == "__main__":
    main()
    
    

    

