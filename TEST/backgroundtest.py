#TESTARE THREADING USANDO un processo con il microfono e l'altro con un time.sleep
import speech_recognition as sr
from multiprocessing import Process

# funzione per il riconoscimento vocale
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    text = r.recognize_google(audio)
    print("You said:", text)

# eseguiamo il riconoscimento vocale in un processo parallelo
if __name__ == '__main__':
    p = Process(target=recognize_speech)
    p.start()

# qui possiamo continuare ad eseguire il codice dello script principale
