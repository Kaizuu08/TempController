#importing the module
import RPi.GPIO as GPIO
import Adafruit_DHT
import matplotlib.pyplot as plt
import time
from datetime import datetime
from twilio.rest import Client
import threading

#<------------ Setup Pins ------------>#
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

led_pin = 21 #<--------Change pin number respectively
GPIO.setup(led_pin, GPIO.OUT)

dht_sensor = Adafruit_DHT.DHT11
dht_pin = 14 #<--------Change pin number respectively
#GPIO.setup(dht_sensor, GPIO.OUT/IN) <---------------- Look at requiring this maybe? - Duc

servo_pin = 16 #<--------Change pin number respectively
GPIO.setup(servo_pin, GPIO.OUT)

# PWM setup 
pwm_frequency = 50 
pwm = GPIO.PWM(servo_pin, pwm_frequency)
pwm.start(7.5)  # or some other default position


#<------------ Functions Here ----------->#

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
    distance = (TimeElapsed * 34300)/2
    return distance
    

def flash_led():
    while thread_running:
        GPIO.output(led_pin, True)
        time.sleep(flash_frequency)
        GPIO.output(led_pin, False)
        time.sleep(flash_frequency)
    
    
def distAlert ():
    account_sid = 'ACdb17449935677facbeaa404b87a989ce'
    auth_token = '14c3254a6b583f37a15c4ea3fb10c36f'
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body = "Distance Alert: Someone in close proximity to server room",
            from_ = "+12565988247",
            to = "+61437238566"
        )
    
def tempAlert ():
    account_sid = 'ACdb17449935677facbeaa404b87a989ce'
    auth_token = '14c3254a6b583f37a15c4ea3fb10c36f'
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body = "Temperature Alert: Server room is above 30 - Cooling fan in operation",
            from_ = "+12565988247",
            to = "+61437238566"
        )

def setServo ():
    while thread_running:
        pwm.ChangeDutyCycle(2.5) #<------------------------- fan spin cycle ? - Duc
        time.sleep(1)
        pwm.ChangeDutyCycle(12.5)
        time.sleep(1)


def show_plot():
    plt.plot(timeList, tempList, marker="*")
    plt.title("Cooling Process")
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.grid(axis = 'y')
    plt.show()

# Used to store the state of the dist alert i.e sent or not sent (TRUE/FALSE)
dist_alert_sent = False

# Read the temperature and humidity
humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

# Used to store how fast the LED flashes
flash_frequency = 1

# Store the state of the thread i.e running or not running
thread_running = True

# Using try and expect so when the program is interupted the GPIO pins are cleanedup
try:
    # Continuous loop to check the temperature & humidity
    while (True):
        """
        * If the temperature goes over 30:
            * Start the servo
            * Flash the LED
            * Check the distance and send the alert

        If the temperature goes over 30 it will only break the if statement
        once the temperature goes below 20
        """
        print(temperature)
        if temperature >= 30:
            print(temperature,"overheat")
            # Threads for LED flashing and Servo so they can operate simultaniously
            servo_thread = threading.Thread(target=setServo)
            led_thread = threading.Thread(target=flash_led)

            # Initiate lists to store temperature, humidity and time
            tempList = []
            humList = []
            timeList = []

            # Send temperature alert
            tempAlert()
            

            # Flash the LED and start the servo
            servo_thread.start()
            led_thread.start()

            while temperature >= 28:
                print(temperature,"cooling")
                """
                If the distance sensors picks something up one meter away or closer
                it will:
                    * Send a distance alert 
                    * Flash the LED faster
                """

                dist = checkDist()

                if dist <= 10:
                    flash_frequency = 0.2

                    if not dist_alert_sent:
                        distAlert()
                        dist_alert_sent = True
                else:
                    flash_frequency = 1

                    if dist_alert_sent:
                        dist_alert_sent = False
                
                #Append the temperature, humidity and time to their respective lists
                tempList.append(temperature)
                humList.append(humidity)
                timeList.append(datetime.now().strftime("%X"))

                # Read the temperature again to check if it's still above 20
                humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

            # Stop the LED and servo thread which turns the servo and led off
            thread_running = False
            servo_thread.join()
            led_thread.join()
            pwm.stop()
            GPIO.output(led_pin, False)

            """
            Once the temperature has been brought down to a normal level, plot and
            display a Temperature vs Time graph to show the cooling process
                * A thread is used for the plot so that when the plot is displayed it 
                  doesnt affect the rest of the program
            """
            plot_thread = threading.Thread(target=show_plot)
            plot_thread.start()
        
        # Sets the threads running state to true again
        thread_running = True

        # Read the temperature and humidity
        humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

except KeyboardInterrupt:
    print("Program shutting down...")
    pwm.stop()
    GPIO.cleanup()

