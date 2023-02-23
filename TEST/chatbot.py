import time
import random
import re
import pygame
from pygame import mixer
import speech_recognition as sr
from gtts import gTTS

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
      r"\bcerto\b"]  # r vale a dire la stringa raw, \b...\b invece è la parola singola separata da caratteri e numeri


def playsound(filepath):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.05)
    # pygame.quit()   #windows debug


def textSpeech(text):
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    playsound("tts.mp3")


# hardcoded chatbot AGGIUNGERE QUALCHE TIPO DI FACCIA CON DOMANDE O EMOZIONI
def chatbot(response):  # CREARE ALTRE DEF NEL CASO DI DIALOGO PIU' PROFONDO

    # stop immediately
    for word in goodbye:
        if word in response:
            print(random.choice(addio) + " resto in ascolto")
            textSpeech(random.choice(addio) + " resto in ascolto")
            return

    for key in responses.keys():
        if key in response:
            print(responses[key] + random.choice(posso))
            textSpeech(responses[key] + random.choice(posso))
            response = talk()
            if response is False:
                return
            elif re.search(r"\bno\b", response):
                print("Va bene, nessun problema! allora vorresti sapere una piccola curiosità su di me?")
                textSpeech("Va bene, nessun problema! allora vorresti sapere una piccola curiosità su di me?")
                response = talk()
                if response is False:  # controllo si o no per curiosità wolly
                    return
                elif re.search(r"\bno\b", response):  # no curiosità wolly
                    print("ok nessun problema, magari posso incuriosirti con un fatto assurdo?")  # Continuare si o no
                    textSpeech("ok nessun problema, magari posso incuriosirti con un fatto assurdo?")
                    return
                for word in ok:
                    if re.search(word, response):  # curiosità su wolly
                        print(random.choice(curiosita))
                        textSpeech(random.choice(curiosita))
                        print("CONTINUARE IL DISCORSO")
                        return
            for word in ok:
                if re.search(word, response):  # parla di quello che sa fare wolly
                    print("So urlare bestemmie")
                    textSpeech("iabadabadu")
                    return


# each time you need to use microphone to get recognized speech as a string
def talk():
    # value to keep track of how many tries the bot needs to ask
    i = 2

    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 1)
            # add sound to help to know when to talk
            playsound("hearing.mp3")
            print("ascolto")
            audio = r.listen(source)

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
            audio = r.listen(source, phrase_time_limit=3, timeout=None)

        try:
            text = r.recognize_google(audio, language="IT-IT")

            if "hey wally" or "ciao wally" or "ok wally" in text.lower():
                textSpeech(random.choice(saluto) + ", dimmi pure")

                response = talk()
                if response is not False:
                    chatbot(response)

        except sr.UnknownValueError:
            print("Non ho capito")
        except sr.RequestError as e:
            print("Errore con il collegamento API: {0}".format(e))


if __name__ == '__main__':
    main()
