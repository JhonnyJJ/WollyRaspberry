import time
import cv2
import random
import pygame
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

from motorsNew import avanti, indietro, destra, sinistra

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

noresponse = ["non riesco a capirti! vado a ricalibrare il mio microfono!",
              "purtroppo non riesco a capire cosa hai detto, vado a prendermi un secondo di pausa ma"]

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
        time.sleep(0.1)
    #pygame.quit()   #windows debug

def textSpeech(text):
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
    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 2)
            # add sound to help to know when to talk
            playsound("hearing.mp3")
            print("ascolto")
            audio = r.listen(source)

        try:
            response = r.recognize_google(audio, language="IT-IT")
            print(response)
            chatbot(response)
            break
        except sr.UnknownValueError:
            global i
            i = i-1
            if i != 0:
                print("non ho capito, puoi ripetere?")
                textSpeech(random.choice(notundst))
            else:
                textSpeech(random.choice(noresponse) + " se hai ancora bisogno di me chiamami!")
                break


def callback(recognizer, audio):
    try:
        print("listen")
        text = recognizer.recognize_google(audio, language="IT-IT")
        # wake word
        if text.lower() in wword:
            textSpeech(random.choice(saluto) + ", dimmi pure")
            # value to keep track of how many tries the bot needs to ask
            global i
            i = 2
            awake()
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


# Inizializza il riconoscimento del microfono
r = sr.Recognizer()
mic = sr.Microphone()

# Carica il classificatore per il rilevamento del viso
face_cascade = cv2.CascadeClassifier('/home/wolly/Desktop/WollyRaspberry/lib/haarcascade_frontalface_default.xml')

# Avvia la webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200);
time.sleep(1)

while True:
    # Leggi un frame dalla webcam
    ret, frame = cap.read()

    if ret == False:
        print("error getting image")
        continue

    # Converti il frame in scala di grigio
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Rileva i volti nel frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Disegna un rettangolo intorno ai volti rilevati
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


    # Ascolta per il discorso
    with mic as source:
        print("ascolto")
        audio = r.listen(source,timeout=5)

    try:
        # Riconosci il discorso
        speech = r.recognize_google(audio, language="it-IT")
        print("Hai detto: " + speech)
    except sr.UnknownValueError:
        print("Non ho capito")
    except sr.RequestError as e:
        print("Errore durante il riconoscimento: {0}".format(e))

    # Se viene premuto il tasto "q", esci dal ciclo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia la webcam e distruggi le finestre
cap.release()
cv2.destroyAllWindows()