import signal
import sys
import multiprocessing

# import FaceDef
import os
import time
from tkinter import *
from PIL import Image, ImageTk

# import chatbot
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import re

# import trackingFace
import cv2
import random


# import frasi necessarie
from frasiDialog import *


# signal handler per ctrl+c alla fine del programma
def signal_handler(sig, frame):
    print('You ended the program')
    process1.terminate()
    process2.terminate()
    process3.terminate()
    # process4.terminate()
    time.sleep(2)
    sys.exit(0)


# ---------fine signal handler---------


# ------------------PROCESSO 1------------------
# permette il cambio di faccia, utilizzando espressione come globale per essere accessibile al secondo processo
espressione = "default"


def face():
    global label, x, espressione, root, p, frames
    time.sleep(0.3)
    root = Tk()
    frames = 50
    x = 1
    p = 1
    
    # initialize a Tk structure
    root.attributes('-fullscreen', True)

    # we create the label and then configure it with the image

    label = Label(root)
    label.pack()
    root.after(0, niamPool)
    root.mainloop()


# "piccolo" è una variabile per capire se stiamo usando una variabile con meno di n "frames" (può essere scalato a piacimento)
# "p" è il contatore per "piccolo" che si ri azzera per poter rifare il ciclo sull'animazione corta (così fa il loop dell'animazione per avere almeno n "frames" totali)
# "piccolo" viene anche usato in niampoll per poter iniziare una nuova animazione prima, in caso sia stata fatta un'animazione breve
def loop():
    global espressione, x, imag, piccolo, p, frames
    DIR = "/home/wolly/Desktop/WollyRaspberry/img/faces/" + espressione + "/"
    face = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and ".png" in name]
    lunghezza = len(face)
    if lunghezza <= frames:
        lenght = frames
        piccolo = 1
    else:
        lenght = lunghezza
        piccolo = 0

    if x <= lenght:
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

# ----------fine processo faccia--------------

# ------------------PROCESSO 2------------------
# secondo processo che usa "reface" PER CAMBIARE LA FACCIA QUANDO VUOLE
def playsound(filepath):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.01)
    # pygame.quit()   #windows debug


def textSpeech(text):
    tts = gTTS(text=text, lang='it')
    tts.save("../mp3/tts.mp3")
    reface("speaker")
    playsound("../mp3/tts.mp3")


# hardcoded chatbot AGGIUNGERE QUALCHE TIPO DI FACCIA CON DOMANDE O EMOZIONI
def chat(response):  # CREARE ALTRE DEF NEL CASO DI DIALOGO PIU' PROFONDO

    if re.search(r"\bno\b", response):
        print(random.choice(noproblem) + random.choice(allora))
        textSpeech(random.choice(noproblem) + random.choice(allora))
        return curioso(talk())
    for word in ok:
        if re.search(word, response):  # parla di quello che sa fare wolly
            print(random.choice(fare))
            textSpeech(random.choice(ecco) + random.choice(fare) + random.choice(vedere))
            return richiesta(talk())

    # stop immediately
    for word in niente:
        if re.search(word, response):
            print(random.choice(noproblem) + " resto in ascolto")
            textSpeech(random.choice(noproblem) + " resto in ascolto")
            return

    print(random.choice(err) + " resto in ascolto")
    textSpeech(random.choice(err) + " resto in ascolto")
    return


# each time you need to use microphone to get recognized speech as a string you call this method
def talk():
    # value to keep track of how many tries the bot needs to ask
    i = 2

    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 1)
            # add sound to help to know when to talk
            print("ascolto")
            playsound("../mp3/hearing.mp3")
            audio = r.listen(source, phrase_time_limit=4, timeout=None)

        try:
            response = r.recognize_google(audio, language="IT-IT")
            print(response)
            return response.lower()

        except sr.UnknownValueError:
            i = i - 1
            if i != 0:
                print("non ho capito, puoi ripetere?")
                textSpeech(random.choice(notundst))
            else:
                print("non riesco a capirti! vado a ricalibrare il mio microfono!")
                textSpeech(random.choice(noresponse) + " se hai ancora bisogno di me chiamami!")
                reface("doubtful")
                startTracking()
                return False


def chatInit():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 2)
            print("ascolto")
            audio = r.listen(source, timeout=None)

        try:
            text = r.recognize_google(audio, language="IT-IT")

            for word in wword:
                if re.search(word, text.lower()):
                    print(random.choice(responses) + random.choice(posso))
                    textSpeech(random.choice(responses) + random.choice(posso))
                    reface("wink")
                    response = talk()
                    if response is not False:
                        chat(response)


        except sr.UnknownValueError:
            print("---------Non ho capito---------")
        except sr.RequestError as e:
            print("Errore con il collegamento API: {0}".format(e))


def reface(espr):
    global process1
    process1.terminate()
    change(espr)


def change(espr):
    global espressione, process1
    espressione = espr
    process1 = multiprocessing.Process(target=face)
    process1.start()


# ----------fine secondo processo -----------

# ------------------PROCESSO 3------------------
# processo 3 tiene la faccia default in sfondo
def default():
    t = Tk()
    t.attributes('-fullscreen', True)
    direct = "/home/wolly/Desktop/WollyRaspberry/img/faces/default/6.png"
    label = Label(t)
    label.pack()
    im = ImageTk.PhotoImage(Image.open(direct))
    label.configure(image=im)
    t.mainloop()
# ----------fine processo 3--------------

# ---------- cam --------------
def cam():
    numFaces = 0
    # cascade classifier for face tracking
    face_cascade = cv2.CascadeClassifier('/home/wolly/Desktop/WollyRaspberry/lib/haarcascade_frontalface_default.xml')

    # inizializing camera capture
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200);
    time.sleep(1)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # infinite loop, it can be stopped with any desired input
    while True:

        # capture frame by frame
        ret, frame = cap.read()

        if ret == False:
            print("error getting image")
            continue

        # gray scaling for easier detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        # face detection for each frame
        faces = face_cascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))
        
def startCam():
    global process4
    process4 = multiprocessing.Process(target=cam)
    process4.start()

def stopCam():
    global process4
    process4.terminate()
    

if __name__ == '__main__':
    print('Press Ctrl+C to stop the program')
    process1 = multiprocessing.Process(target=face)
    process2 = multiprocessing.Process(target=chatInit)
    process3 = multiprocessing.Process(target=default)
    process3.start()
    process1.start()
    process2.start()
    time.sleep(1)
    signal.signal(signal.SIGINT, signal_handler)

