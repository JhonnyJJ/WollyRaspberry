import cv2
import time
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from motors import stop, avanti, indietro, destra, sinistra

numFaces = 0

# possible implementation of a wake word, so he can talk when somebody speaks to him

run = True

responses = {
    "ciao": "heila ciao, come ti ho già detto sono Wolly",
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
    # while mixer.music.get_busy():  # wait for music to finish playing
    #    time.sleep(0.5)
    # pygame.quit()

def chatbot(text):
    user_response = text.lower()
    err = "non ho sentito bene, puoi ripetere?"
    if user_response in responses:
        print("Wolly: " + responses[user_response])
        textSpeech(responses[user_response], 'tts.mp3')
    else:
        print(err)
        textSpeech(err, 'tts.mp3')


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

# infinite loop, it can be stopped with 's' input
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
    if 0 < len(faces):
        if len(faces) > numFaces:
            print("max num persone->"+ str(numFaces))
            textSpeech("Ciao io mi chiamo Wolly! Salutami o chiedimi qualcosa", "tts.mp3")
            numFaces = len(faces)

    print("vedo " + str(len(faces)) + " faccai/ facce")

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
        if deadzone_sx > x > correct_sx:
            sinistra(0.05, 0x61A8)
            stop()
        elif deadzone_rx < x < correct_rx:
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

        break

    # input s to stop
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

cap.release()
