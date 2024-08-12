import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

servo_pin = 17
GPIO.setup(servo_pin, GPIO.OUT)

# Set the PWM frequency to 50Hz
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # Rotate servo to 0 degrees
        SetAngle(0)
        time.sleep(2)
        
        # Rotate servo to 90 degrees
        SetAngle(90)
        time.sleep(2)
        
        # Rotate servo to 180 degrees
        SetAngle(180)
        time.sleep(2)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
