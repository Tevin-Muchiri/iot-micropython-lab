# Raspberry Pi Pico W MicroPython Quick Reference

## Important board note

This MQTT version needs **Raspberry Pi Pico W**. A normal Raspberry Pi Pico has no built-in WiFi, so it cannot publish MQTT unless an external WiFi module is added.

## Wiring: DHT22 to Pico W

| DHT22 Pin | Pico W Pin |
|---|---|
| VCC | 3V3 OUT / physical pin 36 |
| DATA | GP4 / physical pin 6 |
| GND | GND / physical pin 3, 8, 13, 18, 23, 28, 33, or 38 |

Add a 10k ohm pull-up resistor between VCC and DATA.

## MicroPython setup

1. Install Pico W MicroPython firmware.
2. In Thonny, select MicroPython (Raspberry Pi Pico).
3. Open `main.py` from this folder.
4. Change WiFi name and password.
5. Save to Pico W as `main.py`.
6. Press F5.

## If `umqtt.simple` is missing

In Thonny, install `micropython-umqtt.simple`, or upload the `umqtt/simple.py` module to the Pico W.

## Success sign

Thonny should show JSON like:

```text
{"device":"PicoW-DHT22","message_no":1,"temperature":24.5,"humidity":61.2,"uptime_seconds":12}
```

Keep the PC subscriber running in another terminal.
