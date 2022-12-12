import os
import tkinter
# from threading import Timer
from tkinter import *
import urllib3
from PIL import Image, ImageTk
from appwrite.client import Client
from appwrite.services.database import Database


def print_green(prt):
    print("\033[32;1m" + str(prt) + "\033[0m")


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ENDPOINT = 'https://32e95fd58ade.ngrok.io/v1'
PROJECT_ID = '5fa7e32a5133e'
API_KEY = '51935101e4598b8a6c6722c919757eab00614c5cf07320d2d4e894a9fc178dfc6e44f9811ac2426d16027197435c663f25665f5f1661aa00d345fb8bef2a177c2ddbee5727e26cb348c99f5a54507f81897a13602b2af124255f7375867cf183c0afbedaa361b4eed1581d94366a327f81588fe233de9282e098ff7207530301 '

client = Client()

client.set_endpoint(ENDPOINT)
client.set_project(PROJECT_ID)
client.set_key(API_KEY)

collectionId = '5fa7f95e7c474'
userId = '5fa9ae0695af3'

# create a tkinter window
t = Tk()
t.attributes('-fullscreen', False)

# Create a size for tkinter window
t.geometry("800x480")  # here use alphabet 'x' not '*' this one

# Create a label
label = Label(t, font="bold")
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
        t.after(20, expression)
    else:
        x = 1
        espressione = "default"


def execJson(response):
    global dateOldMossa, espressione
    document = response["documents"][0]
    print('eta: ' + document["eta"])
    if document["eta"] != dateOldMossa:
        dateOldMossa = document['eta']
        print('Nuovo comando')
        exec(document["mosse"])


def list_doc():
    database = Database(client)
    print_green("--Running List Document API")
    response = database.list_documents(collectionId)
    execJson(response)


def mainLoop():
    expression()
    list_doc()
    t.after(3000, mainLoop)


def stop():
    print("stop")


t.after(0, mainLoop)
t.bind("<Escape>", lambda event: t.destroy())
tkinter.mainloop()
