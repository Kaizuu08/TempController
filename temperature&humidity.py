#importing the module
import Adafruit_DHT
#import matplotlib.pyplot as plt , can be used for plotting data
import time
from twilio.rest import Client

account_sid = ''
auth_token = ''
twilio_client = Client(account_sid, auth_token)


dht_sensor = Adafruit_DHT.DHT11
pin = 2#whatever GPIO pin number

for i in range(2):
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, pin)
    
    if temperature is not None and humidity is not None:
        print(f"Reading {i + 1}: Temperature = {temperature:.2f}°C, Humidity = {humidity:.2f}%")
        '''#if temperature >= 30:
            #code for led flashing

            #code for twilio alert
                message = twilio_client.messages.create(
                from_="",
                body=f"server room is overheating {temperature:.2f}",
                to=""
            )
            
            print(f"Message ID: {message.sid}")'''

else:
    print("reading failed")
    
#how long befor next read
time.sleep(10)