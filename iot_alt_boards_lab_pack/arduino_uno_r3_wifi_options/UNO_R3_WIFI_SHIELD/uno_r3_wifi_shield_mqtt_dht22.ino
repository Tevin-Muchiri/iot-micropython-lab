/*
  Arduino UNO R3 + Arduino WiFi Shield / WiFi Module + DHT22 + MQTT Publisher
  ICS 4111: Embedded Systems & IoT Lab

  System flow:
  DHT22 -> Arduino UNO R3 -> WiFi Shield/Module -> MQTT broker -> PC subscriber -> SQLite

  Required Arduino IDE libraries:
  - WiFi library
  - PubSubClient
  - DHT sensor library by Adafruit
  - Adafruit Unified Sensor

  Notes:
  - This version is for classic Arduino WiFi Shield / compatible modules using WiFi.h.
  - If your module uses WiFiNINA, replace #include <WiFi.h> with #include <WiFiNINA.h>.
  - DHT data pin is set to D6 to avoid common WiFi Shield pins.
*/

#include <SPI.h>
#include <WiFi.h>
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
// Sensor Configuration
// =========================
const int DHT_PIN = 6;
#define DHT_TYPE DHT22

// =========================
// Publishing Configuration
// =========================
const unsigned long PUBLISH_INTERVAL_MS = 3000;

// =========================
// Global Objects
// =========================
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
DHT dht(DHT_PIN, DHT_TYPE);

int wifiStatus = WL_IDLE_STATUS;
unsigned long lastPublishTime = 0;
unsigned long startTime = 0;
unsigned long messageCounter = 0;

void connectWiFi() {
  Serial.println();
  Serial.println("Checking WiFi shield/module...");

  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield/module not detected.");
    Serial.println("Check that the shield/module is fitted correctly.");
    while (true) {
      delay(1000);
    }
  }

  while (wifiStatus != WL_CONNECTED) {
    Serial.print("Connecting to WiFi: ");
    Serial.println(WIFI_SSID);

    wifiStatus = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    delay(10000);
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
    snprintf(clientId, sizeof(clientId), "uno-r3-wifi-%lu", millis());

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
    "{\"device\":\"UNO-R3-WIFI-SHIELD-DHT22\",\"message_no\":%lu,\"temperature\":%s,\"humidity\":%s,\"uptime_seconds\":%lu}",
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
  Serial.println("Arduino UNO R3 + WiFi Shield + DHT22 MQTT Publisher");
  Serial.println("============================================================");

  dht.begin();
  startTime = millis();

  connectWiFi();
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);

  Serial.println("Starting sensor readings...");
  Serial.println("Press reset to restart.");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected. Reconnecting...");
    wifiStatus = WL_IDLE_STATUS;
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
