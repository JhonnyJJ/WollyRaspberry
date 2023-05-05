import multiprocessing
import time

from os import getpid

    
    
    
def chatInit(event):
    global process2
    print("chiusura faccia")
    process2 = multiprocessing.Process(target=faccia)
    process2.start()
    print("riapro faccia")
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
    process2.terminate()
    process3 = multiprocessing.Process(target=chatInit, args=(event,))
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