import signal
import sys
import multiprocessing
import time
import random
from pygame import mixer
from gtts import gTTS
import cv2
from frasiDialog import *


def playsound(filepath):
    print("parlo")
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.01)
        
def textSpeech(text):
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    playsound("tts.mp3")

def track():
    global process3
    while True:
        print("TTS" )
        textSpeech(random.choice(ciao) + random.choice(ascolto) + random.choice(quando))
        print("inizio")
        playsound("/home/wolly/Desktop/WollyRaspberry/mp3/alien_sound.mp3")
        time.sleep(10)
        
        

# signal handler per ctrl+c alla fine del programma
def signal_handler(sig, frame):
    global process2, process3
    print('You ended the program')
    process4.terminate()
    time.sleep(3)
    sys.exit(0)


if __name__ == '__main__':
    print('Press Ctrl+C to stop the program')
    process4 = multiprocessing.Process(target=track)
    process4.start()
    print("prova")
    time.sleep(3)
    print("prova")
    print("prova")
    process4.terminate()
    signal.signal(signal.SIGINT, signal_handler)