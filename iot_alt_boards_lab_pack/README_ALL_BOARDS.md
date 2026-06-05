# IoT Alternative Boards Lab Pack

This pack adapts the existing ESP32 DHT22 + MQTT + SQLite lab to the other possible boards:

1. ESP8266 / NodeMCU
2. Raspberry Pi 4 / 5 using Standard Python
3. Raspberry Pi Pico W using MicroPython

The original ESP32 workflow was preserved:

```text
Board + DHT22 -> MQTT broker -> PC subscriber -> SQLite database -> database check script
```

## Common PC workflow

Open Terminal 1:

```bash
cd common_pc_scripts
pip install paho-mqtt
python subscriber_sqlite_all_boards.py
```

Open Terminal 2 after collecting messages:

```bash
cd common_pc_scripts
python check_database.py
```

## Screenshots to collect

Use the same screenshots as the ESP32 lab:

1. Wiring photo showing DHT22, board, and pull-up resistor.
2. Board terminal / Thonny REPL showing at least 10 published messages.
3. Subscriber terminal showing messages received and saved.
4. Database output showing at least 10 rows.
5. Optional MQTT raw-message screenshot using `mosquitto_sub`.

## MQTT settings used everywhere

```text
Broker: broker.hivemq.com
Port: 1883
Topic: iot/lab/sensor
```

## Most important warning

For Raspberry Pi Pico, use **Pico W**, not the normal Pico. The normal Pico has no built-in WiFi.
