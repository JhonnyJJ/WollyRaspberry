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
    # simil execjson del vecchio wolly




if __name__ == '__main__':
    main()