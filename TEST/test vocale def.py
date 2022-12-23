import os
import cv2
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

run = True

def textSpeech(text):
    mixer.init()
    print('parla')
    tts = gTTS(text=text)
    tts.save('tts.mp3')
    mixer.music.load('tts.mp3')
    mixer.music.play()
    
while run:
    with sr.Microphone() as source:
        recognizer = sr. Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000

        try:
            print("ascolto")
            audio = recognizer.listen(source, timeout = 5.0)
            response = recognizer.recognize_google(audio)
            print(response)
            print("parlo")
            textSpeech(response)
        except sr.UnknownValueError:
            print("Non ho capito")

    if cv2.waitKey(1) & 0xFF ==ord('s'):
        break