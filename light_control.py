from flask_sqlalchemy import SQLAlchemy
import Adafruit_BBIO.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

# Importing my Flask app, models, and db from my_flask_app.py
import my_flask_app
from my_flask_app import db, LightData, Threshold

# Connecting to the local MQTT broker
client = mqtt.Client()
client.connect("localhost", 1883, 60)

# the light is connected to GPIO pin "P9_14"
light = "P9_14"
GPIO.setup(light, GPIO.OUT)

def control_light():
    while True:
        # Get the current threshold
        threshold = Threshold.query.get(1).value

        # Get the latest light data
        latest_data = LightData.query.order_by(LightData.timestamp.desc()).first()

        if latest_data is not None:
            if latest_data.value < threshold:
                # Turn on the light
                GPIO.output(light, GPIO.HIGH)

                # Publish an MQTT message to turn on the ESP32 light
                client.publish("light/control", "on")
            else:
                # Turn off the light
                GPIO.output(light, GPIO.LOW)

                # Publish an MQTT message to turn off the ESP32 light
                client.publish("light/control", "off")

        # Sleep for a bit to prevent the loop from running too fast
        time.sleep(1)

if __name__ == "__main__":
    with my_flask_app.app.app_context():
        control_light()
