# ===============================================================================
# ESP32 MicroPython - DHT22 Sensor with MQTT Publisher
# ICS 4111: Embedded Systems & IoT Lab
# 
# This file should be uploaded to your ESP32 using Thonny IDE
# ===============================================================================

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
WIFI_SSID = "YOUR_WIFI_NAME"        # Replace with your WiFi name
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"  # Replace with your WiFi password

# =========================
# MQTT Configuration
# =========================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab/sensor"

# Unique client ID for this ESP32 based on device MAC address
MQTT_CLIENT_ID = b"esp32-dht22-" + hexlify(unique_id())

# =========================
# Sensor Configuration
# =========================
DHT_PIN = 4  # GPIO4 (D4) - Change if you wired differently

# =========================
# Publishing Configuration
# =========================
PUBLISH_INTERVAL = 3  # Publish every 3 seconds (faster data collection)

# =========================
# Global Variables
# =========================
message_counter = 0
start_time = time.ticks_ms()


def connect_wifi():
    """Connect ESP32 to WiFi network with timeout and status feedback."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Connecting to WiFi:", WIFI_SSID)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Wait for connection (timeout after 30 seconds)
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
    else:
        print("WiFi connection failed. Check credentials and network.")
        return False


def connect_mqtt():
    """Connect ESP32 to MQTT broker with error handling."""
    print("\nConnecting to MQTT broker:", MQTT_BROKER)
    print("Client ID:", MQTT_CLIENT_ID.decode())
    
    try:
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
    except Exception as e:
        print("MQTT connection error:", e)
        raise


def read_sensor(sensor):
    """Read temperature and humidity from DHT22 sensor with error handling."""
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        return temperature, humidity
    except OSError as e:
        print("Sensor read error:", e)
        return None, None


def create_payload(temperature, humidity):
    """Create JSON payload for MQTT publishing."""
    global message_counter
    
    message_counter += 1
    uptime_seconds = time.ticks_diff(time.ticks_ms(), start_time) // 1000
    
    payload = {
        "device": "ESP32-DHT22",
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
        print("Temperature:", temperature, "°C")
        print("Humidity:", humidity, "%")
        print("JSON:", json_payload)
        
        client.publish(MQTT_TOPIC, json_payload)
        print("✓ Published successfully!")
        return True
    except Exception as e:
        print("✗ MQTT publish error:", e)
        return False


def main():
    """Main program loop with robust error handling and reconnection logic."""
    print("=" * 60)
    print("ESP32 DHT22 MQTT Publisher")
    print("ICS 4111: Embedded Systems & IoT Lab")
    print("=" * 60)
    
    # Connect to WiFi
    if not connect_wifi():
        print("\n⚠ Cannot proceed without WiFi. Please check credentials.")
        return
    
    # Initialize DHT22 sensor
    try:
        sensor = dht.DHT22(Pin(DHT_PIN))
        print("\nDHT22 sensor initialized on GPIO", DHT_PIN)
    except Exception as e:
        print("Sensor initialization error:", e)
        return
    
    # Connect to MQTT broker
    try:
        client = connect_mqtt()
    except Exception as e:
        print("Cannot proceed without MQTT connection.")
        return
    
    print("\n" + "=" * 60)
    print("Starting sensor readings...")
    print("Publishing every", PUBLISH_INTERVAL, "seconds")
    print("Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    # Main loop - read sensor and publish
    try:
        while True:
            # Read sensor data
            temperature, humidity = read_sensor(sensor)
            
            if temperature is not None and humidity is not None:
                # Publish data
                success = publish_data(client, temperature, humidity)
                
                if not success:
                    print("⚠ Publish failed, will retry on next cycle")
            else:
                print("⚠ Failed to read sensor, skipping this cycle")
            
            # Wait before next reading
            time.sleep(PUBLISH_INTERVAL)
            
    except KeyboardInterrupt:
        # Clean shutdown when user presses Ctrl+C
        print("\n\n" + "=" * 60)
        print("Program stopped by user")
        print("=" * 60)
        try:
            client.disconnect()
            print("✓ Disconnected from MQTT broker")
        except:
            pass
    
    except Exception as e:
        # Handle unexpected errors and attempt MQTT reconnection
        print("\n⚠ Unexpected error:", e)
        print("Attempting to reconnect MQTT...")
        
        try:
            client = connect_mqtt()
            print("✓ Reconnected! Resuming operation...")
            # Restart main loop by calling main() recursively
            main()
        except:
            print("✗ Reconnection failed. Please restart manually.")


# Run the program
if __name__ == "__main__":
    main()