import time
import random
import re


# ARRAYS FOR WOLLY

saluto = ["ciao", "hey ciao!", "salve umano", "heila"]

addio = ["come desideri", "nessun problema", "va bene"]

posso = ["vuoi che ti dica quello che so fare?", "vuoi sentire cosa so fare?", "sei curioso di sapere cosa so fare?"]

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

ok = [r"\bok\b", r"\bsi\b", r"\bva bene\b", r"\bcerto\b"] # r vale a dire la stringa raw, \b...\b invece è la parola singola


def chatbot(text):
    user_response = text.lower()

    # stop immediately
    for word in goodbye:
        if word in user_response:
            print(random.choice(addio) + " resto in ascolto")
            return

    for key in responses.keys():
        if key in user_response:
            print(responses[key] + random.choice(posso))
            response = input()
            if response is None:
                return
            elif re.search(r"\bno\b", response):
                print("che vuoi brutto scemo")
                return
            for word in ok:
                if re.search(word, response):
                    print("BRAVOOOOOOOo")
                    return

    print(random.choice(err))


def main():
    while True:
        print("vada vada")
        response = input()
        chatbot(response)

if __name__ == '__main__':
    main()