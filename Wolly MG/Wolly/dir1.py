from threading import Thread, Event
import time
from dir2 import method_generic

can_continue = Event()
buffer = []

def main():
    th1 = Thread(target=method_generic, args=(can_continue, buffer))
    th1.start()
    time.sleep(5)
    can_continue.set()
    th1.join()
    print(buffer)

if __name__=="__main__":
    main()