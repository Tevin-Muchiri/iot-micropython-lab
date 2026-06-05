# Quick Reference: Arduino UNO R3 + WiFi Shield/Module + DHT22

## Wiring

### DHT22 to Arduino UNO R3

| DHT22 Pin | Arduino UNO R3 Pin |
|---|---|
| VCC | 5V |
| DATA | D6 |
| GND | GND |

Add a 10kΩ pull-up resistor between DHT22 VCC and DATA.

D6 is used because some WiFi shields reserve other pins such as SPI pins and may also use D7 or D4.

## Arduino IDE Libraries

Install from Library Manager:

- PubSubClient
- DHT sensor library by Adafruit
- Adafruit Unified Sensor

The classic Arduino `WiFi` library is normally available with the Arduino IDE.

If your WiFi module is WiFiNINA-based, change this line:

```cpp
#include <WiFi.h>
```

to:

```cpp
#include <WiFiNINA.h>
```

and install the WiFiNINA library.

## Upload Steps

1. Open `uno_r3_wifi_shield_mqtt_dht22.ino`.
2. Change:

```cpp
char WIFI_SSID[] = "YOUR_WIFI_NAME";
char WIFI_PASSWORD[] = "YOUR_WIFI_PASSWORD";
```

3. Select board: **Arduino Uno**.
4. Select the correct COM port.
5. Upload the sketch.
6. Open Serial Monitor at **9600 baud**.

## Expected Serial Monitor Output

```text
Arduino UNO R3 + WiFi Shield + DHT22 MQTT Publisher
WiFi connected successfully!
IP Address: 192.168.x.x
MQTT connected successfully!
Message #: 1
Temperature: 24.5 °C
Humidity: 61.2 %
JSON: {"device":"UNO-R3-WIFI-SHIELD-DHT22",...}
Published successfully!
```

## PC Side

Run the same PC subscriber:

```bash
python subscriber_sqlite.py
```

Then verify database:

```bash
python check_database.py
```

## Troubleshooting

- WiFi shield not detected: reseat the shield and check library compatibility.
- Compilation error on `WiFi.h`: your module may need `WiFiNINA.h` or another library.
- MQTT not connecting: check internet access and broker/topic settings.
- DHT error: check DHT data pin D6 and 10kΩ pull-up resistor.
- Database empty: make sure the PC subscriber is running while Arduino is publishing.
