import random
import re
from frasiDialog import *
import time


# AGGIUNGERE WHILE true DENTRO OGNI DEF CHE PRENDE IN CONSIDERAZIONE UNA PAROLA NON COLLEGATA A NESSUNA AZIONE

# si: curiosità di wolly
# no: fatti assurdi
def curioso():
    global talk, textSpeech
    from chatbot import talk, textSpeech
    i=0
    while i <= 1:
        response = talk()
        if response is False:  # controllo si o no per curiosità wolly
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(magarifatto))
            textSpeech(random.choice(noproblem) + random.choice(magarifatto))
            return facs(talk())
        for word in ok:
            if re.search(word, response):  # curiosità su wolly
                i = 0
                while i<=1:
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
                        textSpeech(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
                        return
                    for wor in ok:
                        if re.search(wor, response):
                            print("va bene, ")
                            textSpeech("va bene, ")
                            i=0
                            flag = False

                    if flag:
                        error("ripeti")
                        i+=1
                break
        error("ripeti")
        i += 1 
    error("ascolto")
    return


# no : stop
# si : un'altra?
def facs():
    i=0
    while i <= 1:
        response = talk()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + " resto in ascolto")
            textSpeech(random.choice(noproblem) + " resto in ascolto")
            return
        for word in ok:
            if re.search(word, response):
                i = 0
                while i<=1:
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
                        textSpeech(random.choice(noproblem) + " se hai ancora bisogno di me chiamami!")
                        # reface("wink")
                        return
                    for wor in ok:
                        if re.search(wor, response):
                            print("va bene, ")
                            textSpeech("va bene, ")
                            i=0
                            flag = False

                    if flag:
                        error("ripeti")
                        i+=1
                break
        error("ripeti")
        i += 1
                       
    error("ascolto")
    return

# no: chiede se vuole sentire una curiosità
# si: chiede cosa vuole vedere
# cantare
# ballare
# suoni 
# barzellette V
# indovinelli V
def richiesta(response):
    global talk, textSpeech
    from chatbot import talk, textSpeech
    i=0
    while i <= 1:
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            return curioso()
        for word in ok:
            if re.search(word, response):
                print(random.choice(noproblem) + "cosa vorresti vedere?")
                textSpeech(random.choice(noproblem) + "cosa vorresti vedere?")  # aggiungere eventi
                i = 0
                while i<=1:
                    response = talk()
                    print("prova")
                    if response is False:
                        return
                    for word in barze:
                        if re.search(word, response):
                            print("va bene ")
                            textSpeech("va bene ")
                            return barzelletta()
                    for word in indovina:
                        if re.search(word, response):
                            print("va bene ")
                            textSpeech("va bene ")
                            return indovinello()
                    error("ripeti")
                    i += 1
                break
        error("ripeti")
        i += 1
        response = talk()
    
    error("ascolto")
    return


def barzelletta():
    i=0
    while i <= 1:
        print(random.choice(battuta))
        textSpeech(random.choice(battuta))
        # reface("crazy")
        textSpeech("ne vuoi sentire un'altra?")
        flag = True
        response = talk()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem))
            textSpeech(random.choice(noproblem) + "resto comunque in ascolto")
            # reface("wink")
            return
        for wor in ok:
            if re.search(wor, response):
                print("va bene, ")
                textSpeech("va bene, ")
                i=0
                flag = False
        if flag:
            error("ripeti")
            i+=1
    error("ascolto")
    return
        
       
def indovinello():
    global ind, soluzione
    i=0
    while i <= 1:
        sbagliato = True
        flag = True
        ind = random.choice(indo)
        print(ind)
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
                sbagliato = False
                return ripInd()
        if sbagliato:
            print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
            textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
            i=0
            while i <= 1:
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
                error("ripeti")
                i+=1
    error("ascolto")
    return
            
        
def ritenta():
    global soluzione, ind
    sbagliato = True
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
    if sbagliato:
        print("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
        textSpeech("Ops! Non è la risposta corretta! Vuoi che ti dica la risposta?")
        i=0
        while i <= 2:
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
            error("ripeti")
            i+=1
        error("ascolto")
        return
    
    
def ripInd():
    print("ne vuoi sentire un'altra?")
    textSpeech("ne vuoi sentire un'altra?")
    i=0
    while i <= 2:
        response = talk()
        if response is False:
            return
        elif re.search(r"\bno\b", response):
            print(random.choice(noproblem) + " resto comunque in ascolto")
            textSpeech(random.choice(noproblem) + " resto comunque in ascolto")
            return
        for word in ok:
            if re.search(word, response):
                print("va bene, ")
                textSpeech("va bene, ")
                return indovinello()
        error("ripeti")
        i+=1
    error("ascolto")
    return
            
                
def error(cos):
    from chatbot import textSpeech
    if cos == "ripeti":
        print(random.choice(err) + " potresti ripetere?")
        textSpeech(random.choice(err) + " potresti ripetere?")
    elif cos== "ascolto":
        print(random.choice(err) + " resto in ascolto")
        textSpeech(random.choice(err) + " resto in ascolto")