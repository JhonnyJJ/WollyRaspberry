import urllib3

# Import AppWrite
from appwrite.client import Client
from appwrite.services.database import Database
from appwrite.services.storage import Storage

# Import Motors
import RPi.GPIO as GPIO
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685  # Import the PCA9685 module.

# Import Faces
import os
from tkinter import *
import tkinter
from PIL import Image, ImageTk

# Import Face Detect
import io
import picamera
import cv2
import numpy
from gtts import gTTS
from pygame import mixer


# Helper method to print green colored output.
def print_green(prt):
    print("\033[32;1m" + str(prt) + "\033[0m")


"""
    Metodi per il movimento di Wolly
"""


def stop():
    pca.channels[0].duty_cycle = 0xFFFF
    pca.channels[1].duty_cycle = 0x0000
    pca.channels[2].duty_cycle = 0x0000
    pca.channels[5].duty_cycle = 0xFFFF
    pca.channels[4].duty_cycle = 0x0000
    pca.channels[3].duty_cycle = 0x0000


def avanti(duration, power):
    stop()
    pca.channels[0].duty_cycle = power
    pca.channels[1].duty_cycle = power
    pca.channels[5].duty_cycle = power
    pca.channels[3].duty_cycle = power
    time.sleep(duration)


def indietro(duration, power):
    stop()
    pca.channels[0].duty_cycle = power
    pca.channels[2].duty_cycle = power
    pca.channels[5].duty_cycle = power
    pca.channels[4].duty_cycle = power
    time.sleep(duration)


def sinistra(duration, power):
    pca.channels[0].duty_cycle = power
    pca.channels[1].duty_cycle = power
    pca.channels[5].duty_cycle = power
    pca.channels[4].duty_cycle = power
    time.sleep(duration)


def destra(duration, power):
    pca.channels[0].duty_cycle = power
    pca.channels[2].duty_cycle = power
    pca.channels[5].duty_cycle = power
    pca.channels[3].duty_cycle = power
    time.sleep(duration)


def led(status):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(21, GPIO.OUT)

    if status == 'on':
        GPIO.output(21, GPIO.HIGH)
    elif status == 'off':
        GPIO.output(21, GPIO.LOW)


"""
    inizio istruzioni per pilotare i motori con i2c_bus
"""

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 60

"""
    fine istruzioni per pilotare i motori con i2c_bus
"""

stop()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
    Face Detect & TextToSpeech
"""
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
    face_cascade = cv2.CascadeClassifier('lib/haarcascade_frontalface_default.xml')

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if 0 < len(faces) != numFaces:
        if len(faces) > numFaces:
            print("TTS", len(faces), numFaces)
            textSpeech()
            numFaces = len(faces)
        print(len(faces), numFaces)
    elif len(faces) == 0:
        numFaces = 0

    print("------------------")
    # print("Found " + str(len(faces)) + " face(s)")

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
    tts.save('mp3/tts.mp3')
    mixer.music.load('mp3/tts.mp3')
    mixer.music.play()
