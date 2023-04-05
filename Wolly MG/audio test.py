import time
from pygame import mixer
from gtts import gTTS

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

    
run = True

while run == True:
    
    text = input()
    
    if "hello" in text:
        speak("Ciao Umano", 'prova.mp3')
        
    if "goodbye" in text:
        speak("Ciao", 'prova.mp3')
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(0.5)
        run = False