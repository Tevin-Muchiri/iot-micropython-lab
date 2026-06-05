# ==============================================================================
# ESP8266 MicroPython - DHT22 Sensor with MQTT Publisher
# ICS 4111: Embedded Systems & IoT Lab
#
# Upload this file to the ESP8266 / NodeMCU using Thonny as main.py
# ==============================================================================

import network
import time
from machine import Pin, unique_id
import dht
import ujson
from ubinascii import hexlify
from umqtt.simple import MQTTClient

# =========================
# WiFi Configuration
# =========================
WIFI_SSID = "YOUR_WIFI_NAME"          # Replace with your WiFi name
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"  # Replace with your WiFi password

# =========================
# MQTT Configuration
# =========================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab/sensor"

# Unique client ID based on ESP8266 device ID
MQTT_CLIENT_ID = b"esp8266-dht22-" + hexlify(unique_id())

# =========================
# Sensor Configuration
# =========================
# NodeMCU label D2 is GPIO4. If your board labels pins as GPIO, use GPIO4 directly.
DHT_PIN = 4

# =========================
# Publishing Configuration
# =========================
PUBLISH_INTERVAL = 3  # seconds

# =========================
# Global Variables
# =========================
message_counter = 0
start_time = time.ticks_ms()


def connect_wifi():
    """Connect ESP8266 to WiFi network with timeout and status feedback."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi:", WIFI_SSID)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        timeout = 30
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            time.sleep(1)
            timeout -= 1
        print()

    if wlan.isconnected():
        print("WiFi connected successfully!")
        print("Network details:", wlan.ifconfig())
        print("IP Address:", wlan.ifconfig()[0])
        return True

    print("WiFi connection failed. Check credentials and ensure 2.4GHz WiFi.")
    return False


def connect_mqtt():
    """Connect ESP8266 to MQTT broker."""
    print("\nConnecting to MQTT broker:", MQTT_BROKER)
    print("Client ID:", MQTT_CLIENT_ID.decode())

    client = MQTTClient(
        client_id=MQTT_CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        keepalive=60
    )
    client.connect()
    print("MQTT connected successfully!")
    print("Publishing to topic:", MQTT_TOPIC)
    return client


def read_sensor(sensor):
    """Read DHT22 temperature and humidity."""
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        return temperature, humidity
    except OSError as e:
        print("Sensor read error:", e)
        return None, None


def create_payload(temperature, humidity):
    """Create JSON payload compatible with subscriber_sqlite.py."""
    global message_counter

    message_counter += 1
    uptime_seconds = time.ticks_diff(time.ticks_ms(), start_time) // 1000

    payload = {
        "device": "ESP8266-DHT22",
        "message_no": message_counter,
        "temperature": temperature,
        "humidity": humidity,
        "uptime_seconds": uptime_seconds
    }
    return ujson.dumps(payload)


def publish_data(client, temperature, humidity):
    """Publish sensor data to MQTT broker."""
    try:
        json_payload = create_payload(temperature, humidity)
        print("=" * 50)
        print("Message #:", message_counter)
        print("Temperature:", temperature, "C")
        print("Humidity:", humidity, "%")
        print("JSON:", json_payload)
        client.publish(MQTT_TOPIC, json_payload)
        print("Published successfully!")
        return True
    except Exception as e:
        print("MQTT publish error:", e)
        return False


def main():
    print("=" * 60)
    print("ESP8266 DHT22 MQTT Publisher")
    print("ICS 4111: Embedded Systems & IoT Lab")
    print("=" * 60)

    if not connect_wifi():
        print("Cannot proceed without WiFi.")
        return

    try:
        sensor = dht.DHT22(Pin(DHT_PIN))
        print("DHT22 sensor initialized on GPIO", DHT_PIN)
        time.sleep(2)
    except Exception as e:
        print("Sensor initialization error:", e)
        return

    try:
        client = connect_mqtt()
    except Exception as e:
        print("MQTT connection error:", e)
        return

    print("\nStarting sensor readings. Press Ctrl+C to stop.\n")

    try:
        while True:
            temperature, humidity = read_sensor(sensor)
            if temperature is not None and humidity is not None:
                success = publish_data(client, temperature, humidity)
                if not success:
                    try:
                        client.disconnect()
                    except Exception:
                        pass
                    time.sleep(2)
                    client = connect_mqtt()
            else:
                print("Failed to read sensor, skipping this cycle.")
            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        try:
            client.disconnect()
            print("Disconnected from MQTT broker.")
        except Exception:
            pass


if __name__ == "__main__":
    main()
