#include <WiFi.h>
#include <PubSubClient.h>

// my WiFi credentials
const char* ssid = "Bilou";
const char* password = "balaboula";

// MQTT broker
const char* mqttServer = "172.20.10.4";
const int mqttPort = 1883;

// GPIO pins

const int potPin = 34; // trim pot connected to GPIO34

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);



  // Connecting to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Setting MQTT server
  client.setServer(mqttServer, mqttPort);

  // Connecting to MQTT broker
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP32Client_bilal")) {
      Serial.println("Connected to MQTT");
    }
    else {
      Serial.print("Failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }

  // Subscribing to the MQTT topic to control the LED
  client.subscribe("light/control");
}

void loop() {
  client.loop();  // maintaining MQTT connection and checking for incoming messages

  if (!client.connected()) {
    while (!client.connected()) {
      if (client.connect("ESP32Client")) {
      }
      else {
        delay(5000);
      }
    }
  }

  // Reading from trim pot and publishing to MQTT
  int potValue = analogRead(potPin);
  String potValueStr = String(potValue);
  client.publish("sensor/light", potValueStr.c_str());

//Serial.println(potValue);

  delay(1000);  // Delay a bit before the next reading
}

// This function is called whenever a message is received on a subscribed topic
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();
}
