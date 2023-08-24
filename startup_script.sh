#!/bin/bash

# Start Mosquitto
mosquitto &

# Navigate to the project directory
cd ~/iot_project

# Start the Python scripts
python3 light_control.py &
python3 light_subscriber.py &

# Start the uwsgi server
uwsgi --socket 0.0.0.0:8082 --protocol=http -w wsgi:app &

