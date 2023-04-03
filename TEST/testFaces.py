import os
import time
from tkinter import *
from PIL import Image, ImageTk
import signal
import sys
import multiprocessing

def signal_handler(sig, frame):
    print('You ended the program')
    process1.terminate()
    process2.terminate()
    process3.terminate()
    sys.exit(0)
    
# processo face che permette il cambio di faccia, utilizzando espressione come globale per essere accessibile al secondo processo
espressione = "default"

def face():
    global label, x, espressione, root
    
    root = Tk()
    x = 1
    #initialize a Tk structure
    root.attributes('-fullscreen', True)

    #root.geometry("800x480")

    # this are the dimension of the screen connected
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    #we create the label and then configure it with the image

    label = Label(root)
    label.pack()
    
    root.after(0,niamPool)
    root.mainloop()
    
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
#----------fine processo faccia--------------

#secondo processo che usa "reface" PER CAMBIARE LA FACCIA QUANDO VUOLE
def prova():
    global espressione, flag
    time.sleep(10)
    reface("crazy")
    time.sleep(10)
    reface("anger")
    
def reface(espr):
    global process1
    process1.terminate()
    change(espr)
    
def change(espr):
    global espressione, process1
    espressione = espr
    process1 = multiprocessing.Process(target=face)
    process1.start()
    
#----------fine secondo processo -----------    
    
def default():
    t = Tk()
    t.attributes('-fullscreen', True)
    direct = "/home/wolly/Desktop/WollyRaspberry/img/faces/default/6.png"
    label = Label(t)
    label.pack()
    im = ImageTk.PhotoImage(Image.open(direct))
    label.configure(image=im)
    t.mainloop()

if __name__ == '__main__':
    print('Press Ctrl+C to stop the program')
    process1 = multiprocessing.Process(target=face)
    process2 = multiprocessing.Process(target=prova)
    process3 = multiprocessing.Process(target=default)
    process3.start()
    process1.start()
    process2.start()
    signal.signal(signal.SIGINT, signal_handler)
