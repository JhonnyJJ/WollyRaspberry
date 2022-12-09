import io
import picamera
import numpy
from gtts import gTTS
import subprocess
from pygame import mixer
from PIL import Image
from cv2 import cv2

numFaces = 0


def faceDetect():
    global numFaces
    # Create a memory stream so photos doesn't need to be saved in a file
    stream = io.BytesIO()

    # Get the picture (low resolution, so it should be quite fast)
    # Here you can also specify other parameters (e.g.:rotate the image)
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.capture(stream, format='jpeg')

    # Convert the picture into a numpy array
    buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)

    # Now creates an OpenCV image
    image = cv2.imdecode(buff, 1)

    # https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
    # Load a cascade file for detecting faces
    face_cascade = cv2.CascadeClassifier('/home/wolly/Desktop/WollyRaspberry/lib/haarcascade_frontalface_default.xml')

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if 0 < len(faces) != numFaces:
        textSpeech()
        numFaces = len(faces)

    print("Found " + str(len(faces)) + " face(s)")

    # Draw a rectangle around every found face
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (111, 210, 90), 2)

    # Save the result image
    # cv2.imwrite('result.jpg',image)


def textSpeech():
    mixer.init()
    print('parla')
    text = 'Ciao sono Wolly!'
    tts = gTTS(text=text, lang='it')
    tts.save('tts.mp3')
    mixer.music.load('tts.mp3')
    mixer.music.play()


if __name__ == "__main__":
    while True:
        faceDetect()
