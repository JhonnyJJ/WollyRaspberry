import signal
import sys
import multiprocessing
from chatbot import main as recognize_speech
from trackingFace import main as track

def signal_handler(sig, frame):
    print('You ended the program')
    process1.terminate()
    process2.terminate()
    sys.exit(0)

if __name__ == '__main__':
    print('Press Ctrl+C to stop the program')
    process1 = multiprocessing.Process(target=recognize_speech)
    process2 = multiprocessing.Process(target=track)
    process1.start()
    process2.start()
    signal.signal(signal.SIGINT, signal_handler)


    

