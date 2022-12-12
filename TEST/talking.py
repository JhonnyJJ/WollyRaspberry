from pygame import mixer
from gtts import gTTS

def textSpeech(text):
    mixer.init()
    print(text)
    tts = gTTS(text=text, lang='it')
    tts.save('tts.mp3')
    mixer.music.load('tts.mp3')
    mixer.music.play()