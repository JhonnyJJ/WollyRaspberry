import time
import cv2
import random
import pygame
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from motors import stop, avanti, indietro, destra, sinistra
from threading import Thread

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
    song = AudioSegment.from_mp3(filepath)
    play(song)

def textSpeech(text):
    # print('parlo')
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    time.sleep(2)
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

def background():
    global r
    global m
    r = sr.Recognizer()
    m = sr.Microphone()
    print("ascolto in background")

    with m as source:
        print("parla")
        r.adjust_for_ambient_noise(source,0.5)
        
        try:
            microphone = r.listen(source)
            text = r.recognize_google(microphone, language="IT-IT")
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


run = True
numFaces=0

# cascade classifier for face tracking
face_cascade = cv2.CascadeClassifier('/home/wolly/Desktop/WollyRaspberry/lib/haarcascade_frontalface_default.xml')

# inizializing camera capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200);
time.sleep(1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

listen = Thread(target=background).start()
while run:
    listen.run()
    # capture frame by frame
    ret, frame = cap.read()

    if ret == False:
        print("error getting image")
        continue

    # gray scaling for easier detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # face detection for each frame
    faces = face_cascade.detectMultiScale(frame, 1.1, 3, 0, (10, 10))

    # if the number of faces is greater than the number of faces already recognised Wolly will introduce himself again
    if 0 < len(faces) != numFaces:
        if len(faces) > numFaces:
            print("TTS", len(faces), numFaces)
            textSpeech("Ciao, sono Wolly!")
            numFaces = len(faces)
        print(len(faces), numFaces)

    print("Found " + str(len(faces)) + " face(s)")

    # create a green rectangle around the found faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # start tracking
        # values of the frame to find the center on the x axis of the frame
        FRAME_W = 320

        # centre of the face (only x axis because it hasn't any motor on the y axis)
        x = x + (w / 2)

        # coordinates on the right side, of the robot while facing you, is greater then left side (any future right or left will be referred to the robot)
        # we take the half of the frame wight and add 80 frames of "dead zone" (40 on each side) so the robot isn't constantly moving
        deadzone_rx = (FRAME_W / 2) + 40
        deadzone_sx = (FRAME_W / 2) - 40

        # we create a border to make bigger adjustments so the robot can keep up with the face
        correct_rx = (FRAME_W / 2) + 70
        correct_sx = (FRAME_W / 2) - 70

        # if the face coordinate is < of the left border the robot needs to be moving left
        # if the face coordinate is > of the right border the robot needs to be moving right
        if x < deadzone_sx and x > correct_sx:
            sinistra(0.05, 0x61A8)
            stop()
        elif x > deadzone_rx and x < correct_rx:
            destra(0.05, 0x61A8)
            stop()
        elif x > correct_rx:
            destra(0.1, 0x61A8)
            stop()
        elif x < correct_sx:
            sinistra(0.1, 0x61A8)
            stop()

        # if the width of the rectangle is greater than 110 it means that the face is too close to the robot, vice versa if it's lower than 52
        if w > 110:
            indietro(0.09, 0x61A8)
            stop()
        elif w < 52:
            avanti(0.09, 0x61A8)
            stop()

        break

cap.release()
print("stop recording")
stop_listening(wait_for_stop=False)