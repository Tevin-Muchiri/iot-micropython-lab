import json
import sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt

# =========================
# MQTT Settings
# =========================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab/sensor"

# =========================
# SQLite Settings
# =========================
DB_NAME = "sensor_data.db"


def create_database():
    """Create SQLite database and sensor_data table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT,
            message_no INTEGER,
            temperature REAL,
            humidity REAL,
            uptime_seconds INTEGER,
            mqtt_topic TEXT,
            received_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_sensor_data(data, topic):
    """Insert received MQTT JSON data into SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    device = data.get("device", "ESP32-DHT22")
    message_no = data.get("message_no", None)

    # Accept both "temperature" and old "temp" key just in case
    temperature = data.get("temperature", data.get("temp", None))
    humidity = data.get("humidity", None)

    uptime_seconds = data.get("uptime_seconds", None)
    received_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO sensor_data (
            device,
            message_no,
            temperature,
            humidity,
            uptime_seconds,
            mqtt_topic,
            received_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        device,
        message_no,
        temperature,
        humidity,
        uptime_seconds,
        topic,
        received_at
    ))

    conn.commit()
    conn.close()

    print("Saved to database:")
    print("Device:", device)
    print("Message No:", message_no)
    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Received At:", received_at)
    print("-" * 50)


def show_latest_rows():
    """Display latest 10 records from SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, device, message_no, temperature, humidity, received_at
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    conn.close()

    print("\nLatest database records:")
    for row in rows:
        print(row)


def on_connect(client, userdata, flags, reason_code, *extra):
    """Callback when MQTT client connects to broker."""
    print("Connected to MQTT broker.")
    print("Connection code:", reason_code)
    print("Subscribing to topic:", MQTT_TOPIC)

    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, message):
    """Callback when MQTT message is received."""
    try:
        payload = message.payload.decode("utf-8")
        print("\nMessage received from topic:", message.topic)
        print("Raw payload:", payload)

        data = json.loads(payload)

        insert_sensor_data(data, message.topic)
        show_latest_rows()

    except json.JSONDecodeError:
        print("Error: Received message is not valid JSON.")

    except Exception as e:
        print("Error while processing message:", e)


def main():
    create_database()

    print("Database ready:", DB_NAME)
    print("Connecting to MQTT broker:", MQTT_BROKER)

    # Compatible with newer and older paho-mqtt versions
    try:
        client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id="pc-sqlite-subscriber"
        )
    except AttributeError:
        client = mqtt.Client(client_id="pc-sqlite-subscriber")

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    print("Waiting for ESP32 sensor data...")
    print("Press Ctrl + C to stop.\n")

    client.loop_forever()


if __name__ == "__main__":
    main()
