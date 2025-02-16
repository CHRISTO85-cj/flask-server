from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for Flutter app

DATABASE = "sensor_data.db"

# Function to connect to SQLite database
def connect_db():
    return sqlite3.connect(DATABASE)

# ✅ 1️⃣ Initialize the Database (Run once)
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pressure REAL,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ✅ 2️⃣ API to Receive Sensor Data
@app.route("/add_data", methods=["POST"])
def add_sensor_data():
    try:
        data = request.get_json()
        pressure = data.get("pressure")
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        rainfall = data.get("rainfall")

        if None in [pressure, temperature, humidity, rainfall]:
            return jsonify({"error": "Missing sensor values"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sensor_readings (pressure, temperature, humidity, rainfall) VALUES (?, ?, ?, ?)",
            (pressure, temperature, humidity, rainfall),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Sensor data added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ 3️⃣ API to Get Latest Sensor Data
@app.route("/latest_data", methods=["GET"])
def get_latest_data():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 1")
        data = cursor.fetchone()
        conn.close()

        if data:
            response = {
                "id": data[0],
                "pressure": data[1],
                "temperature": data[2],
                "humidity": data[3],
                "rainfall": data[4],
                "timestamp": data[5],
            }
            return jsonify(response)
        else:
            return jsonify({"message": "No data found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ 4️⃣ API to Get Historical Data (Last 10 Entries)
@app.route("/history", methods=["GET"])
def get_history():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 10")
        data = cursor.fetchall()
        conn.close()

        history = [
            {"id": row[0], "pressure": row[1], "temperature": row[2], "humidity": row[3], "rainfall": row[4], "timestamp": row[5]}
            for row in data
        ]
        return jsonify(history)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run Flask Server
if __name__ == "__main__":
    create_table()  # Ensure table is created
    app.run(host="0.0.0.0", port=5000, debug=True)
