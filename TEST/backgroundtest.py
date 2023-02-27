import cv2
import time
import signal
import sys
from motorsNew import avanti, indietro, destra, sinistra
import multiprocessing
from chatbot import main as recognize_speech
from chatbot import textSpeech

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
            if deadzone_sx > x > correct_sx:
                sinistra(0.05, 0.6)

            elif deadzone_rx < x < correct_rx:
                destra(0.05, 0.6)

            elif x > correct_rx:
                destra(0.1, 0.6)

            elif x < correct_sx:
                sinistra(0.1, 0.6)

            # if the width of the rectangle is greater than 120 it means that the face is too close to the robot, vice versa if it's lower than 60
            if w > 120:
                indietro(0.09, 0.6)

            elif w < 60:
                avanti(0.09, 0.6)

            break

    cap.release()
    # cv2.destroyAllWindows()

def signal_handler(sig, frame):
    print('You ended the program')
    process1.terminate()
    process2.terminate()
    sys.exit(0)

if __name__ == '__main__':
    process1 = multiprocessing.Process(target=recognize_speech)
    process2 = multiprocessing.Process(target=track)
    process1.start()
    process2.start()
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')

    

