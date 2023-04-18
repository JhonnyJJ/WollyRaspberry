import time
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from Dialog import *
from frasiDialog import *


def playsound(filepath):
    mixer.init()
    mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.01)
    # pygame.quit()   #windows debug

def textSpeech(text):
    tts = gTTS(text=text, lang='it')
    tts.save("tts.mp3")
    playsound("tts.mp3")


# each time you need to use microphone to get recognized speech as a string you call this method
def talk():
    # value to keep track of how many tries the bot needs to ask
    i = 3

    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 0.8)
            # add sound to help to know when to talk
            playsound("../../mp3/hearing.mp3")
            time.sleep(0.7)
            print("ascolto")
            audio = r.listen(source, phrase_time_limit=6, timeout=None)

        try:
            response = r.recognize_google(audio, language="IT-IT")
            print(response)
            return response.lower()

        except sr.UnknownValueError:
            i = i - 1
            if i != 0:
                print("non ho capito, puoi ripetere?")
                textSpeech(random.choice(notundst))
            else:
                print("non riesco a capirti! vado a ricalibrare il mio microfono!")
                textSpeech(random.choice(noresponse) + " se hai ancora bisogno di me chiamami!")
                return False
            
            
# hardcoded chatbot AGGIUNGERE QUALCHE TIPO DI FACCIA CON DOMANDE O EMOZIONI
def chat(response):  # CREARE ALTRE DEF NEL CASO DI DIALOGO PIU' PROFONDO
    while True:
        if re.search(r"\bno\b", response):
            print(random.choice(noproblem) + random.choice(allora))
            textSpeech(random.choice(noproblem) + random.choice(allora))
            return curioso(talk())
        for word in ok:
            if re.search(word, response):  # parla di quello che sa fare wolly
                print(random.choice(fare))
                textSpeech(random.choice(ecco) + random.choice(fare) + random.choice(vedere))
                return richiesta(talk())

        # stop immediately
        for word in niente:
            if word in response:
                print(random.choice(noproblem) + " resto in ascolto")
                textSpeech(random.choice(noproblem) + " resto in ascolto")
                return
            
        error()
        response = talk()


def chatInit():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 1)
            print("ascolto")
            audio = r.listen(source, timeout=None, phrase_time_limit=6)

        try:
            text = r.recognize_google(audio, language="IT-IT")

            for word in wword:
                if re.search(word, text.lower()):
                    print(random.choice(responses) + random.choice(posso))
                    textSpeech(random.choice(responses) + random.choice(posso))

                    response = talk()
                    if response is not False:
                        chat(response)

        except sr.UnknownValueError:
            print("---------Non ho capito---------")
        except sr.RequestError as e:
            print("Errore con il collegamento API: {0}".format(e))
            

if __name__ == '__main__':
    chatInit()
