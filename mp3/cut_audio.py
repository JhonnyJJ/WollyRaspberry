from pydub import AudioSegment

song = AudioSegment.from_mp3("hearing.mp3")

start_min = 0
start_sec = 0
end_min = 0
end_sec = 1

start = ((start_min*60)+start_sec)*1000
end =  ((end_min*60)+end_sec)*1000

middle = song[start: end]

middle.export("hearing.mp3", format = "mp3")
print("fatto")