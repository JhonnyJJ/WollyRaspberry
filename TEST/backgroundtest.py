import cv2
import time
import random
from gtts import gTTS
from pygame import mixer
import speech_recognition as sr
from motorsNew import avanti, indietro, destra, sinistra
import multiprocessing
from Dialog import *


# wake words
wword = ["hey wally", "ciao wally", "ok wally"]

# ARRAYS FOR WOLLY

saluto = ["ciao", "hey ciao!", "salve umano", "heila"]

posso = ["vuoi che ti dica quello che so fare? ", "vuoi sentire cosa so fare? ", "sei curioso di sapere cosa so fare? "]

ecco = ["D'accordo, ecco una lista di quello che so fare!", "Va bene, ecco cosa so fare!", "so fare alcune cose simpatiche tra cui "]

fare = ["So raccontare le barzellette, so capire di che umore sei, so fare calcoli difficili, so cantare o ballare e so imitare dei suoni di cose e di animali"]

vedere = ["vorresti vedermi fare qualcosa?", "ti piacerebbe vedermi fare qualocosa?", "vuoi che faccia qualche azione?",
          "vuoi mettermi alla prova?"]

allora = ["allora vorresti sapere una piccola curiosità su di me?",
          "magari preferisci sentire qualche fatto curioso su di me?",
          "che ne dici di sentire qualche informazione in più su di me?"]

# error phrases
err = ["forse non sono stato programmato per rispondere a questo!", "Mi dispiace, non so darti una risposta precisa",
       "faccio difficoltà a capire cosa intendi", "vorrei poterti dare una risposta ma non posso!",
       "ora non so risponderti, quando saprò la risposta sarai la prima persona a cui lo dirò!"]

# not understood phrases
notundst = ["non sono riuscito a sentirti!", "come scusa, non ho capito?", "scusa non ho capito potresti ripetere?",
            "non riesco a sentirti!"]

noresponse = ["non riesco a capirti! vado a ricalibrare il mio microfono!",
              "purtroppo non riesco a capire cosa hai detto, vado a prendermi un secondo di pausa ma"]

# HUMAN INPUTS

goodbye = ["nulla", "niente", "lascia stare"]

responses = ["hey ciao, ", "ciao, ", "heila ciao, "]

ok = [r"\bok\b", r"\bsì\b", r"\bva bene\b",
      r"\bcerto\b"]  # r vale a dire la stringa raw, \b...\b invece è la parola singola separata da caratteri e numeri


def playsound(filepath):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.01)
    # pygame.quit()   #windows debug

def textSpeech(text):
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    playsound("tts.mp3")

# hardcoded chatbot AGGIUNGERE QUALCHE TIPO DI FACCIA CON DOMANDE O EMOZIONI
def chatbot(response):  # CREARE ALTRE DEF NEL CASO DI DIALOGO PIU' PROFONDO

    if response is False:
        return
    elif re.search(r"\bno\b", response):
        print(random.choice(noproblem) + random.choice(allora))
        textSpeech(random.choice(noproblem) + random.choice(allora))
        return curioso(talk())
    for word in ok:
        if re.search(word, response):  # parla di quello che sa fare wolly
            print(random.choice(fare))
            textSpeech(random.choice(ecco) + random.choice(fare) + random.choice(vedere))
            return richiesta(talk())

    # stop immediately
    for word in goodbye:
        if word in response:
            print(random.choice(noproblem) + " resto in ascolto")
            textSpeech(random.choice(noproblem) + " resto in ascolto")
            return


# each time you need to use microphone to get recognized speech as a string you call this method
def talk():
    # value to keep track of how many tries the bot needs to ask
    i = 2

    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 1)
            # add sound to help to know when to talk
            print("ascolto")
            playsound("hearing.mp3")
            audio = r.listen(source, phrase_time_limit=6, timeout=None)

        try:
            response = r.recognize_google(audio, language="IT-IT")
            print(response)
            return response.lower()

        except sr.UnknownValueError:
            i = i - 1
            if i != 0:
                print("non ho capito, puoi ripetere?")
                textSpeech(random.choice(notundst))
            else:
                print("non riesco a capirti! vado a ricalibrare il mio microfono!")
                textSpeech(random.choice(noresponse) + " se hai ancora bisogno di me chiamami!")
                return False


def recognize_speech():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 2)
            print("ascolto")
            audio = r.listen(source, timeout=None)

        try:
            text = r.recognize_google(audio, language="IT-IT")

            for word in wword:
                if re.search(word, text.lower()):
                    print(random.choice(responses) + random.choice(posso))
                    textSpeech(random.choice(responses) + random.choice(posso))

                    response = talk()
                    if response is not False:
                        chatbot(response)

        except sr.UnknownValueError:
            print("----------Non ho capito----------")
        except sr.RequestError as e:
            print("Errore con il collegamento API: {0}".format(e))


def track():
    numFaces = 0
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

    # infinite loop, it can be stopped with any desired input
    while True:

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
                textSpeech("ciao sono wolly")
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
                sinistra(0.05, 0.6)

            elif x > deadzone_rx and x < correct_rx:
                destra(0.05, 0.6)

            elif x > correct_rx:
                destra(0.1, 0.6)

            elif x < correct_sx:
                sinistra(0.1, 0.6)

            # if the width of the rectangle is greater than 110 it means that the face is too close to the robot, vice versa if it's lower than 52
            if w > 110:
                indietro(0.09, 0.6)

            elif w < 52:
                avanti(0.09, 0.6)

            break

        # resize and flip to show camera feed with squares
        # creation of the camera feed window

        # frame = cv2.resize(frame, (320,200))
        # frame = cv2.flip(frame,1)
        # cv2.imshow('Video', frame)

        # input s to stop
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    cap.release()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    process1 = multiprocessing.Process(target=recognize_speech)
    process2 = multiprocessing.Process(target=track)
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    

