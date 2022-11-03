#Importing Libraries
import RPi.GPIO as GPIO
import time
import math
 
#GPIO Mode - GPIO pin number
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 21
GPIO_ECHO = 20
LED = 2
 
# GPIO warning set to false
GPIO.setwarnings(False)

# Setting GPIO pins either input or output
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

# PWM for LED pin (max value 100)
P = GPIO.PWM(LED,100)
 
def distance():
    # setting Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # delay of 0.00001
    time.sleep(0.00001)
    
    # setting Trigger to Low
    GPIO.output(GPIO_TRIGGER, False)
 
    # For calculating the time
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    Time_difference = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (Time_difference * 34300) / 2
 
    return distance
 
try:
    while True:
        # calculating distance and displaying on the terminal
        dist = distance()
        print ("Measured Distance = " +  str(dist) + " cm")
        
        # controlling the analogue pin of LED
        if dist < 100:
            P.start(math.ceil(100 - dist))
        else:
            P.start(1)
        
        #Delay of one second
        time.sleep(1)
 
except KeyboardInterrupt:
    GPIO.cleanup()

