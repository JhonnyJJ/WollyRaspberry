import random
import re
from frasi import *
import time


# AGGIUNGERE WHILE true DENTRO OGNI DEF CHE PRENDE IN CONSIDERAZIONE UNA PAROLA NON COLLEGATA A NESSUNA AZIONE

# si: curiosità di wolly
# no: fatti assurdi
def curioso(response):
    from chatbot import talk, textSpeech
    global talk, textSpeech
    if response is False:  # controllo si o no per curiosità wolly
        return
    elif re.search(r"\bno\b", response):
        print(random.choice(noproblem) + random.choice(magarifatto))
        textSpeech(random.choice(noproblem) + random.choice(magarifatto))
        return facs(talk())
    for word in ok:
        if re.search(word, response):  # curiosità su wolly
            while True:
                flag = True  # flag necessario per ripetere curiosità saltando l'if erorre
                print(random.choice(curiosita))
                textSpeech(random.choice(curiosita))
                # reface("wink")
                time.sleep(1)
                textSpeech("ne vuoi sentire un'altra?")
                response = talk()
                if response is False:
                    return
                elif re.search(r"\bno\b", response):
                    print(random.choice(noproblem))
                    textSpeech(random.choice(noproblem) + " resto comunque in ascolto")
                    return
                for wor in ok:
                    if re.search(wor, response):
                        print("va bene, ")
                        textSpeech("va bene, ")
                        flag = False

                if flag:
                    print(random.choice(err) + " resto in ascolto")
                    textSpeech(random.choice(err) + " resto in ascolto")
                    return


# no : stop
# si : un'altra?
def facs(response):
    if response is False:
        return
    elif re.search(r"\bno\b", response):
        print(random.choice(noproblem) + "resto in ascolto")
        textSpeech(random.choice(noproblem) + "resto in ascolto")
        return
    for word in ok:
        if re.search(word, response):
            while True:
                flag = True
                print(random.choice(realfacs))
                textSpeech(random.choice(realfacs))
                # reface("wink")
                time.sleep(1)
                textSpeech("ne vuoi sentire un altro?")
                response = talk()
                if response is False:
                    return
                elif re.search(r"\bno\b", response):
                    print(random.choice(noproblem))
                    textSpeech(random.choice(noproblem) + "resto comunque in ascolto")
                    return
                for wor in ok:
                    if re.search(wor, response):
                        print("va bene, ")
                        textSpeech("va bene, ")
                        flag = False

                if flag:
                    print(random.choice(err) + " resto in ascolto")
                    textSpeech(random.choice(err) + " resto in ascolto")
                    return


# no: chiede se vuole sentire una curiosità
# si: chiede cosa vuole vedere
# cantare
# ballare
# suoni
# barzellette V
# calcoli (?)
# indovinelli (?)
def richiesta(response):
    from chatbot import talk, textSpeech
    global talk, textSpeech
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
            response = talk()
            for word in barze:
                if re.search(word, response):
                    print(random.choice("va bene "))
                    textSpeech(random.choice("va bene "))
                    return barzelletta()


def barzelletta():
    while True:
        flag = True
        print(random.choice(battuta))
        textSpeech(random.choice(battuta))
        # reface("crazy")
        time.sleep(1)
        textSpeech("ne vuoi sentire un'altra?")
        response = talk()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem))
            textSpeech(random.choice(noproblem) + "resto comunque in ascolto")
            return
        for wor in ok:
            if re.search(wor, response):
                print("va bene, ")
                textSpeech("va bene, ")
                flag = False
        if flag:
            print(random.choice(err) + " resto in ascolto")
            textSpeech(random.choice(err) + " resto in ascolto")
            return