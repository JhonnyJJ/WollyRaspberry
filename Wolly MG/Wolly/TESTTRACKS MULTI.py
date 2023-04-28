import cv2
import time
import random

import signal
import sys
import multiprocessing

#import AppWrite
from appwrite.client import Client
from appwrite.services.database import Database
from appwrite.services.storage import Storage

from motorsNew import *

import urllib3


def signal_handler(sig, frame):
    global process2, process3, process4
    print('You ended the program')
    process2.terminate()
    time.sleep(3)
    sys.exit(0)


ENDPOINT = 'http://app.wolly.di.unito.it/v1'
PROJECT_ID = '60cc80c053637'
API_KEY = '15735ace9c277263e68936020652843ed788409e79f9f2ca745fe4179d82e7f25de27e83dee7161e9b747540161f0902ba077f0e10844ac2bbdc639386e4a98de2dc5c3db62356d7cb3003e3bb4cd881e065b3f5bdcae8ad45b546e7a02dbac0f2d88a6c6df411611c19673e3e498cdaefcfcd0d0d055d92bf531dd3b6e350d8'

client = Client()

client.set_endpoint(ENDPOINT)
client.set_project(PROJECT_ID)
client.set_key(API_KEY)
# client.add_header("Origin", ENDPOINT)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

collectionId = '60d2f79f5ffc1'
userId = '60d2f78729a5c'

dateOldMossa = ""

def track():
    global cap
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
        
        print(len(faces))

        # if the number of faces is greater than 0 wolly will introduce himself
        if 0 < len(faces):
            print("aaaaaaaaaaaaaaaaa")
            ciao()
            
def ciao():
    while True:
        print("suca")
            
def print_green(prt):
    print("\033[32;1m" + str(prt) + "\033[0m")
    
def execJson(response):
    global dateOldMossa
    document = response["documents"][0]
    print('eta: ' + document["eta"])
    if document["eta"] != dateOldMossa:
        dateOldMossa = document['eta']
        print('Nuovo comando')
        exec(document["mosse"])

def list_doc():
    database = Database(client)
    print_green("Running List Document API")
    response = database.list_documents(collectionId)
    execJson(response)

def master():
    global process4
    while True:
        chat = False
        database = Database(client)
        response = database.list_documents(collectionId)
        document = response["documents"][0]
        autonomo = document["autonomo"]
        print("controllo 1")
        
        if autonomo:
            startProc()
            print("autonomo")
            chat = True
        elif not autonomo:
            list_doc()
            print('old mossa: ' + dateOldMossa)

        while True:
            database = Database(client)
            response = database.list_documents(collectionId)
            document = response["documents"][0]
            autonomia = document["autonomo"]
            print("controllo 2")
            
            if not autonomo:
                list_doc()
                print('old mossa: ' + dateOldMossa)

            if autonomo != autonomia:
                if chat:
                    print("close proc") # NON CHIUDE IL PROCESSO
                    stopProc()
                break
            
            
def startProc():
    global process4
    process4 = multiprocessing.Process(target=track)
    process4.start()

def stopProc():
    global process4
    process4.terminate()
    time.sleep(4)
    
if __name__ == '__main__':
    print('Press Ctrl+C to stop the program')
    process2 = multiprocessing.Process(target=master) # faccia che si chiude e si riapre ogni volta che si cambia espressione
    process2.start()
    
    
    