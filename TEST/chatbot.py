import time
import cv2
import random
import pygame
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

global numFaces
global i

# wake words
wword = ["hey wally", "ciao wally", "ok wally"]

saluto = ["ciao", "hey ciao!", "salve umano", "heila"]

# error phrases
err = ["forse non sono stato programmato per rispondere a questo!", "Mi dispiace, non so darti una risposta precisa",
       "faccio difficoltà a capire cosa intendi", "vorrei poterti dare una risposta ma non posso!",
       "ora non so risponderti, quando saprò la risposta sarai la prima persona a cui lo dirò!"]

# not understood phrases
notundst = ["non sono riuscito a sentirti!", "come scusa, non ho capito?", "scusa non ho capito potresti ripetere?",
          "non riesco a sentirti!"]

noresponse = ["non riesco a capirti! vado a ricalibrare il mio microfono!", "purtroppo non riesco a capire cosa hai detto, vado a prendermi un secondo di pausa ma"]

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

def textSpeech(text):
    # print('parlo')
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    playsound("tts.mp3")

def chatbot(text):
    user_response = text.lower()

    if user_response in goodbye:
        textSpeech(random.choice(goodbye) + "resto in ascolto")
        return

    if user_response in responses:
        print("Wolly: " + responses[user_response])
        textSpeech(responses[user_response])
    else:
        print(random.choice(err))
        textSpeech(random.choice(err))


def awake():
    global stop_listening
    stop_listening(wait_for_stop= False)
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, 2)
        try:
            # add sound to help to know when to talk
            playsound("hearing.mp3")
            microphone = r.listen(source)
            response = r.recognize_google(microphone, language="IT-IT")
            print(response)
            chatbot(response)
            background()
        except sr.UnknownValueError:
            global i
            i += 1
            if i <= 2:
                print("non ho capito, puoi ripetere?")
                textSpeech(random.choice(notundst))
                awake()
            else:
                textSpeech(random.choice(noresponse) + " se hai ancora bisogno di me chiamami!")
                background()
                return


def callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio, language="IT-IT")
        #wake word
        if text.lower() in wword:
            textSpeech(random.choice(saluto) + ", dimmi pure")
            # value to keep track of how many tries the bot needs to ask
            global i
            i = 0
            awake()
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def background():
    global r
    global m
    r = sr.Recognizer()
    m = sr.Microphone()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,2)

    print("listen background")
    global stop_listening
    stop_listening = r.listen_in_background(m, callback)


run = True
background()

while run:
    for _ in range(50): time.sleep(0.1)

print("stop recording")
stop_listening(wait_for_stop=False)