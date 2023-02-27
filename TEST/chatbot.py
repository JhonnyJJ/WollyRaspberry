import time
import random
import pygame
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from Dialog import *

# wake words
wword = ["hey wally", "ciao wally", "ok wally"]

# ARRAYS FOR WOLLY

saluto = ["ciao", "hey ciao!", "salve umano", "heila"]

posso = ["vuoi che ti dica quello che so fare? ", "vuoi sentire cosa so fare? ", "sei curioso di sapere cosa so fare? "]

ecco = ["D'accordo, ecco una lista di quello che so fare!", "Va bene, ecco cosa so fare!", "so fare alcune cose simpatiche tra cui "]

fare = ["So raccontare le barzellette, so capire di che umore sei, so fare calcoli difficili, so cantare o ballare e so imitare dei suoni di cose e di animali"]

vedere = ["vorresti vedermi fare qualcosa?", "ti piacerebbe vedermi fare qualocosa?", "vuoi che faccia qualche azione?",
          "vuoi mettermi alla prova?"]

allora = ["allora vorresti sapere una piccola curiosità su di me?",
          "magari preferisci sentire qualche fatto curioso su di me?",
          "che ne dici di sentire qualche informazione in più su di me?"]

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

responses = ["hey ciao, ", "ciao, ", "heila ciao, "]

ok = [r"\bok\b", r"\bsì\b", r"\bva bene\b",
      r"\bcerto\b"]  # r vale a dire la stringa raw, \b...\b invece è la parola singola separata da caratteri e numeri


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
    playsound("tts.mp3")

# hardcoded chatbot AGGIUNGERE QUALCHE TIPO DI FACCIA CON DOMANDE O EMOZIONI
def chatbot(response):  # CREARE ALTRE DEF NEL CASO DI DIALOGO PIU' PROFONDO

    if response is False:
        return
    elif re.search(r"\bno\b", response):
        print(random.choice(noproblem) + random.choice(allora))
        textSpeech(random.choice(noproblem) + random.choice(allora))
        return curioso(talk())
    for word in ok:
        if re.search(word, response):  # parla di quello che sa fare wolly
            print(random.choice(fare))
            textSpeech(random.choice(ecco) + random.choice(fare) + random.choice(vedere))
            return richiesta(talk())

    # stop immediately
    for word in goodbye:
        if word in response:
            print(random.choice(noproblem) + " resto in ascolto")
            textSpeech(random.choice(noproblem) + " resto in ascolto")
            return


# each time you need to use microphone to get recognized speech as a string you call this method
def talk():
    # value to keep track of how many tries the bot needs to ask
    i = 2

    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 1)
            # add sound to help to know when to talk
            print("ascolto")
            playsound("hearing.mp3")
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
                return False


def main():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 2)
            print("ascolto")
            audio = r.listen(source, timeout=None)

        try:
            text = r.recognize_google(audio, language="IT-IT")

            for word in wword:
                if re.search(word, text.lower()):
                    print(random.choice(responses) + random.choice(posso))
                    textSpeech(random.choice(responses) + random.choice(posso))

                    response = talk()
                    if response is not False:
                        chatbot(response)

        except sr.UnknownValueError:
            print("Non ho capito")
        except sr.RequestError as e:
            print("Errore con il collegamento API: {0}".format(e))


if __name__ == '__main__':
    main()
