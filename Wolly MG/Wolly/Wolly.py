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

# import tracking
import cv2

#import AppWrite
from appwrite.client import Client
from appwrite.services.database import Database
from appwrite.services.storage import Storage

import urllib3

# import dialog
import random
import re
from frasiDialog import *
import time
from pygame import mixer
from motorsNew import *


# signal handler per ctrl+c alla fine del programma
def signal_handler(sig, frame):
    global process1, process3
    print('You ended the program')
    process1.terminate()
    process3.terminate()
    time.sleep(3)
    sys.exit(0)

# ---------fine signal handler---------


#--------------inizio configurazione appwrite----------------

# ENDPOINT = 'https://9225438084d8.ngrok.io/v1'
# PROJECT_ID = '5fa7e32a5133e'
# API_KEY = '51935101e4598b8a6c6722c919757eab00614c5cf07320d2d4e894a9fc178dfc6e44f9811ac2426d16027197435c663f25665f5f1661aa00d345fb8bef2a177c2ddbee5727e26cb348c99f5a54507f81897a13602b2af124255f7375867cf183c0afbedaa361b4eed1581d94366a327f81588fe233de9282e098ff7207530301'

ENDPOINT = 'http://app.wolly.di.unito.it/v1'
PROJECT_ID = '60cc80c053637'
API_KEY = '15735ace9c277263e68936020652843ed788409e79f9f2ca745fe4179d82e7f25de27e83dee7161e9b747540161f0902ba077f0e10844ac2bbdc639386e4a98de2dc5c3db62356d7cb3003e3bb4cd881e065b3f5bdcae8ad45b546e7a02dbac0f2d88a6c6df411611c19673e3e498cdaefcfcd0d0d055d92bf531dd3b6e350d8'

client = Client()

client.set_endpoint(ENDPOINT)
client.set_project(PROJECT_ID)
client.set_key(API_KEY)
# client.add_header("Origin", ENDPOINT)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

collectionId = '60d2f79f5ffc1'
userId = '60d2f78729a5c'

dateOldMossa = ""

#--------------fine configurazione appwrite----------------


# ----------------processo master---------------
def print_green(prt):
    print("\033[32;1m" + str(prt) + "\033[0m")
    
def execJson(response):
    global dateOldMossa
    document = response["documents"][0]
    print('eta: ' + document["eta"])
    if document["eta"] != dateOldMossa:
        dateOldMossa = document['eta']
        print('Nuovo comando')
        exec(document["mosse"])

def list_doc():
    database = Database(client)
    print_green("Running List Document API")
    response = database.list_documents(collectionId)
    execJson(response)

def master():
    global process2
    while True:
        process2 = multiprocessing.Process(target=face)
        process2.start()
        chat = False
        database = Database(client)
        response = database.list_documents(collectionId)
        document = response["documents"][0]
        autonomo = document["autonomo"]
        
        if autonomo:
            print("autonomo")
            chat = track()
            if chat == True:
                print("TTS")
                textSpeech(random.choice(ciao) + random.choice(ascolto) + random.choice(quando))
                process4 = multiprocessing.Process(target=chatInit)
                process4.start()
        elif not autonomo:
            print("blockly")
            list_doc()
            print('old mossa: ' + dateOldMossa)

        while True:
            database = Database(client)
            response = database.list_documents(collectionId)
            document = response["documents"][0]
            autonomia = document["autonomo"]
            
            if not autonomo:
                list_doc()
                print('old mossa: ' + dateOldMossa)

            if autonomo != autonomia:
                if chat:
                    process2.terminate()
                    print("close proc") 
                    process4.terminate()
                else:
                    process2.terminate()
                break

# ----------------fine processo master---------------


# ------------------PROCESSO 1------------------
# processo 1 tiene la faccia default in sfondo
def default():
    t = Tk()
    t.attributes('-fullscreen', True)
    direct = "/home/wolly/Desktop/WollyRaspberry/img/faces/default/6.png"
    label = Label(t)
    label.pack()
    im = ImageTk.PhotoImage(Image.open(direct))
    label.configure(image=im)
    t.mainloop()
# ----------fine processo 1--------------

# -------------TRACK FACE proc4-----------------
#face tracking che dopo aver visto una persona ascolta se viene chiamato

def track():
    global cap
    # cascade classifier for face tracking
    face_cascade = cv2.CascadeClassifier('/home/wolly/Desktop/WollyRaspberry/lib/haarcascade_frontalface_default.xml')

    # inizializing camera capture
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
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
        
        print(len(faces))

        # if the number of faces is greater than 0 wolly will introduce himself
        if 0 < len(faces):
            cap.release()
            return 1
            

def chatInit():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 1)
            print("ascolto")
            audio = r.listen(source, timeout=None, phrase_time_limit=10)

        try:
            text = r.recognize_google(audio, language="IT-IT")

            for word in wword:
                if re.search(word, text.lower()):
                    print(random.choice(responses) + random.choice(posso))
                    textSpeech(random.choice(responses) + random.choice(posso))
                    reface("happy", 0)
                    return chat()  # aggiungere variabile per uscire dall'ascolto chat

        except sr.UnknownValueError:
            print("---------Non ho capito---------")
        except sr.RequestError as e:
            print("Errore con il collegamento API: {0}".format(e))
            
#-----------------fine track face proc4------------------
            

# ------------------PROCESSO 2------------------
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

# ------------------metodi per la chat------------------
# terzo processo chat, usa reface per cambiare faccia
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


# each time you need to use microphone to get recognized speech as a string you call this method
def talk():
    # value to keep track of how many tries the bot needs to ask
    i = 3

    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 0.8)
            # add sound to help to know when to talk
            playsound("../../mp3/hearing.mp3")
            time.sleep(1.3)
            print("ascolto")
            audio = r.listen(source, timeout=None, phrase_time_limit = 8)

        try:
            response = r.recognize_google(audio, language="IT-IT")
            print(response)
            return response.lower()

        except sr.UnknownValueError:
            i = i - 1
            if i != 0:
                print(random.choice(notundst))
                textSpeech(random.choice(notundst))
            else:
                print("non riesco a capirti! vado a ricalibrare il mio microfono!")
                textSpeech(random.choice(noresponse) + " se hai ancora bisogno di me chiamami!")
                reface("doubtful",0)
                return False
            
            
# hardcoded chatbot 
def chat():
    global textSpeech
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            reface("wink",0)
            return curioso()
        for word in ok:
            if re.search(word, response):  # parla di quello che sa fare wolly
                print(random.choice(fare))
                textSpeech(random.choice(ecco) + random.choice(fare) + random.choice(vedere))
                reface("happy", 0)
                return richiesta()

        # stop immediately
        for word in niente:
            if word in response:
                print(random.choice(noproblem) + " resto in ascolto")
                textSpeech(random.choice(noproblem) + " resto in ascolto")
                reface("sleepy", 5)
                return
            
        error()


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

# ----------fine metodi per la chat-----------


# ---------------------DIALOG---------------------
# si: curiosità di wolly
# no: fatti assurdi
def curioso():
    
    while True:
        flag = True
        response = talk()
        if response is False:  # controllo si o no per curiosità wolly
            return
        elif re.search(r"\bno\b", response):
            reface("sad", 5)
            print(random.choice(noproblem) + random.choice(magarifatto))
            textSpeech(random.choice(noproblem) + random.choice(magarifatto))
            return facs()
        for word in ok:
            if re.search(word, response):  # curiosità su wolly
                flag = True  # flag necessario per ripetere curiosità saltando l'if erorre
                print(random.choice(curiosita))
                textSpeech(random.choice(curiosita))
                reface("wink", 4)
                print("ne vuoi sentire un'altra?")
                textSpeech("ne vuoi sentire un'altra?")
                flag = False
        if flag:  
            error()


# no : stop
# si : un'altra?
def facs():
    
    while True:
        response = talk()
        flag = True
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            reface("sad", 5)
            print(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
            textSpeech(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
            reface("sleepy", 5)
            return
        for word in ok:
            if re.search(word, response):
                flag = True
                print(random.choice(realfacs))
                textSpeech(random.choice(realfacs))
                reface("surprise", 5)
                print("ne vuoi sentire un altro?")
                textSpeech("ne vuoi sentire un altro?")
                flag = False
                
        if flag:
            error()
    

# no: chiede se vuole sentire una curiosità
# si: chiede cosa vuole vedere
# cantare V
# ballare V
# emozioni (alberto)
# mimo V
# barzellette V
# indovinelli V
def richiesta():

    while True:
        response = talk()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            reface("sad", 5)
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            return curioso()
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem) + " cosa vorresti vedere?")
                textSpeech(random.choice(noproblem) + " cosa vorresti vedere?")
                reface("happy", 0)
                
                while True:
                    response = talk()
                    if response is False:
                        return
                    for word in barze:
                        if re.search(word, response):
                            print(random.choice(noproblem))
                            textSpeech(random.choice(noproblem))
                            return barzelletta()
                    for word in indovina:
                        if re.search(word, response):
                            print(random.choice(noproblem))
                            textSpeech(random.choice(noproblem))
                            return indovinello()
                    for word in imita:
                        if re.search(word, response):
                            print(random.choice(noproblem))
                            textSpeech(random.choice(noproblem))
                            return imitare()
                    for word in ballo:
                        if re.search(word, response):
                            print(random.choice(noproblem) + "adesso mi scateno un po'")
                            textSpeech(random.choice(noproblem) + "adesso mi scateno un po'")
                            return ballare()
                    for word in canto:
                        if re.search(word, response):
                            print(random.choice(noproblem) + "devo un attimo scaldare l'altoparlante")
                            textSpeech(random.choice(noproblem) + "devo un attimo scaldare l'altoparlante")
                            return cantare()
                    error()  
        error()


def ripRichiesta():
    print(" vuoi vedere altro?")
    textSpeech(" vuoi vedere altro?")
    
    while True:
        print("eccomi")
        response = talk()
        if response is False:
                return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            reface("wink",0)
            return curioso()
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem) + "cosa vorresti vedere?")
                textSpeech(random.choice(noproblem) + "cosa vorresti vedere?")  # aggiungere eventi
                reface("happy", 0)
                
                while True:
                    response = talk()
                    if response is False:
                        return
                    for word in barze:
                        if re.search(word, response):
                            print(random.choice(noproblem))
                            textSpeech(random.choice(noproblem))
                            return barzelletta()
                    for word in indovina:
                        if re.search(word, response):
                            print(random.choice(noproblem))
                            textSpeech(random.choice(noproblem))
                            return indovinello()
                    for word in imita:
                        if re.search(word, response):
                            print(random.choice(noproblem))
                            textSpeech(random.choice(noproblem))
                            return imitare()
                    for word in ballo:
                        if re.search(word, response):
                            print(random.choice(noproblem) + "adesso mi scateno un po'")
                            textSpeech(random.choice(noproblem) + "adesso mi scateno un po'")
                            return ballare()
                    for word in canto:
                        if re.search(word, response):
                            print(random.choice(noproblem) + "devo un attimo scaldare l'altoparlante")
                            textSpeech(random.choice(noproblem) + "devo un attimo scaldare l'altoparlante")
                            return cantare()
                    error()
        error()


def cantare():
    movimento = [0, 1]
    durata = [0.2, 0.1]
    canta = ["../../mp3/alien_sound.mp3", "../../mp3/pavarotti.mp3"]
    mixer.init()
    mixer.music.load(random.choice(canta))
    mixer.music.play()
    c = 0
    reface("sing",0)
    while c < 35:
        if c == 10 or c == 18:
            reface("sing",0)  
        destra(random.choice(durata), 0.46)
        sinistra(random.choice(durata), 0.46)
        c += 1
       
    mixer.quit()
    ripRichiesta()


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
    ripRichiesta()
    
    
def barzelletta():
    while True:
        print(random.choice(battuta))
        textSpeech(random.choice(battuta))
        reface("crazy",0)
        playsound("../../mp3/joke.mp3")
        textSpeech("ne vuoi sentire un'altra?")
        flag = True
        response = talk()
        
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem))
            textSpeech(random.choice(noproblem))
            reface("wink",4)
            return ripRichiesta()
        for wor in ok:
            if re.search(wor, response):
                print(random.choice(noproblem))
                textSpeech(random.choice(noproblem))
                flag = False
        if flag:
            error()
            


def imitare():
    global mima, sol
    print("ecco come funziona il gioco, adesso imiterò un suono e tu dovrai dirmi che suono è")
    textSpeech("ecco come funziona il gioco, adesso imiterò un suono e tu dovrai dirmi che suono è")
    
    mima = random.choice(mimata)
    sol = mimo[mima]
    reface("sing",0)
    playsound(mima)
    print("cosa ho imitato?")
    textSpeech("cosa ho imitato?")
    
    response=talk()
    if response is False: 
        return
    for word in sol:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            reface("happy",4)
            sbagliato = False
            return ripMimo()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            reface("wink",0)

            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    reface("wink",4)
                    return ritentaMimo()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + mimo[mima][0])
                        textSpeech("la risposta era " + mimo[mima][0])
                        reface("happy",3)
                        return ripMimo()
                error()
    reface("sad",4)                
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            reface("wink",3)
            return ritentaMimo()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + mimo[mima][0])
                textSpeech("la risposta era " + mimo[mima][0])
                reface("happy",3)
                return ripMimo()
        error()


def ritentaMimo():
    global mima, sol
    reface("sing",0)
    playsound(mima)
    print("cosa ho imitato?")
    textSpeech("cosa ho imitato?")
    response = talk()
    if response is False: 
        return
    for word in sol:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            reface("happy",3)
            return ripMimo()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            reface("wink",0)

            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    reface("wink",0)
                    return ritentaMimo()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + mimo[mima][0])
                        textSpeech("la risposta era " + mimo[mima][0])
                        reface("happy",3)
                        return ripMimo()
                error()
            
    reface("sad",4)
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            reface("wink",3)
            return ritentaMimo()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
                reface("happy",3)
                return ripMimo()
        error()
     
     
def ripMimo():
    global mima, sol
    print("vuoi rigiocare?")
    textSpeech("vuoi rigiocare?")
    
    while True:
        response = talk()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem))
            textSpeech(random.choice(noproblem))
            return ripRichiesta()
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem))
                textSpeech(random.choice(noproblem))
                reface("happy",3)
                return imitare()
        error()
         
       
def indovinello():
    global ind, soluzione
    
    ind = random.choice(indo)
    textSpeech(ind)
    reface("surprise",0)
    response = talk()
    soluzione = indovinelli[ind]
    if response is False: 
        return
    for word in soluzione:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            reface("happy",3)
            return ripInd()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            reface("wink",0)
            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    reface("wink",3)
                    return ritenta()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + indovinelli[ind][0])
                        textSpeech("la risposta era " + indovinelli[ind][0])
                        reface("happy",0)
                        return ripInd()
                error()
                
    reface("sad",4)
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            reface("wink",3)
            return ritenta()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
                reface("happy",3)
                return ripInd()
        error() 
     
            
        
def ritenta():
    global soluzione, ind
    
    print("ecco l'indovinello, " + ind)
    textSpeech("ecco l'indovinello, " + ind)
    reface("wink",0)
    response = talk()
    if response is False: 
            return
    for word in soluzione:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            reface("happy",3)
            sbagliato = False
            return ripInd()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            reface("wink",0)
            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    reface("wink",3)
                    return ritenta()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + indovinelli[ind][0])
                        textSpeech("la risposta era " + indovinelli[ind][0])
                        reface("happy",3)
                        return ripInd()
                error()
    reface("sad",4)  
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    while True:
        response = talk()
        if response is False:
            return
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
                reface("happy",3)
                return ripInd()
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            reface("wink",3)
            return ritenta()
        error()
    
    
def ripInd():
    print("ne vuoi sentire un'altro?")
    textSpeech("ne vuoi sentire un'altro?")
    reface("happy",0)
    
    while True:
        response = talk()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem))
            textSpeech(random.choice(noproblem))
            return ripRichiesta()
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem))
                textSpeech(random.choice(noproblem))
                reface("wink",4)
                return indovinello()
        error()
            
                
def error():
    print(random.choice(err) + " Ripeti quello che hai detto")
    textSpeech(random.choice(err) + " Ripeti quello che hai detto")
    
#----------------------------------------------------------
    

if __name__ == '__main__':
    print('Press Ctrl+C to stop the program')
    process1 = multiprocessing.Process(target=default)  # faccia in background per coprire lo schermo
    process3 = multiprocessing.Process(target=master) # controllo se wolly è autonomo o no, crea processo faccia che si chiude e si riapre ogni volta che si cambia espressione
    process1.start()
    time.sleep(2)
    process3.start()
    signal.signal(signal.SIGINT, signal_handler)


