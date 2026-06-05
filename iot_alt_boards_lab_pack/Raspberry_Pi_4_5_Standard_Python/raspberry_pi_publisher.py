# ==============================================================================
# Raspberry Pi 4 / 5 - Standard Python DHT22 Sensor with MQTT Publisher
# ICS 4111: Embedded Systems & IoT Lab
#
# Run on Raspberry Pi OS using: python3 raspberry_pi_publisher.py
# ==============================================================================

import json
import time
import uuid

import adafruit_dht
import board
import paho.mqtt.client as mqtt

# =========================
# MQTT Configuration
# =========================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab/sensor"

# Unique client ID based on Raspberry Pi network hardware ID
MQTT_CLIENT_ID = "raspberrypi-dht22-{:x}".format(uuid.getnode())

# =========================
# Sensor Configuration
# =========================
# board.D4 = GPIO4 = physical pin 7 on Raspberry Pi 4/5 header.
DHT_PIN = board.D4

# =========================
# Publishing Configuration
# =========================
PUBLISH_INTERVAL = 3  # seconds

# =========================
# Global Variables
# =========================
message_counter = 0
start_time = time.monotonic()


def make_mqtt_client():
    """Create a paho-mqtt client compatible with newer and older versions."""
    try:
        return mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=MQTT_CLIENT_ID
        )
    except AttributeError:
        return mqtt.Client(client_id=MQTT_CLIENT_ID)


def connect_mqtt():
    """Connect Raspberry Pi to MQTT broker."""
    print("Connecting to MQTT broker:", MQTT_BROKER)
    print("Client ID:", MQTT_CLIENT_ID)
    client = make_mqtt_client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    print("MQTT connected successfully!")
    print("Publishing to topic:", MQTT_TOPIC)
    return client


def read_sensor(dht_device):
    """Read temperature and humidity from DHT22."""
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if temperature is None or humidity is None:
            print("Sensor returned no data. Retrying next cycle.")
            return None, None

        return round(float(temperature), 1), round(float(humidity), 1)

    except RuntimeError as e:
        # DHT sensors often fail a single read; retrying is normal.
        print("Sensor read retry:", e)
        return None, None


def create_payload(temperature, humidity):
    """Create JSON payload compatible with subscriber_sqlite.py."""
    global message_counter

    message_counter += 1
    uptime_seconds = int(time.monotonic() - start_time)

    payload = {
        "device": "RaspberryPi-DHT22",
        "message_no": message_counter,
        "temperature": temperature,
        "humidity": humidity,
        "uptime_seconds": uptime_seconds
    }
    return json.dumps(payload)


def publish_data(client, temperature, humidity):
    """Publish sensor data to MQTT broker."""
    json_payload = create_payload(temperature, humidity)

    print("=" * 50)
    print("Message #:", message_counter)
    print("Temperature:", temperature, "C")
    print("Humidity:", humidity, "%")
    print("JSON:", json_payload)

    result = client.publish(MQTT_TOPIC, json_payload)
    result.wait_for_publish()

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print("Published successfully!")
        return True

    print("MQTT publish failed. Result code:", result.rc)
    return False


def main():
    print("=" * 60)
    print("Raspberry Pi 4/5 DHT22 MQTT Publisher")
    print("ICS 4111: Embedded Systems & IoT Lab")
    print("=" * 60)
    print("Make sure Raspberry Pi is already connected to WiFi/Ethernet.")

    # use_pulseio=False improves compatibility on Raspberry Pi boards.
    dht_device = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)
    print("DHT22 sensor initialized on GPIO4 / physical pin 7")

    try:
        client = connect_mqtt()
    except Exception as e:
        print("MQTT connection error:", e)
        dht_device.exit()
        return

    print("\nStarting sensor readings. Press Ctrl+C to stop.\n")

    try:
        while True:
            temperature, humidity = read_sensor(dht_device)
            if temperature is not None and humidity is not None:
                publish_data(client, temperature, humidity)
            else:
                print("Failed to read sensor, skipping this cycle.")
            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

    finally:
        dht_device.exit()
        client.loop_stop()
        client.disconnect()
        print("Clean shutdown complete.")


if __name__ == "__main__":
    main()
