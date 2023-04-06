import cv2
import time
import random

from motorsNew import avanti, indietro, destra, sinistra

ciao = ["ciao sono wolly, ", "heila ciao, io sono wolly, ", "hey ciao, mi chiamo wolly, "]

ascolto = ["resto in ascolto, ", " ", "sono tutto orecchi, ", "sono a tua disposizione, ", "adesso sono in ascolto, "]

quando = ["quando hai bisogno di me chiamami e ti risponderò", "se avessi bisogno di me chiamami", "se volessi sapere quello che so fare chiamami",
          "se avessi bisogno di me chiamami"]


def main():
    from chatbot import textSpeech
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
        faces = face_cascade.detectMultiScale(gray, 1.1, 3, 0, (10, 10))

        # if the number of faces is greater than the number of faces already recognised Wolly will introduce himself again
        if 0 < len(faces) != numFaces:
            if len(faces) > numFaces:
                print("TTS", len(faces), numFaces)
                textSpeech(random.choice(ciao) + random.choice(ascolto) + random.choice(quando))
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
                sinistra(0.05, 0.8)

            elif x > deadzone_rx and x < correct_rx:
                destra(0.05, 0.8)

            elif x > correct_rx:
                destra(0.1, 0.8)

            elif x < correct_sx:
                sinistra(0.1, 0.8)

            # if the width of the rectangle is greater than 110 it means that the face is too close to the robot, vice versa if it's lower than 52
            if w > 120:
                indietro(0.09, 0.8)

            elif w < 60:
                avanti(0.09, 0.8)

            break

        # resize and flip to show camera feed with squares
        # creation of the camera feed window

        # frame = cv2.resize(frame, (320,200))
        # frame = cv2.flip(frame,1)
        # cv2.imshow('Video', frame)

    cap.release()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
