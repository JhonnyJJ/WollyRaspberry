import multiprocessing
import chatbot
import trackingFace

def chatbot():
    chatbot.main()

def tracking(): #Inserisci direttamente i codici se non dovesse andare
    trackingFace.main()

if __name__ == '__main__':
    chat = multiprocessing.Process(target=chatbot())
    tracking = multiprocessing.Process(target=tracking())

chat.start()
tracking.start()

chat.join()
tracking.join()