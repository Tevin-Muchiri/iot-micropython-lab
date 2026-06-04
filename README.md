# 🌡️ ICS 4111: IoT MicroPython Lab Guide
## ESP32 + DHT22 Temperature/Humidity Monitoring with MQTT

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Before Lab Day - Preparation](#before-lab-day---preparation)
3. [Lab Day - Step by Step Guide](#lab-day---step-by-step-guide)
4. [Required Screenshots & Deliverables](#required-screenshots--deliverables)
5. [Troubleshooting](#troubleshooting)
6. [Project Structure](#project-structure)

---

## 🎯 Overview

This lab demonstrates a complete IoT system:
- **ESP32** reads temperature/humidity from **DHT22** sensor
- Data is published to **MQTT broker** via WiFi
- **Python subscriber** on PC receives data and stores in **SQLite database**

**Topic:** `iot/lab/sensor`  
**Broker:** `broker.hivemq.com` (public test broker)

---

## 🔧 Before Lab Day - Preparation

### 1. Install Required Software

Run these commands on your PC:

```bash
# Install esptool for flashing ESP32
pip install esptool

# Install MQTT client library
pip install paho-mqtt

# SQLite is bundled with Python (no installation needed)
```

### 2. Download MicroPython Firmware

1. Visit: https://micropython.org/download/ESP32_GENERIC/
2. Download the latest `.bin` file (v1.24+)
3. Save it to a known location (e.g., `Downloads` folder)

### 3. Install Thonny IDE

1. Download from: https://thonny.org/
2. Install and launch Thonny
3. Go to **Tools** → **Options** → **Interpreter**
4. Select **MicroPython (ESP32)**

---

## 🚀 Lab Day - Step by Step Guide

### PHASE 1: Hardware Setup (10 minutes)

#### Step 1.1: Wire the DHT22 Sensor

**Wiring connections:**

| DHT22 Pin | ESP32 Pin | Wire Color (suggested) |
|-----------|-----------|------------------------|
| VCC (+)   | 3.3V      | Red                    |
| DATA      | GPIO4 (D4)| Yellow                 |
| GND (-)   | GND       | Black                  |

**Important:** Place a **10kΩ pull-up resistor** between VCC and DATA pins.

#### 📸 **DELIVERABLE 1: Take photo of wiring**
- Clear photo showing all connections
- Include resistor placement
- Make sure ESP32 and DHT22 labels are visible

---

### PHASE 2: Flash MicroPython Firmware (15 minutes)

#### Step 2.1: Connect ESP32 to PC

1. Connect ESP32 to PC using USB cable
2. Note the COM port (check Device Manager on Windows)
   - Should appear as: `COM3`, `COM4`, etc.

#### Step 2.2: Erase Flash Memory

Open Command Prompt or PowerShell and run:

```bash
# Replace COM3 with your actual port
esptool.py --port COM3 erase_flash
```

Wait for "Erasing flash... Done" message.

#### Step 2.3: Flash MicroPython Firmware

```bash
# Replace COM3 with your port and adjust the .bin file path
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 C:\Users\YourName\Downloads\ESP32_GENERIC-20240222-v1.24.0.bin
```

**Expected output:**
```
Connecting...
Writing at 0x00001000...
Hash of data verified.
Leaving...
Hard resetting via RTS pin...
```

---

### PHASE 3: Upload Code to ESP32 (10 minutes)

#### Step 3.1: Open Thonny IDE

1. Launch Thonny
2. Configure interpreter:
   - **Tools** → **Options** → **Interpreter**
   - Select: **MicroPython (ESP32)**
   - Port: Your COM port (e.g., COM3)
   - Click **OK**

#### Step 3.2: Configure WiFi Credentials

1. Open `main.py` in Thonny
2. Update these lines:

```python
WIFI_SSID = "YOUR_WIFI_SSID"        # Your WiFi name
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"  # Your WiFi password
```

**💡 Tip:** Make sure you're using a 2.4GHz WiFi network (ESP32 doesn't support 5GHz)

#### Step 3.3: Upload Code to ESP32

1. Copy all contents of `main.py`
2. In Thonny, paste the code
3. Click **File** → **Save as** → **MicroPython device**
4. Save as: `main.py`
5. Click **Save**

#### Step 3.4: Test the Code

1. Click the **Green Play button** in Thonny (or press F5)
2. Watch the **Shell (REPL)** at bottom of Thonny

**Expected output:**
```
==================================================
ESP32 DHT22 MQTT Publisher
==================================================
Connecting to WiFi: YourWiFiName
WiFi connected!
IP Address: 192.168.1.123
DHT22 sensor initialized on GPIO 4
Connected to MQTT broker: broker.hivemq.com
Publishing to topic: iot/lab/sensor

Starting sensor readings...
Press Ctrl+C to stop

Temp: 24.5°C | Humidity: 61.2%
Published: {"device":"ESP32-DHT22","message_no":1,"temperature":24.5,"humidity":61.2,"uptime_seconds":12}
```

#### 📸 **DELIVERABLE 2: Screenshot of REPL output**
- Capture Thonny Shell showing at least **10 published messages**
- Should show temperature, humidity, and message numbers incrementing

---

### PHASE 4: Run PC Subscriber (10 minutes)

**⚠️ Keep ESP32 running in Thonny!** Open a NEW terminal window.

#### Step 4.1: Run the Subscriber Script

Open Command Prompt or PowerShell in your project folder:

```bash
cd d:\projects\iot-micropython-lab
python subscriber_sqlite.py
```

**Expected output:**
```
Database ready: sensor_data.db
Connecting to MQTT broker: broker.hivemq.com
Connected to MQTT broker.
Connection code: Success
Subscribing to topic: iot/lab/sensor
Waiting for ESP32 sensor data...
Press Ctrl + C to stop.

Message received from topic: iot/lab/sensor
Raw payload: {"device":"ESP32-DHT22","message_no":5,"temperature":24.5,"humidity":61.2,"uptime_seconds":25}
Saved to database:
Device: ESP32-DHT22
Message No: 5
Temperature: 24.5
Humidity: 61.2
Received At: 2026-06-04 14:23:45
--------------------------------------------------
```

#### 📸 **DELIVERABLE 3: Screenshot of subscriber terminal**
- Capture terminal showing at least **10 messages received**
- Should show "Saved to database" confirmations

**💡 Let it run for at least 2-3 minutes to collect enough data**

---

### PHASE 5: Verify Database (5 minutes)

#### Step 5.1: Query the Database

Open ANOTHER Command Prompt/PowerShell window:

```bash
cd d:\projects\iot-micropython-lab
python check_database.py
```

**Expected output:**
```
Running SQLite SELECT query:
SELECT * FROM sensor_data;
--------------------------------------------------------------------------------
(1, 'ESP32-DHT22', 1, 24.5, 61.2, 12, 'iot/lab/sensor', '2026-06-04 14:23:32')
(2, 'ESP32-DHT22', 2, 24.6, 61.1, 17, 'iot/lab/sensor', '2026-06-04 14:23:37')
(3, 'ESP32-DHT22', 3, 24.5, 61.3, 22, 'iot/lab/sensor', '2026-06-04 14:23:42')
...
```

#### 📸 **DELIVERABLE 4: Screenshot of database query**
- Should show at least **10-15 rows** with timestamps
- All columns should have valid data

---

### PHASE 6: Testing with mosquitto_sub (Optional but Recommended)

If you have Mosquitto installed, you can verify MQTT messages directly:

```bash
mosquitto_sub -h broker.hivemq.com -t iot/lab/sensor
```

You'll see raw JSON messages in real-time.

#### 📸 **DELIVERABLE 5: Screenshot of mosquitto_sub** (if available)

---

## 📸 Required Screenshots & Deliverables

### Checklist for Tomorrow's Lab:

- [ ] **Photo 1:** Breadboard wiring (clear, well-lit, showing all connections)
- [ ] **Screenshot 1:** Thonny REPL showing 10+ published messages
- [ ] **Screenshot 2:** subscriber_sqlite.py terminal showing 10+ received messages
- [ ] **Screenshot 3:** check_database.py output showing 10+ database rows with timestamps
- [ ] **Screenshot 4:** mosquitto_sub terminal (optional but recommended)
- [ ] **Group Photo:** Team working together during the lab

### 📝 When to Take Each Screenshot:

| Time in Lab | Action | Screenshot/Photo |
|-------------|--------|------------------|
| 0-10 min    | Wire hardware | Photo of breadboard |
| 25-30 min   | ESP32 publishing | Thonny REPL output |
| 35-40 min   | PC receiving data | subscriber terminal |
| 42-45 min   | Database verification | check_database.py output |
| End of lab  | Team together | Group photo |

---

## 🛠️ Troubleshooting

### Problem: ESP32 won't connect to WiFi

**Solutions:**
- Verify WiFi credentials (case-sensitive!)
- Ensure using 2.4GHz network (not 5GHz)
- Move closer to WiFi router
- Check if network requires captive portal login

### Problem: "Sensor read error: OSError"

**Solutions:**
- Check DHT22 wiring (especially DATA pin to GPIO4)
- Verify 10kΩ pull-up resistor is connected
- Try different GPIO pin and update `DHT_PIN` in code
- Sensor needs 2 seconds to stabilize after power-on

### Problem: MQTT connection fails

**Solutions:**
- Check internet connection
- Try alternative broker: `test.mosquitto.org`
- Verify MQTT_BROKER and MQTT_PORT settings match

### Problem: subscriber_sqlite.py not receiving data

**Solutions:**
- Ensure ESP32 is still running and publishing
- Check both devices on same MQTT topic
- Verify PC has internet access
- Check firewall isn't blocking Python

### Problem: Database is empty

**Solutions:**
- Ensure subscriber ran for at least 1-2 minutes
- Check for error messages in subscriber terminal
- Verify `sensor_data.db` file exists in project folder

---

## 📁 Project Structure

```
iot-micropython-lab/
│
├── main.py                    # ESP32 MicroPython code (upload to device)
├── subscriber_sqlite.py       # PC Python script (run on computer)
├── check_database.py          # Database verification script
├── sensor_data.db            # SQLite database (created automatically)
├── README.md                  # This guide
└── .git/                     # Git repository
```

---

## 🎯 Which File to Run When?

### On ESP32 (via Thonny):
1. **Upload:** `main.py` → Save to MicroPython device
2. **Run:** Press F5 or click Green Play button
3. **Keep running** throughout the lab

### On PC (in terminal):
1. **First terminal:** `python subscriber_sqlite.py`
2. **Second terminal:** `python check_database.py` (after collecting data)

---

## 📊 Lab Report Sections (Max 5 Pages)

1. **Introduction** (0.5 page)
   - Lab objectives and overview

2. **System Architecture** (1 page)
   - Block diagram showing ESP32 → MQTT → PC → Database flow
   - Wiring diagram/photo

3. **Implementation** (1.5 pages)
   - Key code sections explained
   - Hardware configuration
   - Software setup steps

4. **Results** (1.5 pages)
   - All required screenshots
   - Data analysis (sample readings)
   - Success confirmation

5. **Challenges & Solutions** (0.5 page)
   - Problems encountered
   - How you resolved them
   - Lessons learned

6. **Group Collaboration Evidence** (0.5 page)
   - Group photo during lab
   - Brief description of each member's role

---

## 🎓 Final Submission Checklist

- [ ] All source code files in GitHub repository
- [ ] Repository link shared on e-learning
- [ ] Comprehensive PDF report with all screenshots
- [ ] Group photo included
- [ ] Team member roles documented
- [ ] Lab report covers challenges and solutions
- [ ] Submitted before deadline by ONE team member

---

## 📞 Need Help?

**Instructor:** sitotia@strathmore.edu  
**Lab Technologist:** jntonjira@strathmore.edu

**Makerspace Lab Access:** Schedule [here](https://link-to-schedule) and forward invite to both contacts above.

---

## ⭐ Success Criteria

Your lab is successful when:
- ✅ ESP32 publishes JSON data to MQTT broker every 5 seconds
- ✅ PC subscriber receives and displays messages in real-time
- ✅ SQLite database contains 10+ timestamped records
- ✅ All screenshots clearly show working system
- ✅ Group collaboration documented

---

**Good luck with your lab! 🚀**

*Last updated: June 2026*