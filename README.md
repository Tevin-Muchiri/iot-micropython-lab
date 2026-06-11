# ICS 4111: IoT MicroPython Lab Documentation
## ESP32 + DHT22 Temperature/Humidity Monitoring with MQTT

---

## Team Members

- **Krishna Madhaparia** - 166980
- **Philip Tait** - 166384
- **Parneet Kaur** - 166985
- **Dhruvin Bhudia** - 169646
- **Tevin Ngiru** - 166289
- **Eeshan Vaghjiani** - 166981

---

## Hardware Setup

### Complete Circuit Assembly

![Full Circuit](Pictures/Full_ESP32_DHT22_Circuit.jpeg)

### ESP32 Connections

![ESP32 Connections](Pictures/ESP32_Connections.jpeg)

### Wiring Configuration

The DHT22 sensor was connected to the ESP32 as follows:

| DHT22 Pin | ESP32 Pin | Wire Color |
|-----------|-----------|------------|
| VCC (+)   | 3.3V      | Red        |
| DATA      | GPIO4 (D4)| Yellow     |
| GND (-)   | GND       | Black      |

A 10kohm pull-up resistor was placed between VCC and DATA pins.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Software Installation](#software-installation)
3. [Lab Execution](#lab-execution)
   - [Phase 1: ESP32 Firmware Setup](#phase-1-esp32-firmware-setup)
   - [Phase 2: MicroPython Configuration](#phase-2-micropython-configuration)
   - [Phase 3: Sensor Data Collection](#phase-3-sensor-data-collection)
   - [Phase 4: MQTT Publishing](#phase-4-mqtt-publishing)
   - [Phase 5: Data Subscription](#phase-5-data-subscription)
   - [Phase 6: Database Verification](#phase-6-database-verification)
4. [Complete Sensor Data](#complete-sensor-data)
5. [File Reference](#file-reference)
6. [Project Structure](#project-structure)

---

## Project Overview

This lab implemented a complete IoT system where:
- An ESP32 microcontroller read temperature and humidity data from a DHT22 sensor
- The sensor data was published to an MQTT broker via WiFi
- A Python subscriber on a PC received the data and stored it in a SQLite database

**MQTT Configuration:**
- **Topic:** `iot/lab/sensor`
- **Broker:** `broker.hivemq.com` (public test broker)
- **Device ID:** `ESP32-DHT22`

---

## Software Installation

The following software packages were installed on the development PC:

```bash
# ESP32 flashing tool
pip install esptool

# MQTT client library for Python
pip install paho-mqtt

# Image processing (for documentation)
pip install pillow pytesseract

# Data analysis
pip install numpy
```

**MicroPython Firmware:**
- Downloaded from: https://micropython.org/download/ESP32_GENERIC/

- Version: v1.28.0 (2026-04-06)
- File: `ESP32_GENERIC-*.bin`

**Thonny IDE:**
- Downloaded from: https://thonny.org/
- Configured for MicroPython (ESP32) interpreter

---

## Lab Execution

### Phase 1: ESP32 Firmware Setup

#### 1.1 Flash Memory Erase

The ESP32's flash memory was erased to prepare for MicroPython installation.

**Command executed:**
```bash
python -m esptool --port COM17 erase_flash
```

**Output:**

![Flash Erase Output](Pictures/esp32_flash_02_erase_flash.png)

The flash memory was successfully erased in 2.4 seconds.

---

#### 1.2 MicroPython Firmware Installation

MicroPython v1.28.0 firmware was flashed to the ESP32.

**Command executed:**
```bash
python -m esptool --chip esp32 --port COM17 write-flash -z 0x1000 esp32.bin
```

**Output:**

![Firmware Flashing](Pictures/esp32_flash_01_flashing_firmware.png)

The firmware (1,760,192 bytes compressed to 1,152,806 bytes) was successfully written to the ESP32.

---

#### 1.3 Troubleshooting Encountered


**Issue 1: Connection Error**

![Connection Error](Pictures/esp32_flash_03_connection_error.png)

The ESP32 failed to enter download mode (boot mode 0x13 detected instead of expected mode).

**Resolution:** Pressed and held the BOOT button on the ESP32 while connecting, then released after connection established.

---

**Issue 2: File Not Found**

![File Not Found](Pictures/esp32_flash_04_file_not_found.png)

The esp32.bin file could not be located in the current directory.

**Resolution:** Navigated to the directory containing the firmware file before executing the flash command.

---

### Phase 2: MicroPython Configuration

#### 2.1 Boot Sequence Verification

After successful firmware installation, the ESP32 was connected via Thonny IDE to verify the MicroPython environment.

**Tool used:** Thonny IDE

**Output:**

![MicroPython Boot](Pictures/micropython_repl_01_boot_sequence.png)

MicroPython v1.28.0 successfully booted on the Generic ESP32 module.

---

#### 2.2 WiFi Connection

The ESP32 was configured to connect to the local WiFi network.

**Code executed:** `main.py` (WiFi initialization section)


```python
import network

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("K8597", "Q0001111")

while not wifi.isconnected():
    print("Connecting WiFi...")
    time.sleep(1)

print("WiFi Connected")
print(wifi.ifconfig())
```

**Output:**

![WiFi Connected](Pictures/micropython_repl_02_wifi_connected.png)

The ESP32 successfully connected to the WiFi network with IP address: `192.168.137.64`

---

#### 2.3 MQTT Broker Connection

The MQTT client was initialized and connected to the HiveMQ public broker.

**Code executed:** `main.py` (MQTT initialization section)

```python
from umqtt.simple import MQTTClient

client = MQTTClient("esp32_test", "broker.hivemq.com")
client.connect()
print("MQTT Connected!")
```

**Output:**

![MQTT Connected](Pictures/micropython_repl_03_mqtt_connected.png)

The ESP32 successfully established a connection to `broker.hivemq.com`.

---

### Phase 3: Sensor Data Collection

#### 3.1 DHT22 Sensor Readings

The DHT22 sensor began collecting temperature and humidity measurements.

**Code executed:** `main.py` (Sensor reading loop)


```python
import dht
from machine import Pin

sensor = dht.DHT22(Pin(4))

while True:
    sensor.measure()
    temp = sensor.temperature()
    humidity = sensor.humidity()
    print(f"Temperature: {temp} C")
    print(f"Humidity: {humidity} %")
    time.sleep(3)
```

**Output - Sample 1:**

![Sensor Output 1](Pictures/sensor_output_01_temperature_humidity.png)

**Output - Sample 2:**

![Sensor Output 2](Pictures/sensor_output_02_temperature_humidity.png)

**Output - Sample 3:**

![Sensor Output 3](Pictures/sensor_output_03_temperature_humidity.png)

**Output - Sample 4:**

![Sensor Output 4](Pictures/sensor_output_04_temperature_humidity.png)

The DHT22 sensor successfully measured temperature readings between 26.4-28.5 degrees Celsius and humidity readings between 58-83%.

---

### Phase 4: MQTT Publishing

#### 4.1 Publisher Implementation

The complete MQTT publisher code was implemented in Thonny IDE, combining WiFi connection, sensor reading, and MQTT publishing.

**File:** `main.py`

**Tool:** Thonny IDE

**Output:**

![MQTT Publisher Code](Pictures/mqtt_publisher_01_thonny_code_shell.png)

The Thonny IDE showed the complete publisher code with the REPL (Read-Eval-Print Loop) displaying connection status.

---

#### 4.2 Data Publishing Results

The ESP32 began publishing sensor data to the MQTT broker in JSON format.

**Published message format:**
```json
{
  "message_no": 10,
  "temperature": 26.9,
  "humidity": 58.7,
  "uptime_seconds": 41,
  "device": "ESP32-DHT22"
}
```

**Output:**

![MQTT Publishing Data](Pictures/mqtt_publisher_02_publishing_data.png)

The system successfully published messages every 3 seconds with:
- Sequential message numbers (10-14 shown)
- Temperature readings around 26.9 degrees Celsius
- Humidity readings between 58.5-58.7%
- Device uptime tracking
- Device identifier: "ESP32-DHT22"

Each message was confirmed with "Published successfully!" status.

---

### Phase 5: Data Subscription

#### 5.1 Python MQTT Subscriber

A Python subscriber script was implemented to receive MQTT messages and store them in a SQLite database.

**File:** `subscriber_sqlite.py`

**Command executed:**
```bash
python subscriber_sqlite.py
```

**Code implementation:**
```python
import paho.mqtt.client as mqtt
import sqlite3
import json
from datetime import datetime

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    
    # Insert into database
    cursor.execute("""
        INSERT INTO sensor_data 
        (device, message_no, temperature, humidity, uptime_seconds, mqtt_topic, received_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (payload['device'], payload.get('message_no'), payload['temperature'],
          payload['humidity'], payload.get('uptime_seconds'), msg.topic, datetime.now()))
    
    conn.commit()
```


**Output - Message Reception:**

![Python Subscriber - Message Received](Pictures/mqtt_subscriber_python_01_message_received.png)

The subscriber successfully:
- Connected to MQTT broker `broker.hivemq.com`
- Subscribed to topic `iot/lab/sensor`
- Received message #6 with temperature 26.9C and humidity 56.6%
- Saved the data to database with timestamp `2026-06-08 15:00:12`

---

**Output - Database Storage:**

![Python Subscriber - Saving to Database](Pictures/mqtt_subscriber_python_02_saving_to_db.png)

The subscriber established:
- Database connection to `sensor_data.db`
- MQTT broker connection with "Success" status code
- Active subscription to `iot/lab/sensor` topic
- Real-time data storage capability

The first test message stored contained:
- Device: ESP32-DHT22
- Temperature: 15.37C
- Humidity: 39.59%
- Additional pressure data: 1008.15
- Timestamp: 2026-06-08 14:59:36

---

#### 5.2 Mosquitto CLI Subscriber (Verification)

As an additional verification method, the Mosquitto command-line subscriber was used to monitor MQTT messages directly.

**Command executed:**
```bash
mosquitto_sub -h broker.hivemq.com -t "iot/lab/sensor" -v
```

**Output - Terminal View:**

![Mosquitto Subscriber Terminal](Pictures/mqtt_subscriber_mosquitto_01_terminal_output.jpeg)

The Mosquitto subscriber received messages 1-8 showing:
- Sequential message numbering
- Temperature: 26.9C (message 1 at 60.0%, message 2 at 26.800002C)
- Uptime progression: 12, 15, 18, 22, 25, 28, 32, 35 seconds
- Device identifier: "ESP32-DHT22"
- Humidity values: 58.5-60.0%


---

**Output - Extended Terminal Session:**

![Mosquitto Subscriber Full Terminal](Pictures/mqtt_subscriber_mosquitto_02_full_terminal.jpeg)

The extended monitoring session captured:
- Multiple subscription sessions showing system reliability
- Messages 1-31 received continuously
- Initial test message with pressure data (1008.15)
- Consistent data format across all messages
- Temperature stability around 26.9C
- Humidity range: 58.5-59.3%
- Uptime tracking from 12 to 111 seconds

This verified that the MQTT publishing system was operating reliably and consistently.

---

### Phase 6: Database Verification

#### 6.1 Initial Database Query

The database was queried to verify data storage.

**File:** `check_database.py`

**Command executed:**
```bash
python check_database.py
```

**Code implementation:**
```python
import sqlite3

conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

print("Running SQLite SELECT query:")
print("SELECT * FROM sensor_data;")
print("-" * 80)

cursor.execute("SELECT * FROM sensor_data")
rows = cursor.fetchall()

for row in rows:
    print(row)
```

**Output:**

![Database Query - Latest Entries](Pictures/database_records_01_latest_entries.png)

The query returned the 3 most recent database records:
- Record 3: Message #2, Temp: 26.9C, Humidity: 56.4%, Time: 2026-06-08 14:59:58
- Record 2: Message #1, Temp: 26.9C, Humidity: 56.3%, Time: 2026-06-08 14:59:55
- Record 1: Initial test, Temp: 15.37C, Humidity: 39.59%, Time: 2026-06-08 14:59:36

---

#### 6.2 Extended Database Records

**Output:**

![Database Query - Sensor Data](Pictures/database_records_02_sensor_data.png)

The database contained 6 records (IDs 3-8) showing:
- Sequential message progression (messages 2-7)
- Consistent device identification: "ESP32-DHT22"
- Temperature stability: 26.9C across all readings
- Humidity variation: 56.4-56.6%
- Uptime progression: 15, 19, 22, 25, 29, 32 seconds
- MQTT topic: "iot/lab/sensor"
- Proper timestamp recording (2026-06-08 14:59:58 to 15:00:14)

---

#### 6.3 Complete Database Dump

**Output:**

![Database Query - Full Table](Pictures/database_records_03_full_table_query.png)

The complete SELECT query displayed all 8 records with full column data:

**Database Schema:**
1. `id` - Auto-increment primary key
2. `device` - Device identifier (ESP32-DHT22)
3. `message_no` - Sequential message counter
4. `temperature` - Temperature in Celsius
5. `humidity` - Relative humidity percentage
6. `uptime_seconds` - Device uptime
7. `mqtt_topic` - MQTT topic path (iot/lab/sensor)
8. `received_at` - Timestamp of data reception

All records showed consistent data structure and proper foreign key relationships.

---

## Complete Sensor Data

### Database Export

The complete sensor data was exported from the SQLite database using the export script.

**File:** `export_db_data.py`

**Command executed:**
```bash
python "export db data.py"
```

This generated two output files:
- `sensor_data_output.csv` - CSV format for spreadsheet analysis
- `sensor_data_table.md` - Markdown table format for documentation


---

### Full Data Table
| id | device | message_no | temperature | humidity | uptime_seconds | mqtt_topic | received_at |
|---|---|---|---|---|---|---|---|
| 1 | ESP32-DHT22 |  | 15.37 | 39.59 |  | iot/lab/sensor | 2026-06-08 14:59:36 |
| 2 | ESP32-DHT22 | 1 | 26.9 | 56.3 | 12 | iot/lab/sensor | 2026-06-08 14:59:55 |
| 3 | ESP32-DHT22 | 2 | 26.9 | 56.4 | 15 | iot/lab/sensor | 2026-06-08 14:59:58 |
<details>
<summary><b>Click to expand complete sensor data table (43 records)</b></summary>

| id | device | message_no | temperature | humidity | uptime_seconds | mqtt_topic | received_at |
|---|---|---|---|---|---|---|---|
| 1 | ESP32-DHT22 |  | 15.37 | 39.59 |  | iot/lab/sensor | 2026-06-08 14:59:36 |
| 2 | ESP32-DHT22 | 1 | 26.9 | 56.3 | 12 | iot/lab/sensor | 2026-06-08 14:59:55 |
| 3 | ESP32-DHT22 | 2 | 26.9 | 56.4 | 15 | iot/lab/sensor | 2026-06-08 14:59:58 |
| 4 | ESP32-DHT22 | 3 | 26.9 | 56.5 | 19 | iot/lab/sensor | 2026-06-08 15:00:03 |
| 5 | ESP32-DHT22 | 4 | 26.9 | 56.600004 | 22 | iot/lab/sensor | 2026-06-08 15:00:06 |
| 6 | ESP32-DHT22 | 5 | 26.9 | 56.600004 | 25 | iot/lab/sensor | 2026-06-08 15:00:08 |
| 7 | ESP32-DHT22 | 6 | 26.9 | 56.600004 | 29 | iot/lab/sensor | 2026-06-08 15:00:12 |
| 8 | ESP32-DHT22 | 7 | 26.9 | 56.600004 | 32 | iot/lab/sensor | 2026-06-08 15:00:14 |
| 9 | ESP32-DHT22 | 8 | 26.9 | 56.5 | 35 | iot/lab/sensor | 2026-06-08 15:00:18 |
| 10 | ESP32-DHT22 | 9 | 26.9 | 56.4 | 39 | iot/lab/sensor | 2026-06-08 15:00:22 |
| 11 | ESP32-DHT22 | 10 | 26.9 | 56.4 | 42 | iot/lab/sensor | 2026-06-08 15:00:24 |
| 12 | ESP32-DHT22 | 11 | 26.9 | 56.600004 | 45 | iot/lab/sensor | 2026-06-08 15:00:28 |
| 13 | ESP32-DHT22 | 12 | 26.9 | 56.5 | 48 | iot/lab/sensor | 2026-06-08 15:00:32 |
| 14 | ESP32-DHT22 | 13 | 26.9 | 56.5 | 52 | iot/lab/sensor | 2026-06-08 15:00:35 |
| 15 | ESP32-DHT22 | 14 | 26.9 | 56.4 | 55 | iot/lab/sensor | 2026-06-08 15:00:39 |
| 16 | ESP32-DHT22 | 15 | 26.9 | 56.4 | 58 | iot/lab/sensor | 2026-06-08 15:00:42 |
| 17 | ESP32-DHT22 | 16 | 26.9 | 56.3 | 62 | iot/lab/sensor | 2026-06-08 15:00:45 |
| 18 | ESP32-DHT22 | 17 | 26.9 | 56.2 | 65 | iot/lab/sensor | 2026-06-08 15:00:49 |
| 19 | ESP32-DHT22 | 18 | 26.9 | 56.2 | 68 | iot/lab/sensor | 2026-06-08 15:00:51 |
| 20 | ESP32-DHT22 | 19 | 26.9 | 56.2 | 71 | iot/lab/sensor | 2026-06-08 15:00:55 |
| 21 | ESP32-DHT22 | 20 | 27.0 | 56.2 | 75 | iot/lab/sensor | 2026-06-08 15:00:59 |
| 22 | ESP32-DHT22 | 21 | 26.9 | 56.3 | 78 | iot/lab/sensor | 2026-06-08 15:01:01 |
| 23 | ESP32-DHT22 | 22 | 26.9 | 56.4 | 81 | iot/lab/sensor | 2026-06-08 15:01:05 |
| 24 | ESP32-DHT22 | 23 | 26.9 | 56.3 | 85 | iot/lab/sensor | 2026-06-08 15:01:09 |
| 25 | ESP32-DHT22 | 24 | 27.0 | 56.4 | 88 | iot/lab/sensor | 2026-06-08 15:01:11 |
| 26 | ESP32-DHT22 | 25 | 26.9 | 56.4 | 91 | iot/lab/sensor | 2026-06-08 15:01:15 |
| 27 | ESP32-DHT22 | 26 | 27.0 | 56.4 | 94 | iot/lab/sensor | 2026-06-08 15:01:19 |
| 28 | ESP32-DHT22 | 27 | 26.9 | 56.5 | 98 | iot/lab/sensor | 2026-06-08 15:01:21 |
| 29 | ESP32-DHT22 | 28 | 27.0 | 56.5 | 101 | iot/lab/sensor | 2026-06-08 15:01:25 |
| 30 | ESP32-DHT22 | 29 | 27.0 | 56.5 | 104 | iot/lab/sensor | 2026-06-08 15:01:27 |
| 31 | ESP32-DHT22 | 30 | 27.0 | 56.600004 | 108 | iot/lab/sensor | 2026-06-08 15:01:31 |
| 32 | ESP32-DHT22 | 31 | 27.0 | 56.5 | 111 | iot/lab/sensor | 2026-06-08 15:01:35 |
| 33 | ESP32-DHT22 | 32 | 27.0 | 56.4 | 114 | iot/lab/sensor | 2026-06-08 15:01:37 |
| 34 | ESP32-DHT22 | 33 | 27.0 | 56.4 | 117 | iot/lab/sensor | 2026-06-08 15:01:41 |
| 35 | ESP32-DHT22 | 34 | 27.0 | 56.3 | 121 | iot/lab/sensor | 2026-06-08 15:01:45 |
| 36 | ESP32-DHT22 | 35 | 27.0 | 56.3 | 124 | iot/lab/sensor | 2026-06-08 15:01:47 |
| 37 | ESP32-DHT22 | 36 | 27.0 | 56.4 | 127 | iot/lab/sensor | 2026-06-08 15:01:51 |
| 38 | ESP32-DHT22 | 37 | 27.0 | 56.4 | 131 | iot/lab/sensor | 2026-06-08 15:01:55 |
| 39 | ESP32-DHT22 | 38 | 27.0 | 56.4 | 134 | iot/lab/sensor | 2026-06-08 15:01:57 |
| 40 | ESP32-DHT22 | 39 | 27.0 | 56.4 | 137 | iot/lab/sensor | 2026-06-08 15:02:01 |
| 41 | ESP32-DHT22 | 40 | 27.0 | 56.4 | 141 | iot/lab/sensor | 2026-06-08 15:02:03 |
| 42 | ESP32-DHT22 | 41 | 27.0 | 56.4 | 144 | iot/lab/sensor | 2026-06-08 15:02:07 |
| 43 | ESP32-DHT22 | 42 | 27.0 | 56.5 | 147 | iot/lab/sensor | 2026-06-08 15:02:11 |

</details>

---

### Data Analysis Summary

**Total Records Collected:** 43 sensor readings

**Time Period:** 
- Start: 2026-06-08 14:59:36
- End: 2026-06-08 15:02:11
- Duration: Approximately 2 minutes 35 seconds

**Temperature Statistics:**
- Average: 26.95C
- Range: 15.37C - 27.0C (excluding initial test reading: 26.9C - 27.0C)
- Stability: Very stable, 0.1C variation during normal operation

**Humidity Statistics:**
- Average: 56.4%
- Range: 39.59% - 60.0% (excluding initial test reading: 56.2% - 60.0%)
- Variation: ~4% range during normal operation

**System Performance:**
- Message Delivery Rate: 100% (all messages received and stored)
- Average Message Interval: ~3 seconds
- Database Integrity: All records properly timestamped
- MQTT Reliability: No message loss detected

---

## File Reference

### Complete File-to-Output Mapping

| File/Command | Purpose | Output |
|-------------|---------|--------|
| `esptool --port COM17 erase_flash` | Erase ESP32 flash memory | esp32_flash_02_erase_flash.png |
| `esptool --chip esp32 --port COM17 write_flash` | Flash MicroPython firmware | esp32_flash_01_flashing_firmware.png |
| Thonny IDE connection | Verify MicroPython boot | micropython_repl_01_boot_sequence.png |
| `main.py` - WiFi section | Connect to WiFi network | micropython_repl_02_wifi_connected.png |
| `main.py` - MQTT section | Connect to MQTT broker | micropython_repl_03_mqtt_connected.png |
| `main.py` - Sensor loop | DHT22 sensor readings | sensor_output_01-04_temperature_humidity.png |
| `main.py` in Thonny | Complete publisher code | mqtt_publisher_01_thonny_code_shell.png |
| `main.py` - Publishing | MQTT message transmission | mqtt_publisher_02_publishing_data.png |
| `subscriber_sqlite.py` | Receive and store MQTT data | mqtt_subscriber_python_01-02.png |
| `mosquitto_sub -h broker.hivemq.com` | Monitor MQTT messages | mqtt_subscriber_mosquitto_01-02.jpeg |
| `check_database.py` | Query SQLite database | database_records_01-03.png |
| `export db data.py` | Export data to CSV/Markdown | sensor_data_output.csv, sensor_data_table.md |

---

## Project Structure

```
iot-micropython-lab/
|
|-- Pictures/                           # All lab screenshots and circuit photos
|   |-- Full_ESP32_DHT22_Circuit.jpeg
|   |-- ESP32_Connections.jpeg
|   |-- esp32_flash_01_flashing_firmware.png
|   |-- esp32_flash_02_erase_flash.png
|   |-- esp32_flash_03_connection_error.png
|   |-- esp32_flash_04_file_not_found.png
|   |-- micropython_repl_01_boot_sequence.png
|   |-- micropython_repl_02_wifi_connected.png
|   |-- micropython_repl_03_mqtt_connected.png
|   |-- sensor_output_01_temperature_humidity.png
|   |-- sensor_output_02_temperature_humidity.png
|   |-- sensor_output_03_temperature_humidity.png
|   |-- sensor_output_04_temperature_humidity.png
|   |-- mqtt_publisher_01_thonny_code_shell.png
|   |-- mqtt_publisher_02_publishing_data.png
|   |-- mqtt_subscriber_python_01_message_received.png
|   |-- mqtt_subscriber_python_02_saving_to_db.png
|   |-- mqtt_subscriber_mosquitto_01_terminal_output.jpeg
|   |-- mqtt_subscriber_mosquitto_02_full_terminal.jpeg
|   |-- database_records_01_latest_entries.png
|   |-- database_records_02_sensor_data.png
|   +-- database_records_03_full_table_query.png
|
|-- main.py                             # ESP32 MicroPython publisher code
|-- subscriber_sqlite.py                # PC Python MQTT subscriber
|-- check_database.py                   # Database verification script
|-- export db data.py                   # Data export utility
|-- sensor_data.db                      # SQLite database (auto-generated)
|-- sensor_data_output.csv              # Exported CSV data
|-- sensor_data_table.md                # Exported Markdown table
|-- README.md                           # This documentation
+-- .git/                               # Git repository
```

---

## System Architecture

**Data Flow:**

```
DHT22 Sensor --> ESP32 (MicroPython)
                    |
                    | WiFi
                    v
            MQTT Broker (broker.hivemq.com)
                    |
                    | Topic: iot/lab/sensor
                    v
        +------------------------+
        |                        |
Python Subscriber        Mosquitto CLI
(subscriber_sqlite.py)   (monitoring)
        |
        v
SQLite Database
(sensor_data.db)
        |
        v
Data Analysis & Export
(CSV, Markdown)
```

---

## Key Technologies Used

- **Hardware:** ESP32 microcontroller, DHT22 temperature/humidity sensor
- **Firmware:** MicroPython v1.28.0
- **Communication:** WiFi (802.11 b/g/n), MQTT protocol
- **Languages:** Python 3.x, MicroPython
- **Libraries:** 
  - `umqtt.simple` (MicroPython MQTT client)
  - `paho-mqtt` (Python MQTT client)
  - `sqlite3` (Python database)
  - `dht` (MicroPython sensor driver)
- **Tools:** Thonny IDE, esptool, mosquitto-clients
- **Database:** SQLite 3

---

## Conclusions

This lab successfully demonstrated:

1. **Hardware Integration:** The ESP32 successfully interfaced with the DHT22 sensor and read accurate temperature and humidity data.

2. **Wireless Communication:** The ESP32 connected reliably to WiFi and maintained a stable connection to the MQTT broker.

3. **Data Publishing:** Sensor data was published consistently every 3 seconds in JSON format with no message loss.

4. **Data Persistence:** All 43 messages were successfully received and stored in the SQLite database with proper timestamps.

5. **System Reliability:** The system operated continuously for over 2.5 minutes without errors or disconnections.

6. **Data Verification:** Multiple verification methods (Python subscriber, Mosquitto CLI, database queries) confirmed data integrity.

The project demonstrated a complete IoT pipeline from sensor data acquisition through wireless transmission to persistent storage and analysis.

---
