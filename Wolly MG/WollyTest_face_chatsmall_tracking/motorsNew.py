import time
from adafruit_motorkit import MotorKit
# Waveshare Motor Driver Hat 0x40
kit = MotorKit(0x40)

# speed is a value from 0.6(it should be 0 but probably it's not enough energy to power the motors) to 1.0, where 1.0 is full throttle and 0.5 is power off
# duration is a value in seconds and is used to indicate for how much time the motor execute the movement

def avanti(duration, speed): 
    kit.motor1.throttle = speed
    kit.motor2.throttle = speed
    
    time.sleep(duration)
    
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    
def indietro(duration, speed):
    kit.motor1.throttle = -speed
    kit.motor2.throttle = -speed
    
    time.sleep(duration)
    
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    
def destra(duration, speed): 
    kit.motor1.throttle = speed
    kit.motor2.throttle = -speed
    
    time.sleep(duration)
    
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    
def sinistra(duration, speed): 
    kit.motor1.throttle = -speed
    kit.motor2.throttle = speed
    
    time.sleep(duration)
    
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0