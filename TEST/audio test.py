import time
from pygame import mixer
from gtts import gTTS

def speak(text,filename):
    mixer.init()
    print('parla')
    tts = gTTS(text=text, lang='it')
    tts.save(filename)
    mixer.music.load(filename)
    mixer.music.play()
    
run = True

while run == True:
    
    text = input()
    
    if "hello" in text:
        speak("Ciao Umano", 'prova.mp3')
        
    if "goodbye" in text:
        speak("Ciao", 'prova.mp3')
        run = False