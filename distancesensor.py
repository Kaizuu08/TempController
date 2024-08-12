# Libraries setup
import RPi.GPIO as GPIO
import time
import os
from twilio.rest import Client

# Initialize the Twilio client
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24

led_pin = 4 #<--------Change pin number respectively

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# function to get distance
def checkDist():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    return distance

def flash_led(amount):
    for flashes in amount:
        GPIO.output(led_pin, True)
        time.sleep(1)
        GPIO.output(led_pin, False)


dist = checkDist()

# code to get distance and send alert
if not dist:
    print("Distance not measured - error")
else:
    flash_led(3) #
    print(f"Distance: {dist} cm")
    if dist > 0:
        message = client.messages.create(
            body=f"Someone detected at {dist} cm, contact the police.",
            from_='+15017122661',
            to='+15558675310'
        )
