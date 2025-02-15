from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from Flutter

# Store latest sensor data
sensor_data = {
    "temperature": None,
    "humidity": None,
    "rainfall": None,
    "pressure": None
}

@app.route('/')
def home():
    return jsonify({"message": "Flask Server Running"}), 200

# API to receive sensor data from Arduino
@app.route('/update', methods=['POST'])
def update_data():
    try:
        data = request.json  # Get JSON data from POST request
        sensor_data["temperature"] = data.get("temperature")
        sensor_data["humidity"] = data.get("humidity")
        sensor_data["rainfall"] = data.get("rainfall")
        sensor_data["pressure"] = data.get("pressure")

        return jsonify({"message": "Data updated successfully", "data": sensor_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# API to fetch the latest sensor data
@app.route('/latest', methods=['GET'])
def get_latest_data():
    return jsonify(sensor_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
