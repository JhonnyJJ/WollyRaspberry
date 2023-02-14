import multiprocessing
import chatbot
import trackingFace

def chatting():
    chatbot.main()

def tracking(): #Inserisci direttamente i codici se non dovesse andare
    trackingFace.main()

if __name__ == '__main__':
    chat = multiprocessing.Process(target=chatting())
    track = multiprocessing.Process(target=tracking())

track.start()
chat.start()

track.join()
chat.join()
