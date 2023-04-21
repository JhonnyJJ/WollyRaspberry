import random
import re
from frasiDialog import *
import time
from pygame import mixer
from motorsNew import *


# AGGIUNGERE WHILE true DENTRO OGNI DEF CHE PRENDE IN CONSIDERAZIONE UNA PAROLA NON COLLEGATA A NESSUNA AZIONE

# si: curiosità di wolly
# no: fatti assurdi
def curioso():
    from chatbot import textSpeech, playsound
    global textSpeech, playsound
    
    while True:
        response = input()
        if response is False:  # controllo si o no per curiosità wolly
            return
        elif re.search(r"\bno\b", response):
            #("sad", 5)
            print(random.choice(noproblem) + random.choice(magarifatto))
            textSpeech(random.choice(noproblem) + random.choice(magarifatto))
            return facs()
        for word in ok:
            if re.search(word, response):  # curiosità su wolly
                flag = True  # flag necessario per ripetere curiosità saltando l'if erorre
                print(random.choice(curiosita))
                textSpeech(random.choice(curiosita))
                #("wink", 4)
                print("ne vuoi sentire un'altra?")
                textSpeech("ne vuoi sentire un'altra?")
                
        error()


# no : stop
# si : un'altra?
def facs():
    
    while True:
        response = input()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            #("sad", 5)
            print(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
            textSpeech(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
            #("sleepy", 0)
            return
        for word in ok:
            if re.search(word, response):
                flag = True
                print(random.choice(realfacs))
                textSpeech(random.choice(realfacs))
                #("surprise", 5)
                textSpeech("ne vuoi sentire un altro?")
                
                while True:
                    response = input()
                    if response is False:
                        return
                    elif re.search(r"\bno\b", response):
                        print(random.choice(noproblem))
                        textSpeech(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
                        #("wink", 0)
                        return
                    for wor in ok:
                        if re.search(wor, response):
                            print("va bene, " + random.choice(realfacs))
                            textSpeech(random.choice(noproblem) + random.choice(realfacs))
                            #("surprise", 5)
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
    from chatbot import textSpeech, playsound
    global textSpeech, playsound
    
    while True:
        response = input()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            #("sad", 5)
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            return curioso()
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem) + " cosa vorresti vedere?")
                textSpeech(random.choice(noproblem) + " cosa vorresti vedere?")
                #("happy", 0)
                print("prova")
                
                while True:
                    response = input()
                    print(response)
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
        response = input()
        if response is False:
                return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            #("wink",0)
            return curioso()
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem) + "cosa vorresti vedere?")
                textSpeech(random.choice(noproblem) + "cosa vorresti vedere?")  # aggiungere eventi
                #("happy", 0)
                
                while True:
                    response = input()
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
#     #("sing",0)
#     while c < 35:
#         if c == 10 or c == 18:
#             #("sing",0)  
#         destra(random.choice(durata), 0.46)
#         sinistra(random.choice(durata), 0.46)
#         c += 1
#        
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
#     c = 0
#     #("crazy",0)
#     while c < 36:
#         if c == 20:
#             #("crazy",0)
#         if random.choice(movimento) == 1:
#            destra(random.choice(durata), random.choice(velocita))
#         else:
#            sinistra(random.choice(durata), random.choice(velocita))
#         c += 1
    mixer.quit()
    ripRichiesta()
    
    
def barzelletta():
    while True:
        print(random.choice(battuta))
        textSpeech(random.choice(battuta))
        #("crazy",0)
        playsound("../../mp3/joke.mp3")
        textSpeech("ne vuoi sentire un'altra?")
        flag = True
        response = input()
        
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem))
            textSpeech(random.choice(noproblem))
            #("wink",4)
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
    #("sing",0)
    playsound(mima)
    print("cosa ho imitato?")
    textSpeech("cosa ho imitato?")
    
    response=input()
    if response is False: 
        return
    for word in sol:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            #("happy",4)
            sbagliato = False
            return ripMimo()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            #("wink",0)

            while True:
                response = input()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    #("wink",4)
                    return ritentaMimo()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + mimo[mima][0])
                        textSpeech("la risposta era " + mimo[mima][0])
                        #("happy",3)
                        return ripMimo()
                error()
    #("sad",4)                
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    
    while True:
        response = input()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            #("wink",3)
            return ritentaMimo()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + mimo[mima][0])
                textSpeech("la risposta era " + mimo[mima][0])
                #("happy",3)
                return ripMimo()
        error()


def ritentaMimo():
    global mima, sol
    #("sing",0)
    playsound(mima)
    print("cosa ho imitato?")
    textSpeech("cosa ho imitato?")
    response = input()
    if response is False: 
        return
    for word in sol:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            #("happy",3)
            return ripMimo()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            #("wink",0)

            while True:
                response = input()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    #("wink",0)
                    return ritentaMimo()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + mimo[mima][0])
                        textSpeech("la risposta era " + mimo[mima][0])
                        #("happy",3)
                        return ripMimo()
                error()
            
    #("sad",4)
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    while True:
        response = input()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            #("wink",3)
            return ritentaMimo()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
                #("happy",3)
                return ripMimo()
        error()
     
     
def ripMimo():
    global mima, sol
    print("vuoi rigiocare?")
    textSpeech("vuoi rigiocare?")
    
    while True:
        response = input()
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
                #("happy",3)
                return imitare()
        error()
         
       
def indovinello():
    global ind, soluzione
    
    ind = random.choice(indo)
    textSpeech(ind)
    #("surprise",0)
    response = input()
    soluzione = indovinelli[ind]
    if response is False: 
        return
    for word in soluzione:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            #("happy",3)
            return ripInd()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            #("wink",0)
            while True:
                response = input()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    #("wink",3)
                    return ritenta()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + indovinelli[ind][0])
                        textSpeech("la risposta era " + indovinelli[ind][0])
                        #("happy",0)
                        return ripInd()
                error()
                
    #("sad",4)
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    while True:
        response = input()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            #("wink",3)
            return ritenta()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
                #("happy",3)
                return ripInd()
        error() 
     
            
        
def ritenta():
    global soluzione, ind
    
    print("ecco l'indovinello, " + ind)
    textSpeech("ecco l'indovinello, " + ind)
    #("wink",0)
    response = input()
    if response is False: 
            return
    for word in soluzione:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            #("happy",3)
            sbagliato = False
            return ripInd()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            #("wink",0)
            while True:
                response = input()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    #("wink",3)
                    return ritenta()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + indovinelli[ind][0])
                        textSpeech("la risposta era " + indovinelli[ind][0])
                        #("happy",3)
                        return ripInd()
                error()
    #("sad",4)  
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    while True:
        response = input()
        if response is False:
            return
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
                #("happy",3)
                return ripInd()
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            #("wink",3)
            return ritenta()
        error()
    
    
def ripInd():
    print("ne vuoi sentire un'altro?")
    textSpeech("ne vuoi sentire un'altro?")
    #("happy",0)
    
    while True:
        response = input()
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
                #("wink",4)
                return indovinello()
        error()
            
                
def error():
    print(random.choice(err) + " Ripeti quello che hai detto")
    textSpeech(random.choice(err) + " Ripeti quello che hai detto")

