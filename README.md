# iot_project
Student name: Bilal El Barbir 
Course name: “IoT : Intro to python” 
Project name: "Smart IoT Light Monitoring and Control System Using ESP32, BBB, MQTT, SQLite, and Flask" 
Date: Thursday August 24, 2023


Project's instructions:

- Build a system with the following components:
  
1. MQTT broker on Raspbery Pi or BeagleBone SBC
2. An ESP32 (or similar MCU) node with a simple photocell light measuring circuit publishes MQTT messages to this broker under the sensor/light category
   
- The following programs run as services automatically started at boot time by the Linux OS on the SBC:

3. A Python script subscribes and listens to messages in the sensor/light and stores them to a SQLITE database.
4. A Flask Python application serves visualisation of the data in the SQLITE DB and takes user input to set the desired light value. This application is served up by an uWSGI server to port 80. This Web application is accessible by other computers on the same network.
5. A third Python program either controls a light connected to the SBC or a light connected to an ESP32. This happens when the value is below the set threshold.  In the case where this LED is connected to an ESP32, then the light is controlled by MQTT messages published by this program and subscribed-to by the ESP32 program.
