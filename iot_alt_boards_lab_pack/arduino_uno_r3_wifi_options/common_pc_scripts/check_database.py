import sqlite3

DB_NAME = "sensor_data.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

print("Running SQLite SELECT query:")
print("SELECT * FROM sensor_data;")
print("-" * 80)

cursor.execute("""
    SELECT id, device, message_no, temperature, humidity, uptime_seconds, mqtt_topic, received_at
    FROM sensor_data
    ORDER BY id ASC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()