from pydub import AudioSegment

song = AudioSegment.from_mp3("elefante.mp3")

start_min = 0
start_sec = 0
end_min = 0
end_sec = 8

start = ((start_min*60)+start_sec)*1000
end =  ((end_min*60)+end_sec)*1000

middle = song[start: end]

middle.export("elefante.mp3", format = "mp3")
print("fatto")