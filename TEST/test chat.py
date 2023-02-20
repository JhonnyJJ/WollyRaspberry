import time
import random
import pygame
from pygame import mixer
import speech_recognition as sr
from gtts import gTTS

global numFaces
global i


saluto = ["ciao", "hey ciao!", "salve umano", "heila"]

# error phrases
err = ["forse non sono stato programmato per rispondere a questo!", "Mi dispiace, non so darti una risposta precisa",
       "faccio difficoltà a capire cosa intendi", "vorrei poterti dare una risposta ma non posso!",
       "ora non so risponderti, quando saprò la risposta sarai la prima persona a cui lo dirò!"]

# not understood phrases
notundst = ["non sono riuscito a sentirti!", "come scusa, non ho capito?", "scusa non ho capito potresti ripetere?",
            "non riesco a sentirti!"]

noresponse = ["non riesco a capirti! vado a ricalibrare il mio microfono!",
              "purtroppo non riesco a capire cosa hai detto, vado a prendermi un secondo di pausa ma"]

goodbye = ["nulla", "niente", "lascia stare"]

responses = {
    "ciao": "heila ciao, come posso esserti utile?",
    "come stai": "bene grazie!",
    "buona giornata": "grazie anche a te!"
}


def chatbot(text):
    user_response = text.lower()

    for word in goodbye:
        if word in user_response:
            print(random.choice(goodbye) + " resto in ascolto")
            return

    if user_response in responses:

        print(responses[user_response])
    else:

        print(random.choice(err))

def main():
    while True:
        print("vada vada")
        response = input()
        chatbot(response)

if __name__ == '__main__':
    main()