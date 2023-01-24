import time
import cv2
import random
import pygame
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from motors import stop, avanti, indietro, destra, sinistra

global numFaces
global i

# wake words
wword = ["hey wally", "ciao wally", "ok wally"]

saluto = ["ciao", "hey ciao!", "salve umano", "heila"]

# error phrases
err = ["forse non sono stato programmato per rispondere a questo!", "Mi dispiace, non so darti una risposta precisa",
       "faccio difficoltà a capire cosa intendi", "vorrei poterti darea una rispota ma non posso!", "ora non so risponderti, quando conoscerò la risposta sarai la prima persona a cui lo dirò!"]

# not understood phrases
notundst = ["non sono riuscito a sentirti!", "come scusa, non ho capito?", "scusa non ho capito potresti ripetere?",
          "non riesco a sentirti!"]

noresponse = ["non riesco a capirti! vado a ricalibrare il mio microfono!", "purtroppo non riesco a capire cosa hai detto, vado a prendermi un secondo di pausa ma"]

goodbye = ["nulla", "niente", "lascia stare"]

responses = {
    "ciao": "heila ciao",
    "come stai": "bene grazie!",
    "buona giornata": "grazie anche a te!"
}


def textSpeech(text, filename):
    mixer.init()
    # print('parlo')
    tts = gTTS(text=text, lang='it')
    tts.save(filename)
    mixer.music.load(filename)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(0.5)
    pygame.quit()


def chatbot(text):
    user_response = text.lower()

    if user_response in goodbye:
        textSpeech(random.choice(goodbye) + "resto in ascolto", 'tts.mp3')
        return

    if user_response in responses:
        print("Wolly: " + responses[user_response])
        textSpeech(responses[user_response], 'tts.mp3')
    else:
        print(random.choice(err))
        textSpeech(random.choice(err), 'tts.mp3')


def awake():
    stop_listening(wait_for_stop= False)
    with sr.Microphone() as source:
        recogni.adjust_for_ambient_noise(source,2)
        try:
            microphone = recogni.listen(source)
            response = recogni.recognize_google(microphone, language="IT-IT")
            print(response)
            chatbot(response)
            global stop_listening
            stop_listening = recogni.listen_in_background(microph, callback)
        except sr.UnknownValueError:
            global i
            i += 1
            if i <= 2:
                print("non ho capito, puoi ripetere?")
                textSpeech(random.choice(notundst), "tts.mp3")
                stop_listening = recogni.listen_in_background(microph, callback)
                awake()
            else:
                textSpeech(random.choice(noresponse) + " se hai ancora bisogno di me chiamami!", "tts.mp3")
                stop_listening = recogni.listen_in_background(microph, callback)
                return


def callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio, language="IT-IT")
        #wake word
        if text.lower() in wword:
            textSpeech(random.choice(saluto) + ", dimmi pure", "tts.mp3")
            # value to keep track of how many tries the bot needs to ask
            global i
            i = 0
            awake()
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def background():
    global recogni
    global microph
    recogni = sr.Recognizer()
    microph = sr.Microphone()

    with sr.Microphone() as source:
        recogni.adjust_for_ambient_noise(source,2)

    print("listen background")
    global stop_listening
    stop_listening = recogni.listen_in_background(microph, callback)


run = True
background()

while run:
    print("example of tracking running")
    for _ in range(50): time.sleep(0.1)

print("stop recording")
stop_listening(wait_for_stop=False)
