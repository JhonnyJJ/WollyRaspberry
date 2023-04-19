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

# import dialog
import random
import re
from frasiDialog import *
import time
from pygame import mixer
from motorsNew import *


# signal handler per ctrl+c alla fine del programma
def signal_handler(sig, frame):
    print('You ended the program')
    process1.terminate()
    process2.terminate()
    process3.terminate()
    time.sleep(3)
    sys.exit(0)

# ---------fine signal handler---------


# ------------------PROCESSO 1------------------
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
# ----------fine processo 1--------------


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

# ------------------PROCESSO 3------------------
# terzo processo chat, usa reface per cambiare faccia
def playsound(filepath):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.01)
    # pygame.quit()   #windows debug


def textSpeech(text):
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    reface("speaker")
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
            time.sleep(0.8)
            print("ascolto")
            audio = r.listen(source, phrase_time_limit=6, timeout=None)

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
                return False
            
            
# hardcoded chatbot 
def chat():  
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            reface("wink")
            return curioso()
        for word in ok:
            if re.search(word, response):  # parla di quello che sa fare wolly
                print(random.choice(fare))
                textSpeech(random.choice(ecco) + random.choice(fare) + random.choice(vedere))
                reface("happy")
                return richiesta()

        # stop immediately
        for word in niente:
            if word in response:
                print(random.choice(noproblem) + " resto in ascolto")
                textSpeech(random.choice(noproblem) + " resto in ascolto")
                reface("sleepy")
                return
            
        error()


def chatInit():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 1)
            print("ascolto")
            audio = r.listen(source, timeout=None, phrase_time_limit=6)

        try:
            text = r.recognize_google(audio, language="IT-IT")

            for word in wword:
                if re.search(word, text.lower()):
                    print(random.choice(responses))
                    textSpeech(random.choice(responses))
                    reface("happy")
                    time.sleep(7)
                    print(random.choice(posso))
                    textSpeech(random.choice(posso))
                    chat()

        except sr.UnknownValueError:
            print("---------Non ho capito---------")
        except sr.RequestError as e:
            print("Errore con il collegamento API: {0}".format(e))


def reface(espr):
    global process2
    process2.terminate()
    change(espr)


def change(espr):
    global espressione, process2
    espressione = espr
    process2 = multiprocessing.Process(target=face)
    process2.start()

# ----------fine secondo processo -----------

# ---------------------DIALOG---------------------
# si: curiosità di wolly
# no: fatti assurdi
def curioso():
    
    while True:
        response = talk()
        if response is False:  # controllo si o no per curiosità wolly
            return
        elif re.search(r"\bno\b", response):
            reface("sad")
            time.sleep(7)
            print(random.choice(noproblem) + random.choice(magarifatto))
            textSpeech(random.choice(noproblem) + random.choice(magarifatto))
            return facs()
        for word in ok:
            if re.search(word, response):  # curiosità su wolly
                flag = True  # flag necessario per ripetere curiosità saltando l'if erorre
                print(random.choice(curiosita))
                textSpeech(random.choice(curiosita))
                reface("wink")
                time.sleep(5)
                textSpeech("ne vuoi sentire un'altra?")
                
                while True:
                    response = talk()
                    if response is False:
                        return
                    elif re.search(r"\bno\b", response):
                        print(random.choice(noproblem) + random.choice(magarifatto))
                        textSpeech(random.choice(noproblem) + random.choice(magarifatto))
                        return facs()
                    for wor in ok:
                        if re.search(wor, response):
                            print(random.choice(noproblem) + random.choice(curiosita))
                            textSpeech(random.choice(noproblem) + random.choice(curiosita))
                            reface("wink")
                            time.sleep(5)
                            textSpeech("ne vuoi sentire un'altra?")
                            flag = False

                    if flag:
                        error()
        error()
        response = talk()


# no : stop
# si : un'altra?
def facs():
    
    while True:
        response = talk()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
            textSpeech(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
            reface("sleepy")
            return
        for word in ok:
            if re.search(word, response):
                flag = True
                print(random.choice(realfacs))
                textSpeech(random.choice(realfacs))
                reface("surprise")
                time.sleep(7)
                textSpeech("ne vuoi sentire un altro?")
                
                while True:
                    response = talk()
                    if response is False:
                        return
                    elif re.search(r"\bno\b", response):
                        print(random.choice(noproblem))
                        textSpeech(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
                        reface("wink")
                        return
                    for wor in ok:
                        if re.search(wor, response):
                            print("va bene, " + random.choice(realfacs))
                            textSpeech(random.choice(noproblem) + random.choice(realfacs))
                            reface("surprise")
                            tiem.sleep(7)
                            textSpeech("ne vuoi sentire un altro?")
                            flag = False

                    if flag:
                        error()
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
            reface("sad")
            time.sleep(7)
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            return curioso()
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem) + " cosa vorresti vedere?")
                textSpeech(random.choice(noproblem) + " cosa vorresti vedere?")
                reface("happy")
                time.sleep(3)
                
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
                            print(random.choice(noproblem))
                            textSpeech(random.choice(noproblem))
                            return ballare()
                    for word in canto:
                        if re.search(word, response):
                            print(random.choice(noproblem))
                            textSpeech(random.choice(noproblem))
                            return cantare()
                    error()  
        error()


def ripRichiesta():
    print(" vuoi vedere altro?")
    textSpeech(" vuoi vedere altro?")
    
    while True:
        response = talk()
        if response is False:
                return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            reface("wink")
            return curioso()
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem) + "cosa vorresti vedere?")
                textSpeech(random.choice(noproblem) + "cosa vorresti vedere?")  # aggiungere eventi
                reaface("happy")
                time.sleep(3)
                
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
    canta = ["../../mp3/alien_sound.mp3", "../../mp3/pavarotti.mp3"]
    playsound(random.choice(canta))
    reface("sing")
    ripRichiesta()


def ballare():
    canzoni = ["../../mp3/mii.mp3", "../../mp3/jojos.mp3"]
    durata = [0.5, 0.4, 0.3]
    velocita = [0.5, 0.55]
    movimento = [0, 1]
    mixer.init()
    mixer.music.load(random.choice(canzoni))
    mixer.music.play()
    c = 0
    while c < 30:
        if c == 10:
            reface("crazy")
        if random.choice(movimento) == 1:
           destra(random.choice(durata), random.choice(velocita))
        else:
           sinistra(random.choice(durata), random.choice(velocita))
        c += 1
    ripRichiesta()
    
    
def barzelletta():
    while True:
        print(random.choice(battuta))
        textSpeech(random.choice(battuta))
        reface("crazy")
        playsound("../../mp3/joke.mp3")
        textSpeech("ne vuoi sentire un'altra?")
        flag = True
        response = talk()
        
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem))
            textSpeech(random.choice(noproblem))
            reface("wink")
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
    reface("sing")
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
            reface("happy")
            time.sleep(3)
            sbagliato = False
            return ripMimo()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            reface("wink")

            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    reface("wink")
                    time.sleep(3)
                    return ritentaMimo()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + mimo[mima][0])
                        textSpeech("la risposta era " + mimo[mima][0])
                        reface("happy")
                        time.sleep(3)
                        return ripMimo()
                error()
                    
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    reface("sad")
    
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            reface("wink")
            time.sleep(3)
            return ritentaMimo()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + mimo[mima][0])
                textSpeech("la risposta era " + mimo[mima][0])
                reface("happy")
                time.sleep(3)
                return ripMimo()
        error()


def ritentaMimo():
    global mima, sol
    reface("sing")
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
            reface("happy")
            time.sleep(3)
            return ripMimo()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            reface("wink")

            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    reface("wink")
                    time.sleep(3)
                    return ritentaMimo()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + mimo[mima][0])
                        textSpeech("la risposta era " + mimo[mima][0])
                        reface("happy")
                        time.sleep(3)
                        return ripMimo()
                error()
            
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    reface("happy")
    
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            reface("wink")
            time.sleep(3)
            return ritentaMimo()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
                reface("happy")
                time.sleep(3)
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
                return imitare()
        error()
         
       
def indovinello():
    global ind, soluzione
    
    ind = random.choice(indo)
    textSpeech(ind)
    reface("surprise")
    response = talk()
    soluzione = indovinelli[ind]
    if response is False: 
        return
    for word in soluzione:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            reface("happy")
            time.sleep(3)
            return ripInd()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            reface("wink")
            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    reaface("wink")
                    time.sleep(3)
                    return ritenta()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + indovinelli[ind][0])
                        textSpeech("la risposta era " + indovinelli[ind][0])
                        reface("happy")
                        return ripInd()
                error()
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    reface("sad")
    
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            reaface("wink")
            time.sleep(3)
            return ritenta()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
                reaface("happy")
                time.sleep(3)
                return ripInd()
        error() 
     
            
        
def ritenta():
    global soluzione, ind
    
    print("ecco l'indovinello, " + ind)
    textSpeech("ecco l'indovinello, " + ind)
    response = talk()
    if response is False: 
            return
    for word in soluzione:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            reface("happy")
            time.sleep(3)
            sbagliato = False
            return ripInd()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            reface("wink")
            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    reaface("wink")
                    time.sleep(3)
                    return ritenta()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + indovinelli[ind][0])
                        textSpeech("la risposta era " + indovinelli[ind][0])
                        reface("happy")
                        return ripInd()
                error()
        
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    reface("sad")
    
    while True:
        response = talk()
        if response is False:
            return
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
                reface("happy")
                time.sleep(3)
                return ripInd()
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            reface("wink")
            time.sleep(3)
            return ritenta()
        error()
    
    
def ripInd():
    print("ne vuoi sentire un'altro?")
    textSpeech("ne vuoi sentire un'altro?")
    
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
                return indovinello()
        error()
            
                
def error():
    print(random.choice(err) + " potresti ripetere?")
    textSpeech(random.choice(err) + " potresti ripetere?")
    
#----------------------------------------------------------
    

if __name__ == '__main__':
    print('Press Ctrl+C to stop the program')
    process2 = multiprocessing.Process(target=face)
    process3 = multiprocessing.Process(target=chatInit)
    process1 = multiprocessing.Process(target=default)
    process1.start()
    process2.start()
    process3.start()
    time.sleep(1)
    signal.signal(signal.SIGINT, signal_handler)


