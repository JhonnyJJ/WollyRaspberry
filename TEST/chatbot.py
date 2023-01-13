import time
import cv2
import pygame
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer


run = True

responses = {
    "ciao": "heila ciao",
    "come stai": "bene grazie!",
    "buona giornata": "grazie anche a te!"
}


def textSpeech(text, filename):
    mixer.init()
    #print('parlo')
    tts = gTTS(text=text, lang='it')
    tts.save(filename)
    mixer.music.load(filename)
    mixer.music.play()
    #while mixer.music.get_busy():  # wait for music to finish playing
    #    time.sleep(0.5)
    #pygame.quit() 


def chatbot(text):
    user_response = text.lower()
    err = "non ho sentito bene, puoi ripetere?"
    if user_response in responses:
        print("Wolly: " + responses[user_response])
        textSpeech(responses[user_response], 'tts.mp3')
    else:
        print(err)
        textSpeech(err, 'tts.mp3')


while run:
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 3000

        try:
            print("ascolto")
            audio = recognizer.listen(source)
            response = recognizer.recognize_google(audio, language="IT-IT")
            print(response)
            chatbot(response)
        except sr.UnknownValueError:
            print("Non ho capito")
            textSpeech("Non ho capito", 'tts.mp3')

    # press key s to stop the test
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
