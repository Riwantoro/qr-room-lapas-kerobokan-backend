#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load data from JSON file
try:
    with open('wbp.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("Data loaded successfully from wbp.json")
except FileNotFoundError:
    print("Error: wbp.json not found!")
    data = {}
except json.JSONDecodeError:
    print("Error: Invalid JSON format in wbp.json!")
    data = {}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Flask Backend API is running!",
        "status": "success",
        "endpoints": [
            "/api/rooms - Get all rooms",
            "/api/occupants/<room> - Get occupants by room",
            "/api/room/<room_name> - Get room data (alternative endpoint)"
        ]
    })

@app.route('/api/rooms', methods=['GET'])
def get_all_rooms():
    try:
        if not data or '05_03_2025' not in data:
            return jsonify({"error": "No data available"}), 404
        
        # Extract unique rooms from data
        rooms = set()
        for entry in data['05_03_2025'][1:]:  # Skip header
            wisma = entry.get('wisma', '')
            if ' - ' in wisma:
                room = wisma.split(' - ')[1]
                rooms.add(room)
        
        return jsonify({
            "status": "success",
            "rooms": sorted(list(rooms)),
            "total_rooms": len(rooms)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/occupants/<room>', methods=['GET'])
def get_room_occupants(room):
    try:
        if not data or '05_03_2025' not in data:
            return jsonify({"error": "No data available"}), 404
        
        occupants = []
        for entry in data['05_03_2025'][1:]:  # Skip header
            wisma = entry.get('wisma', '')
            if f' - {room}' in wisma:
                occupants.append({
                    'nama': entry.get('nama', ''),
                    'no_registrasi': entry.get('no_registrasi', ''),
                    'pidana': entry.get('pidana', '').split(' - ')[0] if entry.get('pidana') else '',
                    'tanggal_masuk': entry.get('tanggal_masuk', ''),
                    'tanggal_ekspirasi': entry.get('tanggal_ekspirasi', ''),
                    'wisma': wisma
                })
        
        return jsonify({
            "status": "success",
            "room": room,
            "occupants": occupants,
            "total_occupants": len(occupants)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/room/<room_name>', methods=['GET'])
def get_room_data(room_name):
    try:
        # This endpoint seems to use a different file structure
        # Adapting to use the same wbp.json data
        if not data or '05_03_2025' not in data:
            return jsonify({"error": "No data available"}), 404
        
        room_data = []
        for entry in data['05_03_2025'][1:]:  # Skip header
            wisma = entry.get('wisma', '')
            # More flexible matching
            if room_name.replace(" ", "").upper() in wisma.replace(" ", "").upper():
                room_data.append({
                    'nama': entry.get('nama', ''),
                    'no_registrasi': entry.get('no_registrasi', ''),
                    'pidana': entry.get('pidana', ''),
                    'tanggal_masuk': entry.get('tanggal_masuk', ''),
                    'tanggal_ekspirasi': entry.get('tanggal_ekspirasi', ''),
                    'wisma': wisma
                })
        
        return jsonify({
            "status": "success",
            "room_name": room_name,
            "data": room_data,
            "total_records": len(room_data)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Flask app is running",
        "data_loaded": bool(data)
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this automatically)
    port = int(os.environ.get('PORT', 5000))
    # Get debug mode from environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Flask app on port {port}")
    print(f"Debug mode: {debug_mode}")
    
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=debug_mode
    )