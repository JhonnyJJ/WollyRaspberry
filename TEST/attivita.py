import time
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import random

from motorsNew import avanti, indietro, destra, sinistra

responses = {
    "ciao": "heila ciao, come posso esserti utile?",
    "come stai": "bene grazie!",
    "buona giornata": "grazie anche a te!"
}

noresponse = ["non riesco a capirti! vado a ricalibrare il mio microfono!",
              "purtroppo non riesco a capire cosa hai detto, vado a prendermi un secondo di pausa ma"]


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

def main():
    textSpeech("daje roma daje, questa è la spiegazione dell'attività che faremo oggi")

    # if you want to use microphone or else

    # while True:
    #     r = sr.Recognizer()
    #
    #     with sr.Microphone() as source:
    #         r.adjust_for_ambient_noise(source, 1)
    #         # add sound to help to know when to talk
    #         playsound("hearing.mp3")
    #         print("ascolto")
    #         audio = r.listen(source)
    #
    #     try:
    #         response = r.recognize_google(audio, language="IT-IT")
    #         print(response)
    #     except sr.UnknownValueError:
    #         textSpeech(random.choice(noresponse) + " se hai ancora bisogno di me chiamami!")




if __name__ == '__main__':
    main()