import os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

run = True


def speak(text, filename):
    if os.path.exists(filename):
        os.remove(filename)
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    playsound(filename)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said


while run == True:

    text = get_audio()

    if "hello" in text:
        speak("Hello, how are you?", 'prova.mp3')


    if "what are you" in text:
        print("")
        speak("I am a speech recognition program", 'prova.mp3')

    if "goodbye" in text:
        speak("Talk to you later" or "Cya" or "Bye", 'prova.mp3')
        run = False
