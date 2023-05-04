import multiprocessing
import time
from os import kill
from os import getpid
from signal import SIGKILL

def chiudi2():
    global process2, pids
    process2.terminate()
    start2()

def start2():
    global process2, pids
    process2 = multiprocessing.Process(target=faccia)
    process2.start()
    print("riapro faccia")
    
    
    
    
    
def chatInit(event, i):
    global process2
    print("chiusura faccia")
    chiudi2()
    while not event.is_set():
        print("chat {}".format(multiprocessing.current_process().pid))
        time.sleep(2)
    process2.terminate()
        
    
def faccia():
    global pids
    pids = getpid()
    while True:
        print("ciao")
        time.sleep(2)
        print("faccia {}".format(multiprocessing.current_process().pid))
    
def master():
    global process2, pids
    event = multiprocessing.Event()
    process2 = multiprocessing.Process(target=faccia)
    process2.start()
    time.sleep(3)
    process3 = multiprocessing.Process(target=chatInit, args=(event, i))
    process3.start()
    print("aspetto chiusura p2")
    time.sleep(10)
    event.set()
    process3.join()
    print("CHIUDO DEF FACCIA")
    
    
    
if __name__ ==  "__main__":
    global process2
    process1 = multiprocessing.Process(target=master)
    process1.start()