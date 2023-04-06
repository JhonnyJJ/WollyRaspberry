import os
import time
from tkinter import *
from PIL import Image, ImageTk

# piccolo è una variabile per capire se stiamo usando una variabile con meno di 30 frame
# p è il contatore che si ri azzera per poter rifare il ciclo sull'animazione corta (così fa il loop dell'animazione per avere almeno 30 frame totali)
# piccolo viene anche usato in niampoll per poter iniziare una nuova animazione prima 
def loop():
    global espressione, x, imag, piccolo, p, frames
    DIR = "/home/wolly/Desktop/WollyRaspberry/img/faces/" + espressione + "/"
    face = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and ".png" in name]
    lunghezza = len(face)
    print(espressione)
    print(DIR)
    if lunghezza <= frames:
        lenght = frames
        piccolo = 1
    else:
        lenght = lunghezza
        piccolo = 0
    
    if x <= lenght:
        if piccolo ==1:
            if p >= lunghezza:
                p = 1
            resized_image = Image.open(DIR + str(p) + ".png")
            imag = ImageTk.PhotoImage(resized_image)
            p += 1
        else:
            resized_image = Image.open(DIR + str(x) + ".png")
            imag = ImageTk.PhotoImage(resized_image)
        label.configure(image=imag)
        x += 1
        root.after(10, loop)
    else:
        x = 1
        espressione = "default" 
    
def niamPool():
    global piccolo
    loop()
    if piccolo == 0:
        root.after(7000, niamPool)
    elif piccolo == 1:
        root.after(4000, niamPool)
        
def main():
    global label, x, espressione, root, frames, p
    
    root = Tk()
    espressione = "speaker"
    frames = 40
    x = 1
    p = 1
    #initialize a Tk structure
    root.attributes('-fullscreen', False)

    root.geometry("800x480")

    #we create the label and then configure it with the image

    label = Label(root)
    label.pack()
    
    root.after(0,niamPool)
    root.mainloop()
    
if __name__ == "__main__":
    main()
    
    
    

    

