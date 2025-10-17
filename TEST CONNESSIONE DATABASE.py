#import AppWrite
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.services.databases import Databases

import urllib3


# ENDPOINT = 'https://9225438084d8.ngrok.io/v1'
# PROJECT_ID = '5fa7e32a5133e'
# API_KEY = '51935101e4598b8a6c6722c919757eab00614c5cf07320d2d4e894a9fc178dfc6e44f9811ac2426d16027197435c663f25665f5f1661aa00d345fb8bef2a177c2ddbee5727e26cb348c99f5a54507f81897a13602b2af124255f7375867cf183c0afbedaa361b4eed1581d94366a327f81588fe233de9282e098ff7207530301'

ENDPOINT = 'http://app.wollybrain.di.unito.it/v1'
PROJECT_ID = '68e6c71b003332bc20b7'
API_KEY = 'standard_786402a023b1896fd3c5c2f41ab730dc7d338bf0522bffbf1fdbdb3abccac3633069d35cd465daf557ebbb8a7429d2bfa144df08e7591e9a1d7d610dad18ed161cc735c98add6ff0dbf6ef3d409f845754923cd767e73a5c801e839d2035dedca0003569c5ee96dcc72f9e818e72d9b79d987303232b1596153aee7120ebfd50'

client = Client()

client.set_endpoint(ENDPOINT)
client.set_project(PROJECT_ID)
client.set_key(API_KEY)
# client.add_header("Origin", ENDPOINT)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

collectionId = '68e6c7670001f5068527'
userId = '68e6d30700399e09b501'
databaseId = '68e6c75a00267bc0a9b9'

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
    database = Databases(client)
    print_green("Running List Document API")
    response = database.list_documents(databaseId, collectionId)
    execJson(response)



database = Databases(client)
response = database.list_documents(databaseId, collectionId)
document = response["documents"][0]
autonomo = document["autonomo"]

print(autonomo)
   
