#import AppWrite
from appwrite.client import Client
from appwrite.services.database import Database
from appwrite.services.storage import Storage

import urllib3


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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

collectionId = '60d2f79f5ffc1'
userId = '60d2f78729a5c'

dateOldMossa = ""

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



database = Database(client)
response = database.list_documents(collectionId)
document = response["documents"][0]
autonomo = document["autonomo"]

print(autonomo)
   
