import time
import random
import pygame
from pygame import mixer
import speech_recognition as sr
from gtts import gTTS

global numFaces
global i

# ARRAYS FOR WOLLY

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

# HUMAN INPUTS

goodbye = ["nulla", "niente", "lascia stare"]

responses = {
    "ciao": "heila ciao, come posso esserti utile?",
    "come stai": "bene grazie!",
    "buona giornata": "grazie anche a te!"
}

def playsound(filepath):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.05)
    #pygame.quit()   #windows debug

def textSpeech(text):
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    playsound("tts.mp3")


#hardcoded chatbot
def chatbot(text):
    user_response = text.lower()

    for word in goodbye:
        if word in user_response:
            print(random.choice(goodbye) + " resto in ascolto")
            textSpeech(random.choice(
                goodbye) + " resto in ascolto")  # al posto di goodbye aggiungere un array di possibili risposte
            return

    for key in responses.keys():
        if key in user_response:
            print(responses[key])
            textSpeech(responses[key])

    if user_response in responses:
        print("Wolly: " + responses[user_response])
        textSpeech(responses[user_response])
    else:
        print(random.choice(err))
        textSpeech(random.choice(err))


# each time you need to use microphone to get recognized speech as a string
def talk():
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
            return response

        except sr.UnknownValueError:
            global i
            i = i-1
            if i != 0:
                print("non ho capito, puoi ripetere?")
                textSpeech(random.choice(notundst))
            else:
                textSpeech(random.choice(noresponse) + " se hai ancora bisogno di me chiamami!")
                return None


def main():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,2)
            print("ascolto")
            audio = r.listen(source, phrase_time_limit=5, timeout=None)

        try:
            text = r.recognize_google(audio, language="IT-IT")

            if "hey wally" or "ciao wally" or "ok wally" in text.lower():
                textSpeech(random.choice(saluto) + ", dimmi pure")

                # value to keep track of how many tries the bot needs to ask
                global i
                i = 2
                response = talk()
                if response is not None:
                    chatbot(response)

        except sr.UnknownValueError:
            print("Non ho capito")
        except sr.RequestError as e:
            print("Errore durante il riconoscimento: {0}".format(e))


if __name__ == '__main__':
    main()