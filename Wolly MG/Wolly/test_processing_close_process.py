import multiprocessing
import time
import psutil

def chiudi2():
    global process2, pids
    process2.terminate()
    start2()

def start2():
    global process2, pids
    process2 = multiprocessing.Process(target=faccia)
    process2.start()
    print("riapro faccia")
    
    
    
    
    
def chatInit():
    global process2, parentpid
    print("chiusura faccia")
    chiudi2()
    parentpid = multiprocessing.current_process().pid
    while True:
        print("chat {}".format(multiprocessing.current_process().pid))
        time.sleep(2)
        
    
def faccia():
    pids = multiprocessing.current_process().pid
    while True:
        print("ciao")
        time.sleep(2)
        print("faccia {}".format(multiprocessing.current_process().pid))
    
def master():
    global process2, parentpid
    process2 = multiprocessing.Process(target=faccia)
    process2.start()
    time.sleep(3)
    process3 = multiprocessing.Process(target=chatInit)
    process3.start()
    print("aspetto chiusura p2")
    time.sleep(12)
    parent = psutil.Process(parentpid)
    parent.terminate()
    print("CHIUDO DEF FACCIA")
    
    
    
if __name__ ==  "__main__":
    global process2
    process1 = multiprocessing.Process(target=master)
    process1.start()