# Board Selection Cheat Sheet

Use this when you enter the lab and do not know which board you will receive.

| Board received | Use this folder | Code file to run/upload | Main difference |
|---|---|---|---|
| ESP8266 / NodeMCU | `ESP8266_NodeMCU` | Save `main.py` to device | MicroPython, WiFi credentials inside code |
| Raspberry Pi 4 / 5 | `Raspberry_Pi_4_5_Standard_Python` | Run `python3 raspberry_pi_publisher.py` | Standard Python, WiFi handled by Raspberry Pi OS |
| Raspberry Pi Pico W | `Raspberry_Pi_Pico_W_MicroPython` | Save `main.py` to device | MicroPython, WiFi credentials inside code |
| Normal Raspberry Pi Pico | Not directly supported for MQTT | Needs external WiFi module | No built-in WiFi |

All publisher files use the same MQTT broker and topic:

```text
broker.hivemq.com
Topic: iot/lab/sensor
```

All publisher files send compatible JSON fields:

```json
{
  "device": "BOARD-DHT22",
  "message_no": 1,
  "temperature": 24.5,
  "humidity": 61.2,
  "uptime_seconds": 12
}
```

Therefore, the same PC scripts can be used for all boards:

```bash
python subscriber_sqlite_all_boards.py
python check_database.py
```
