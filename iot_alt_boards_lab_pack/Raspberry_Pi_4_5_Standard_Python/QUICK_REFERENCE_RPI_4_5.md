# Raspberry Pi 4 / 5 Standard Python Quick Reference

## Wiring: DHT22 to Raspberry Pi 4/5

| DHT22 Pin | Raspberry Pi Pin |
|---|---|
| VCC | 3.3V physical pin 1 or 17 |
| DATA | GPIO4 / physical pin 7 |
| GND | GND physical pin 6, 9, 14, 20, 25, 30, 34, or 39 |

Add a 10k ohm pull-up resistor between VCC and DATA.

## Software setup

Raspberry Pi 4/5 already runs normal Python. Do not use Thonny MicroPython for this board.

Recommended terminal setup:

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip python3-libgpiod
python3 -m venv ~/iotlab-venv
source ~/iotlab-venv/bin/activate
pip install paho-mqtt adafruit-circuitpython-dht
```

## Run the publisher

```bash
source ~/iotlab-venv/bin/activate
python3 raspberry_pi_publisher.py
```

## Success sign

Terminal should show JSON like:

```text
{"device":"RaspberryPi-DHT22","message_no":1,"temperature":24.5,"humidity":61.2,"uptime_seconds":12}
```

Keep the PC subscriber running in another terminal. If the Raspberry Pi is also your PC, run the subscriber in a second terminal tab.
