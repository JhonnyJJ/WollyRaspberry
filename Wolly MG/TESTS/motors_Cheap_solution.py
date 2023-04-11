import RPi.GPIO as GPIO
from time import sleep
 
leftForward = 7
leftBackward = 11
leftEnable = 13
 
rightForward = 8
rightBackward = 10
rightEnable = 12
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
 
GPIO.setup(leftForward, GPIO.OUT)
GPIO.setup(leftBackward, GPIO.OUT)
GPIO.setup(leftEnable, GPIO.OUT)
GPIO.setup(rightForward, GPIO.OUT)
GPIO.setup(rightBackward, GPIO.OUT)
GPIO.setup(rightEnable, GPIO.OUT)
 
leftEnPWM = GPIO.PWM(leftEnable, 100)
leftEnPWM.start(50)
GPIO.output(leftEnable, GPIO.HIGH)
 
rightEnPWM = GPIO.PWM(rightEnable, 100)
rightEnPWM.start(50)
GPIO.output(rightEnable, GPIO.HIGH)

def muovi():
    GPIO.output(leftForward, GPIO.HIGH)
    GPIO.output(rightForward, GPIO.HIGH)
    leftEnPWM.ChangeDutyCycle(50)
    rightEnPWM.ChangeDutyCycle(50)
    sleep(0.1)
    GPIO.output(leftForward, GPIO.LOW)
    GPIO.output(rightForward, GPIO.LOW)
    
