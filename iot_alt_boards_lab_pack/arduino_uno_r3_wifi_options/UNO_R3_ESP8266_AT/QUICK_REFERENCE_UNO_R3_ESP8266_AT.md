# Quick Reference: Arduino UNO R3 + ESP8266/ESP-01 AT + DHT22

## Wiring

### DHT22 to Arduino UNO R3

| DHT22 Pin | Arduino UNO R3 Pin |
|---|---|
| VCC | 5V |
| DATA | D7 |
| GND | GND |

Add a 10kΩ pull-up resistor between DHT22 VCC and DATA.

### ESP8266 / ESP-01 to Arduino UNO R3

| ESP8266 / ESP-01 Pin | Connection |
|---|---|
| VCC | External 3.3V regulator output |
| GND | Common GND with Arduino |
| CH_PD / EN | 3.3V |
| RST | 3.3V or leave pulled up |
| TX | Arduino D2 |
| RX | Arduino D3 through voltage divider / level shifter |

Recommended voltage divider for Arduino D3 to ESP8266 RX:

```text
Arduino D3 ---- 1kΩ ---- ESP8266 RX ---- 2kΩ ---- GND
```

This reduces the Arduino 5V signal to about 3.3V.

## Arduino IDE Libraries

Install from Library Manager:

- WiFiEspAT
- PubSubClient
- DHT sensor library by Adafruit
- Adafruit Unified Sensor

## Upload Steps

1. Open `uno_r3_esp8266_at_mqtt_dht22.ino`.
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
Arduino UNO R3 + ESP8266 AT + DHT22 MQTT Publisher
WiFi connected successfully!
IP Address: 192.168.x.x
MQTT connected successfully!
Message #: 1
Temperature: 24.5 °C
Humidity: 61.2 %
JSON: {"device":"UNO-R3-ESP8266-DHT22",...}
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

- ESP8266 not detected: check power, CH_PD/EN pin, baud rate, and wiring.
- Random resets: use a stronger 3.3V regulator for ESP8266.
- Garbage in Serial Monitor: check baud rate.
- MQTT not connecting: check WiFi, internet, topic, and broker.
- DHT error: check DHT data pin D7 and 10kΩ pull-up resistor.
