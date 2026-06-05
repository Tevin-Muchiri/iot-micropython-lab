# ESP8266 / NodeMCU Quick Reference

## Wiring: DHT22 to ESP8266 NodeMCU

| DHT22 Pin | ESP8266 / NodeMCU Pin |
|---|---|
| VCC | 3V3 |
| DATA | D2 / GPIO4 |
| GND | GND |

Add a 10k ohm pull-up resistor between VCC and DATA.

## MicroPython setup

1. Flash ESP8266 MicroPython firmware.
2. In Thonny, select MicroPython (ESP8266).
3. Open `main.py` from this folder.
4. Change WiFi name and password.
5. Save to device as `main.py`.
6. Press F5.

## Flash command example

```bash
esptool.py --port COM3 erase_flash
esptool.py --port COM3 --baud 460800 write_flash --flash_size=detect 0 ESP8266_GENERIC.bin
```

## Success sign

Thonny should show JSON like:

```text
{"device":"ESP8266-DHT22","message_no":1,"temperature":24.5,"humidity":61.2,"uptime_seconds":12}
```

Keep the PC subscriber running in another terminal.
