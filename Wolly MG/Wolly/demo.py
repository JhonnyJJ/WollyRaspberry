import random
import re
from frasiDialog import *
import time
from pygame import mixer
from motorsNew import *
from gtts import gTTS
import os
import time
from tkinter import *
from PIL import Image, ImageTk
import signal
import sys
import multiprocessing

def signal_handler(sig, frame):
    global process1, process3
    print('You ended the program')
    process1.terminate()
    process3.terminate()
    time.sleep(3)
    sys.exit(0)

def master():
    global process2
    process2 = multiprocessing.Process(target=face)
    process2.start()
    time.sleep(2)
    textSpeech("ciao sono wolly, sono il robottino del dipartimento di informatica di Torino")
    textSpeech("Ti dico un fatto simpatico su di me")
    textSpeech("lo sapevi che " + random.choice(curiosita))
    reface("wink", 4)
    textSpeech("so fare tante cose come ad esempio ballare, guarda qui")
    ballare()
    textSpeech("evviva, che divertimento!")
    textSpeech("so anche cantare, senti che voce!")
    cantare()
    textSpeech("posso farti anche ridere con una battuta")
    print(random.choice(battuta))
    textSpeech(random.choice(battuta))
    reface("crazy", 0)
    playsound("../../mp3/joke.mp3")
    textSpeech("queste sono solo alcune delle cose che so fare")
    textSpeech("di sicuro con il tempo ne saprò fare ancora di più")


def playsound(filepath):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.01)

def textSpeech(text):
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    reface("speaker",0)
    playsound("tts.mp3")

def reface(espr, tempo):
    global process2
    process2.terminate()
    change(espr, tempo)

def change(espr, tempo):
    global espressione, process2
    espressione = espr
    process2 = multiprocessing.Process(target=face)
    process2.start()
    time.sleep(tempo)

espressione = "default"

def face():
    global label, x, espressione, root, p, frames
    time.sleep(0.3)
    root = Tk()
    frames = 50
    x = 1
    p = 1
    # inizializza una Tk structure
    root.attributes('-fullscreen', True)

    # creiamo la label e la configuriamo con l'immagine

    label = Label(root)
    label.pack()
    root.after(0, niamPool)
    root.mainloop()


# "piccolo" è una variabile per capire se stiamo usando un'animazione con meno di n "frames" (può essere scalato a piacimento)
# "p" è il contatore per "piccolo" che si ri azzera per poter rifare il ciclo sull'animazione corta (così fa il loop dell'animazione per avere almeno n "frames" totali)
# "piccolo" viene anche usato in niampoll per poter iniziare una nuova animazione prima, in caso sia stata fatta un'animazione breve
def loop():
    global espressione, x, imag, piccolo, p, frames
    DIR = "/home/wolly/Desktop/WollyRaspberry/img/faces/" + espressione + "/"
    face = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and ".png" in name]
    lunghezza = len(face)
    if lunghezza <= frames:
        length = frames
        piccolo = 1
    else:
        length = lunghezza
        piccolo = 0

    if x <= length:
        if piccolo == 1:
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
        root.after(5000, niamPool)

def ballare():
    canzoni = ["../../mp3/mii.mp3", "../../mp3/jojos.mp3"]
    durata = [0.2, 0.5, 0.4, 0.3]
    velocita = [0.5, 0.55]
    movimento = [0, 1]
    mixer.init()
    mixer.music.load(random.choice(canzoni))
    mixer.music.play()
    c = 0
    reface("crazy",0)
    while c < 36:
        if c == 20:
            reface("crazy",0)
        if random.choice(movimento) == 1:
           destra(random.choice(durata), random.choice(velocita))
        else:
           sinistra(random.choice(durata), random.choice(velocita))
        c += 1
    mixer.quit()


def cantare():
    durata = [0.2, 0.1]
    canta = ["../../mp3/alien_sound.mp3", "../../mp3/pavarotti.mp3"]
    mixer.init()
    mixer.music.load(random.choice(canta))
    mixer.music.play()
    c = 0
    reface("sing", 0)
    while c < 35:
        if c == 10 or c == 18:
            reface("sing", 0)
        destra(random.choice(durata), 0.46)
        sinistra(random.choice(durata), 0.46)
        c += 1

    mixer.quit()


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
    process1 = multiprocessing.Process(target=default)              # faccia in background per coprire lo schermo
    process3 = multiprocessing.Process(target=master)                       # controllo se wolly è autonomo o no, crea processo faccia che si chiude e si riapre ogni volta che si cambia espressione
    process1.start()
    time.sleep(2)
    process3.start()
    signal.signal(signal.SIGINT, signal_handler)