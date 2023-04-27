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
    stop()
    pca.channels[0].duty_cycle = power
    pca.channels[1].duty_cycle = power
    pca.channels[5].duty_cycle = power
    pca.channels[4].duty_cycle = power
    time.sleep(duration)


def destra(duration, power):
    stop()
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
    ----------------------------------
"""

host_name = '192.168.43.103'
host_port = '8000'


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
    Inizio configurazione AppWrite
"""

# ENDPOINT = 'https://9225438084d8.ngrok.io/v1'
# PROJECT_ID = '5fa7e32a5133e'
# API_KEY = '51935101e4598b8a6c6722c919757eab00614c5cf07320d2d4e894a9fc178dfc6e44f9811ac2426d16027197435c663f25665f5f1661aa00d345fb8bef2a177c2ddbee5727e26cb348c99f5a54507f81897a13602b2af124255f7375867cf183c0afbedaa361b4eed1581d94366a327f81588fe233de9282e098ff7207530301'

ENDPOINT = 'http://app.wolly.di.unito.it/v1'
PROJECT_ID = '60cc80c053637'
API_KEY = '15735ace9c277263e68936020652843ed788409e79f9f2ca745fe4179d82e7f25de27e83dee7161e9b747540161f0902ba077f0e10844ac2bbdc639386e4a98de2dc5c3db62356d7cb3003e3bb4cd881e065b3f5bdcae8ad45b546e7a02dbac0f2d88a6c6df411611c19673e3e498cdaefcfcd0d0d055d92bf531dd3b6e350d8'

client = Client()

client.set_endpoint(ENDPOINT)
client.set_project(PROJECT_ID)
client.set_key(API_KEY)
# client.add_header("Origin", ENDPOINT)

collectionId = '60d2f79f5ffc1'
userId = '60d2f78729a5c'

"""
    Fine configurazione AppWrite
"""

"""
    Inizio configurazione Tkinter per volto Wolly
"""

# Creazione di una finestra di Tkinter
root = Tk()
root.attributes('-fullscreen', True)

# Create a size for tkinter window
root.geometry("800x480")  # here use alphabet 'x' not '*' this one

# Creazione della Label
label = Label(root, font="bold")
label.pack()

espressione = "default"
dateOldMossa = ""
x = 1
img = ImageTk.PhotoImage(Image.open("img/faces/default/1.png"))


def expression():
    global x, img, espressione
    DIR = 'img/faces/' + espressione + "/"
    faces = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name)) and ".png" in name]
    count = len(faces)
    if x <= count:
        img = ImageTk.PhotoImage(Image.open(DIR + str(x) + ".png"))
        label.configure(image=img)
        x += 1
        root.after(20, expression)
    else:
        x = 1
        espressione = "default"


"""
    Fine espressioni
"""

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


"""
    --------------------------------------------------------------------
"""

"""
    Esecuzione comandi dati dal sito
"""


def execJson(response):
    global dateOldMossa
    document = response["documents"][0]
    print('eta: ' + document["eta"])
    if document["eta"] != dateOldMossa:
        dateOldMossa = document['eta']
        print('Nuovo comando')
        exec(document["mosse"])


"""
    Retrive documenti sul database
"""


def list_doc():
    database = Database(client)
    print_green("Running List Document API")
    response = database.list_documents(collectionId)
    execJson(response)


def mainLoop():
    database = Database(client)
    response = database.list_documents(collectionId)
    document = response["documents"][0]
    autonomo = document["autonomo"]

    if autonomo:
        faceDetect()
        led("on")
        root.after(0, mainLoop)
    elif not autonomo:
        led("off")
        expression()
        list_doc()
        print('old mossa: ' + dateOldMossa)
        root.after(3000, mainLoop)


root.after(0, mainLoop)
root.bind("<Escape>", lambda event: root.destroy())
tkinter.mainloop()

