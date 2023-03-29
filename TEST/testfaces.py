import signal
import sys
import multiprocessing
from Faces import main as face
from inputs import main as inputs


def signal_handler(sig, frame):
    print('You ended the program')
    process1.terminate()
    process2.terminate()
    sys.exit(0)

if __name__ == '__main__':
    print('Press Ctrl+C to stop the program')
    process1 = multiprocessing.Process(target=face)
    process2 = multiprocessing.Process(target=inputs)
    process2.start()
    process1.start()
    signal.signal(signal.SIGINT, signal_handler)