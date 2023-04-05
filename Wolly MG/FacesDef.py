import os
import time
from tkinter import *
from PIL import Image, ImageTk

global label, x, espressione, root
    
root = Tk()
espressione = "speaker"
x = 1
#initialize a Tk structure
root.attributes('-fullscreen', False)

root.geometry("800x480")

#we create the label and then configure it with the image

label = Label(root)
label.pack()

def loop():
    global espressione, x, imag
    DIR = "/home/wolly/Desktop/WollyRaspberry/img/faces/" + espressione + "/"
    face = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and ".png" in name]
    lenght = len(face)
    print(espressione)
    print(DIR)
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
    global flag
    loop()
    if flag == "long":
        root.after(7000, niamPool)
    else:
        
    
def main():
    root.after(0,niamPool)
    root.mainloop()
    
if __name__ == "__main__":
    main()
    
    
    

    

