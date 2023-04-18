import random
import re
from frasiDialog import *
import time
from pygame import mixer
from motorsNew import *


# AGGIUNGERE WHILE true DENTRO OGNI DEF CHE PRENDE IN CONSIDERAZIONE UNA PAROLA NON COLLEGATA A NESSUNA AZIONE

# si: curiosità di wolly
# no: fatti assurdi
def curioso(response):
    global talk, textSpeech
    from chatbot import talk, textSpeech
    
    while True:
        if response is False:  # controllo si o no per curiosità wolly
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(magarifatto))
            textSpeech(random.choice(noproblem) + random.choice(magarifatto))
            return facs(talk())
        for word in ok:
            if re.search(word, response):  # curiosità su wolly
                flag = True  # flag necessario per ripetere curiosità saltando l'if erorre
                print(random.choice(curiosita))
                textSpeech(random.choice(curiosita))
                # reface("wink")
                # time.sleep(1)
                textSpeech("ne vuoi sentire un'altra?")
                
                while True:
                    response = talk()
                    if response is False:
                        return
                    elif re.search(r"\bno\b", response):
                        print(random.choice(noproblem) + random.choice(magarifatto))
                        textSpeech(random.choice(noproblem) + random.choice(magarifatto))
                        return facs(talk())
                    for wor in ok:
                        if re.search(wor, response):
                            print(random.choice(noproblem) + random.choice(curiosita))
                            textSpeech(random.choice(noproblem) + random.choice(curiosita))
                            # reface("wink")
                            # time.sleep(1)
                            textSpeech("ne vuoi sentire un'altra?")
                            flag = False

                    if flag:
                        error()
        error()
        response = talk()


# no : stop
# si : un'altra?
def facs(response):
    
    while True:
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
            textSpeech(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
            return
        for word in ok:
            if re.search(word, response):
                flag = True
                print(random.choice(realfacs))
                textSpeech(random.choice(realfacs))
                # reface("wink")
                # time.sleep(1)
                textSpeech("ne vuoi sentire un altro?")
                
                while True:
                    response = talk()
                    if response is False:
                        return
                    elif re.search(r"\bno\b", response):
                        print(random.choice(noproblem))
                        textSpeech(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
                        # reface("wink")
                        return
                    for wor in ok:
                        if re.search(wor, response):
                            print("va bene, " + random.choice(realfacs))
                            textSpeech(random.choice(noproblem) + random.choice(realfacs))
                            # reface("wink")
                            textSpeech("ne vuoi sentire un altro?")
                            flag = False

                    if flag:
                        error()
        error()
        response = talk()

# no: chiede se vuole sentire una curiosità
# si: chiede cosa vuole vedere
# cantare V
# ballare V
# emozioni (alberto)
# mimo V
# barzellette V
# indovinelli V
def richiesta(response):
    global talk, textSpeech, playsound
    from chatbot import talk, textSpeech, playsound

    while True:
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            return curioso(talk())
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem) + " cosa vorresti vedere?")
                textSpeech(random.choice(noproblem) + " cosa vorresti vedere?")  
                
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
        response = talk()
    


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
            return curioso(talk())
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem) + "cosa vorresti vedere?")
                textSpeech(random.choice(noproblem) + "cosa vorresti vedere?")  # aggiungere eventi
                
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


def cantare():
    canta = ["../../mp3/alien_sound.mp3"]
    playsound(random.choice(canta))
    # reface("sing")
    # reface("sing")
    # reface("sing")
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
        #reface("crazy")
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
        # reface("crazy")
        playsound("../../mp3/joke.mp3")
        textSpeech("ne vuoi sentire un'altra?")
        flag = True
        response = talk()
        
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem))
            textSpeech(random.choice(noproblem))
            # reface("wink")
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
            sbagliato = False
            return ripMimo()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")

            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    return ritentaMimo()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + mimo[mima][0])
                        textSpeech("la risposta era " + mimo[mima][0])
                        return ripMimo()
                error()
                    
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            return ritentaMimo()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + mimo[mima][0])
                textSpeech("la risposta era " + mimo[mima][0])
                return ripMimo()
        error()


def ritentaMimo():
    global mima, sol
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
            return ripMimo()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")

            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    return ritentaMimo()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + mimo[mima][0])
                        textSpeech("la risposta era " + mimo[mima][0])
                        return ripMimo()
                error()
            
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            return ritentaMimo()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
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
    response = talk()
    soluzione = indovinelli[ind]
    if response is False: 
        return
    for word in soluzione:
        if re.search(word, response):
            risp = word
            print("bene, la risposta era proprio " + risp)
            textSpeech("bene, la risposta era proprio " + risp)
            return ripInd()
    for word in nonSo:
        if re.search(word, response):
            print("non ti preoccupare! Vuoi che ti dica la risposta?")
            textSpeech("non ti preoccupare! Vuoi che ti dica la risposta?")
            while True:
                response = talk()
                if response is False:
                    return
                if re.search(r"\bno\b", response):
                    print("d'accordo, ti lascio riprovare")
                    textSpeech("d'accordo, ti lascio riprovare")
                    return ritenta()
                for wor in ok:
                    if re.search(wor, response):
                        print("la risposta era " + indovinelli[ind][0])
                        textSpeech("la risposta era " + indovinelli[ind][0])
                        return ripInd()
                error()
    print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
    
    while True:
        response = talk()
        if response is False:
            return
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
            return ritenta()
        for wor in ok:
            if re.search(wor, response):
                print("la risposta era " + indovinelli[ind][0])
                textSpeech("la risposta era " + indovinelli[ind][0])
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
            sbagliato = False
            return ripInd()
        
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
                return ripInd()
        if re.search(r"\bno\b", response):
            print("d'accordo, ti lascio riprovare")
            textSpeech("d'accordo, ti lascio riprovare")
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
        i+=1
            
                
def error():
    from chatbot import textSpeech
    print(random.choice(err) + " potresti ripetere?")
    textSpeech(random.choice(err) + " potresti ripetere?")
