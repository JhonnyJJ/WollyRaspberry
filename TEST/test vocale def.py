import cv2
import time
import pygame
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

def playsound(filepath):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)
    #pygame.quit()   #windows debug

def textSpeech(text):
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    playsound("tts.mp3")
    
while True:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000
        print("ascolto")
        audio = recognizer.listen(source, timeout=5.0)

        try:
            response = recognizer.recognize_google(audio, language="IT-IT")
            print(response)
            textSpeech(response)
        except sr.UnknownValueError:
            print("Non ho capito")

    if cv2.waitKey(1) & 0xFF ==ord('s'):
        break