import pyttsx3
engine = pyttsx3.init()

engine.setProperty('voice', 'italian')
engine.setProperty('rate', 120)
engine.say("ciao sono Wolly, è un piacere conoscerti")
# engine.save_to_file('ciao sono Wolly, è un piacere conoscerti', 'pyttsx3_prove.mp3')
engine.runAndWait()