import os
import speech_recognition as sr
from pygame import mixer
from gtts import gTTS

r = sr.Recognizer()
mic = sr.Microphone()

run = True

def speak(text,filename):
    if os.path.exist(filename):
        os.remove(filename)
    mixer.init()
    print('parla')
    tts = gTTS(text=text, lang='it')
    tts.save(filename)
    mixer.music.load(filename)
    mixer.music.play()
    
def get_audio():
    with sr.Microphone() as source:
        listen = sr.Recognizer()
        listen.energy_threshold = 335.9141163575556
        #r.adjust_for_ambient_noise(source)
        listen.dynamic_energy_threshold = True
        audio = listen.listen(source)
        said = ""
        
        try:
            said = r.recognize_google(audio, lang = "ita")
            print(said)
        except Exeption as e:
           print("Eception:" + str(e))
    
    return said


while run == True:
    
    text = get_audio()
    
    if "hello" in text:
        speak("hello human", 'prova.mp3')
        
    if "goodbye" in text:
        speak("goddbye Human", 'prova.mp3')
        run = False
