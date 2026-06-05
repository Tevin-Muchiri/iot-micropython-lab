# Arduino UNO R3 + DHT22 + MQTT Lab Options

This pack gives two Arduino UNO R3 versions of the same lab system already used for the ESP32 setup:

```text
DHT22 sensor → Arduino UNO R3 → WiFi module/shield → MQTT broker → PC subscriber → SQLite database
```

The MQTT broker, topic, and JSON fields are kept the same as the ESP32 version so the existing PC scripts can still be used.

## Common MQTT settings

```cpp
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT   = 1883
MQTT_TOPIC  = "iot/lab/sensor"
```

## Common JSON payload format

```json
{
  "device": "UNO-R3-...-DHT22",
  "message_no": 1,
  "temperature": 24.5,
  "humidity": 61.2,
  "uptime_seconds": 12
}
```

## Version A: UNO R3 + ESP8266 / ESP-01 AT WiFi module

Use this if you are given a small ESP8266 WiFi module such as ESP-01, or an ESP8266 shield that is controlled with AT commands.

Folder:

```text
UNO_R3_ESP8266_AT/
```

Main file:

```text
uno_r3_esp8266_at_mqtt_dht22.ino
```

Required Arduino IDE libraries:

- `WiFiEspAT`
- `PubSubClient`
- `DHT sensor library` by Adafruit
- `Adafruit Unified Sensor`

Important hardware warning:

- Arduino UNO R3 logic is 5V.
- ESP8266 logic is 3.3V.
- Do not connect UNO TX directly to ESP8266 RX without a voltage divider or level shifter.
- Do not power the ESP8266 from the UNO 3.3V pin. Use an external 3.3V regulator capable of around 500 mA or more.
- Connect all grounds together.

## Version B: UNO R3 + Arduino WiFi Shield / compatible WiFi module

Use this if you are given a classic Arduino WiFi Shield or compatible shield using the Arduino `WiFi.h` library.

Folder:

```text
UNO_R3_WIFI_SHIELD/
```

Main file:

```text
uno_r3_wifi_shield_mqtt_dht22.ino
```

Required Arduino IDE libraries:

- `WiFi` library
- `PubSubClient`
- `DHT sensor library` by Adafruit
- `Adafruit Unified Sensor`

Note: If your module is based on WiFiNINA, the sketch may need `#include <WiFiNINA.h>` instead of `#include <WiFi.h>`.

## PC side

The PC side stays the same:

```bash
python subscriber_sqlite.py
python check_database.py
```

The Arduino must be publishing to the same topic:

```text
iot/lab/sensor
```

## Screenshot evidence for report

Take these screenshots/photos:

1. Arduino + DHT22 + WiFi module wiring photo
2. Arduino IDE Serial Monitor showing published MQTT JSON messages
3. PC subscriber terminal showing messages received and saved
4. SQLite query output showing rows in `sensor_data.db`
