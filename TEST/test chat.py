import time
import random
import re

# ARRAYS FOR WOLLY

saluto = ["ciao", "hey ciao!", "salve umano", "heila"]

addio = ["come desideri", "nessun problema", "va bene"]

posso = ["vuoi che ti dica quello che so fare?", "vuoi sentire cosa so fare?", "sei curioso di sapere cosa so fare?"]

curiosita = ["sono un robottino creato per diventare un insegnante, prima o poi con tanto duro lavoro lo diventerò",
             "sono stato creato utilizzando un computer che si chiama Raspberry, è esattamente come un computer normale, solo un po più piccolo!"]

# error phrases
err = ["forse non sono stato programmato per rispondere a questo!", "Mi dispiace, non so darti una risposta precisa",
       "faccio difficoltà a capire cosa intendi", "vorrei poterti dare una risposta ma non posso!",
       "ora non so risponderti, quando saprò la risposta sarai la prima persona a cui lo dirò!"]

# not understood phrases
notundst = ["non sono riuscito a sentirti!", "come scusa, non ho capito?", "scusa non ho capito potresti ripetere?",
            "non riesco a sentirti!"]

noresponse = ["non riesco a capirti! vado a ricalibrare il mio microfono!",
              "purtroppo non riesco a capire cosa hai detto, vado a prendermi un secondo di pausa ma"]

# HUMAN INPUTS

goodbye = ["nulla", "niente", "lascia stare"]

responses = {
    "ciao": "hey ciao, ",
    "hey": "ciao, ",
    "heila": "heila ciao, "
}

ok = [r"\bok\b", r"\bsi\b", r"\bva bene\b",
      r"\bcerto\b"]  # r vale a dire la stringa raw, \b...\b invece è la parola singola


def chatbot(response): # CREARE ALTRE DEF NEL CASO DI DIALOGO PIU' PROFONDO

    # stop immediately
    for word in goodbye:
        if word in response:
            print(random.choice(addio) + " resto in ascolto")
            return

    for key in responses.keys():
        if key in response:
            print(responses[key] + random.choice(posso))
            response = input()
            if response is False:
                return
            elif re.search(r"\bno\b", response):
                print("Va bene, nessun problema! allora vorresti sapere una piccola curiosità su di me?")
                response = input()
                if response is False: # controllo si o no per curiosità wolly
                    return
                elif re.search(r"\bno\b", response): # no curiosità wolly
                    print("ok nessun problema, magari posso incuriosirti con un fatto assurdo?") # Continuare si o no
                    return
                for word in ok:
                    if re.search(word, response): # curiosità su wolly
                        print(random.choice(curiosita))
                        print("CONTINUARE IL DISCORSO")
                        return
            for word in ok:
                if re.search(word, response): # parla di quello che sa fare wolly
                    print("So urlare bestemmie")
                    return


def main():
    while True:
        print("vada vada")
        response = input()
        chatbot(response)


if __name__ == '__main__':
    main()
