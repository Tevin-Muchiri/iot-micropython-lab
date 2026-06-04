# ⚡ Quick Reference - Lab Day Cheat Sheet

## 🔌 Wiring
```
DHT22        ESP32
VCC    →     3.3V
DATA   →     GPIO4 (+ 10kΩ resistor to VCC)
GND    →     GND
```

## 💻 Commands to Run

### 1. Flash ESP32 (one time)
```bash
# Erase
esptool.py --port COM3 erase_flash

# Flash (adjust .bin path)
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 path\to\firmware.bin
```

### 2. In Thonny
- Update WiFi credentials in `main.py`
- Save to MicroPython device as `main.py`
- Press F5 to run
- **Keep it running!**

### 3. On PC - Terminal 1
```bash
cd d:\projects\iot-micropython-lab
python subscriber_sqlite.py
```
Let run for 2-3 minutes minimum

### 4. On PC - Terminal 2
```bash
cd d:\projects\iot-micropython-lab
python check_database.py
```

## 📸 Screenshot Timeline
| Time | What | Where |
|------|------|-------|
| 0-10 min | Wired breadboard photo | Camera/phone |
| 25-30 min | Thonny REPL (10+ messages) | Thonny window |
| 35-40 min | Subscriber terminal (10+ messages) | Terminal window |
| 42-45 min | Database query output | Terminal window |
| End | Group photo | Camera/phone |

## 🚨 Quick Troubleshooting
- **WiFi fails?** → Check 2.4GHz, verify credentials
- **Sensor error?** → Check wiring, GPIO4, resistor
- **No MQTT?** → Check internet, try test.mosquitto.org
- **No database?** → Wait longer, check subscriber running

## ✅ Success Signs
- Thonny shows: `Published: {"device":"ESP32-DHT22"...}`
- Subscriber shows: `Saved to database:`
- Database has 10+ rows with timestamps
- All files working together

## 📁 Files
- `main.py` → Upload to ESP32 (Thonny)
- `subscriber_sqlite.py` → Run on PC
- `check_database.py` → Run on PC (verify)

---
**Keep this page open during lab! Good luck! 🎯**
