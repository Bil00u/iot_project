import sqlite3
import paho.mqtt.client as mqtt

print("Starting script...")

# my MQTT broker information
broker_address = "172.20.10.4"
broker_port = 1883
mqtt_topic = "sensor/light"

# SQLite database file path
db_file = "/home/debian/iot_project/light_data.db"

# Callback functions for MQTT connection events
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker successfully.")
    else:
        print("Failed to connect to MQTT broker: return code =", rc)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection from MQTT broker.")

# Callback function for receiving MQTT messages
def on_message(client, userdata, message):
    print("Received message.")
    # Extracting the payload (light value) from the MQTT message
    light_value = float(message.payload.decode())
    print("Light value:", light_value)  # Prints the received light value
    
    # Storing the light value in the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Creating the table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS light_data (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp INTEGER, value REAL)")
    
    # Inserting the light value into the table along with the current timestamp
    cursor.execute("INSERT INTO light_data (timestamp, value) VALUES (strftime('%s','now'), ?)", (light_value,))
    print("Inserted into the database")  # Prints a confirmation message after inserting the data
    
    # Committing the changes and closing the database connection
    conn.commit()
    conn.close()

# Creating an MQTT client and setting the callback functions
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connecting to the MQTT broker and subscribing to the topic
client.connect(broker_address, broker_port)
client.subscribe(mqtt_topic)

# Starting the MQTT loop to handle incoming messages
client.loop_forever()

