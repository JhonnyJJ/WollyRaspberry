import time
import random
import re
from backgroundtest import textSpeech, talk, ok, err

curiosita = ["sono un robottino creato per diventare un insegnante, prima o poi con tanto duro lavoro lo diventerò",
             "sono stato creato utilizzando un computer che si chiama Raspberry, è esattamente come un computer normale, solo un po più piccolo!"]

noproblem = ["ok nessun problema, ", "okay non importa, ", " va bene, ", "okay capisco, ", "Va bene, nessun problema! ",
             "D'accordo, ", "Ho capito, ", "perfetto, "]

fattoassurdo = ["magari posso incuriosirti con un fatto assurdo?",
                "se vuoi posso dirti qualche fatto curioso", "vuoi che ti racconti qualche curiosità?",
                "vuoi per caso sapere qualche curiosità?"]

realfacs = ["Masticare una chewing-gum mentre si pelano le cipolle può frenare il pianto",
            "I fenicotteri sono rosa perché mangiano gamberetti",
            "Il miele è l'unico cibo che non scade mai: lo stesso miele che è stato sepolto con i faraoni in Egitto è ancora commestibile",
            "il ketchup è nato come una medicina",
            "l'altezza della torre eiffel può variare di 15 centimetri in base alla temperatura"]


# si: curiosità di wolly
# no: fatti assurdi
def curioso(response):
    if response is False:  # controllo si o no per curiosità wolly
        return
    elif re.search(r"\bno\b", response):
        print(random.choice(noproblem) + random.choice(fattoassurdo))  # Continuare si o no
        textSpeech(random.choice(noproblem) + random.choice(fattoassurdo))
        return facs(talk())
    for word in ok:
        if re.search(word, response):  # curiosità su wolly
            while True:
                flag = True
                print(random.choice(curiosita))
                textSpeech(random.choice(curiosita) + ", ne vuoi sentire un'altra?")
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
                textSpeech(random.choice(realfacs) + ", ne vuoi sentire un altro?")
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


# no: lascia chiede se vuole sentire una curiosità
# si: chiede cosa vuole vedere
def richiesta(response):
    if response is False:
        return
    elif re.search(r"\bno\b", response):
        print(random.choice(noproblem) + " resto in ascolto")
        textSpeech(random.choice(noproblem) + " resto in ascolto")
        return curioso(talk())
    for word in ok:
        if re.search(word, response):
            print(random.choice(noproblem) + "cosa vorresti vedere?")
            textSpeech(random.choice(noproblem) + "cosa vorresti vedere?")  # aggiungere eventi
            return