/*
  Arduino UNO R3 + ESP8266/ESP-01 AT WiFi Module + DHT22 + MQTT Publisher
  ICS 4111: Embedded Systems & IoT Lab

  System flow:
  DHT22 -> Arduino UNO R3 -> ESP8266 AT WiFi -> MQTT broker -> PC subscriber -> SQLite

  Required Arduino IDE libraries:
  - WiFiEspAT
  - PubSubClient
  - DHT sensor library by Adafruit
  - Adafruit Unified Sensor

  IMPORTANT ESP8266 HARDWARE NOTES:
  - ESP8266 is 3.3V only.
  - Do NOT power ESP8266 from Arduino UNO 3.3V pin. Use external 3.3V regulator, 500 mA or more.
  - Do NOT connect Arduino TX directly to ESP8266 RX. Use voltage divider or level shifter.
  - Common GND is required between Arduino, ESP8266, DHT22, and power supply.
*/

#include <SoftwareSerial.h>
#include <WiFiEspAT.h>
#include <PubSubClient.h>
#include <DHT.h>

// =========================
// WiFi Configuration
// =========================
char WIFI_SSID[] = "YOUR_WIFI_NAME";
char WIFI_PASSWORD[] = "YOUR_WIFI_PASSWORD";

// =========================
// MQTT Configuration
// =========================
const char MQTT_BROKER[] = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char MQTT_TOPIC[] = "iot/lab/sensor";

// =========================
// Hardware Pins
// =========================
// Arduino D2 receives from ESP8266 TX
// Arduino D3 transmits to ESP8266 RX through voltage divider / level shifter
const int ESP8266_RX_TO_ARDUINO_PIN = 2;
const int ESP8266_TX_FROM_ARDUINO_PIN = 3;

// DHT22 data pin
const int DHT_PIN = 7;
#define DHT_TYPE DHT22

// =========================
// Publishing Configuration
// =========================
const unsigned long PUBLISH_INTERVAL_MS = 3000;

// If your ESP8266 AT firmware uses 115200 baud, change it to 9600 first if possible.
// SoftwareSerial is more stable at 9600 on Arduino UNO.
const long ESP8266_BAUD = 9600;

// =========================
// Global Objects
// =========================
SoftwareSerial espSerial(ESP8266_RX_TO_ARDUINO_PIN, ESP8266_TX_FROM_ARDUINO_PIN);
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
DHT dht(DHT_PIN, DHT_TYPE);

unsigned long lastPublishTime = 0;
unsigned long startTime = 0;
unsigned long messageCounter = 0;

void connectWiFi() {
  Serial.println();
  Serial.println("Initialising ESP8266 AT module...");

  WiFi.init(espSerial);

  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("ESP8266 module not detected.");
    Serial.println("Check wiring, power, baud rate, and AT firmware.");
    while (true) {
      delay(1000);
    }
  }

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to WiFi: ");
    Serial.println(WIFI_SSID);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    delay(8000);
  }

  Serial.println("WiFi connected successfully!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT broker: ");
    Serial.println(MQTT_BROKER);

    char clientId[40];
    snprintf(clientId, sizeof(clientId), "uno-r3-esp8266-%lu", millis());

    if (mqttClient.connect(clientId)) {
      Serial.println("MQTT connected successfully!");
      Serial.print("Publishing to topic: ");
      Serial.println(MQTT_TOPIC);
    } else {
      Serial.print("MQTT failed, state: ");
      Serial.println(mqttClient.state());
      Serial.println("Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void publishSensorData() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("DHT22 read failed. Check wiring and pull-up resistor.");
    return;
  }

  messageCounter++;
  unsigned long uptimeSeconds = (millis() - startTime) / 1000;

  // AVR UNO does not reliably support float formatting in sprintf/snprintf.
  // Convert floats to strings first using dtostrf().
  char temperatureText[12];
  char humidityText[12];
  dtostrf(temperature, 4, 1, temperatureText);
  dtostrf(humidity, 4, 1, humidityText);

  char payload[180];
  snprintf(
    payload,
    sizeof(payload),
    "{\"device\":\"UNO-R3-ESP8266-DHT22\",\"message_no\":%lu,\"temperature\":%s,\"humidity\":%s,\"uptime_seconds\":%lu}",
    messageCounter,
    temperatureText,
    humidityText,
    uptimeSeconds
  );

  Serial.println("==================================================");
  Serial.print("Message #: ");
  Serial.println(messageCounter);
  Serial.print("Temperature: ");
  Serial.print(temperatureText);
  Serial.println(" °C");
  Serial.print("Humidity: ");
  Serial.print(humidityText);
  Serial.println(" %");
  Serial.print("JSON: ");
  Serial.println(payload);

  bool success = mqttClient.publish(MQTT_TOPIC, payload);

  if (success) {
    Serial.println("Published successfully!");
  } else {
    Serial.println("MQTT publish failed.");
  }
}

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;
  }

  Serial.println("============================================================");
  Serial.println("Arduino UNO R3 + ESP8266 AT + DHT22 MQTT Publisher");
  Serial.println("============================================================");

  dht.begin();
  startTime = millis();

  espSerial.begin(ESP8266_BAUD);
  delay(2000);

  connectWiFi();

  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);

  Serial.println("Starting sensor readings...");
  Serial.println("Press reset to restart.");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected. Reconnecting...");
    connectWiFi();
  }

  if (!mqttClient.connected()) {
    reconnectMQTT();
  }

  mqttClient.loop();

  unsigned long currentTime = millis();
  if (currentTime - lastPublishTime >= PUBLISH_INTERVAL_MS) {
    lastPublishTime = currentTime;
    publishSensorData();
  }
}
