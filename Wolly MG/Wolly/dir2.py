import random

def method_generic(can_cont, buffer):
    while not can_cont.is_set():
        buffer.append(random.randint(0, 50))
    print("fuori")
    