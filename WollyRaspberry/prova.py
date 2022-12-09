# Metodi uso database

def list_collection():
    database = Database(client)
    print_green("Running List Collection API")
    response = database.list_collections()
    collection = response['collections'][0]
    print(collection)


def list_doc():
    database = Database(client)
    print_green("Running List Document API")
    response = database.list_documents(collectionId)
    execJson(response)


def list_user():
    users = Users(client)
    print_green("Running List User API")
    response = users.list()
    print(response)


def list_files():
    storage = Storage(client)
    print_green("Running List Files API")
    result = storage.list_files()
    file_count = result['sum']
    print("Total number of files {} ".format(file_count))
    files = result['files']
    print(files)
