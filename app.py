#!/usr/bin/env python3
print("File ditemukan! Lokasi:", __file__)

from flask import Flask, jsonify
import json

app = Flask(__name__)

# Load data from JSON file
with open('wbp.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    

@app.route('/api/rooms', methods=['GET'])
def get_all_rooms():
    # Extract unique rooms from data
    rooms = set()
    for entry in data['05_03_2025'][1:]:  # Skip header
        wisma = entry['wisma']
        if ' - ' in wisma:
            room = wisma.split(' - ')[1]
            rooms.add(room)
    return jsonify(sorted(list(rooms)))

@app.route('/api/occupants/<room>', methods=['GET'])
def get_room_occupants(room):
    occupants = []
    for entry in data['05_03_2025'][1:]:  # Skip header
        wisma = entry['wisma']
        if f' - {room}' in wisma:
            occupants.append({
                'nama': entry['nama'],
                'no_registrasi': entry['no_registrasi'],
                'pidana': entry['pidana'].split(' - ')[0],
                'tanggal_masuk': entry['tanggal_masuk'],
                'tanggal_ekspirasi': entry['tanggal_ekspirasi']
            })
    return jsonify(occupants)

@app.route("/api/room/<room_name>")
def get_room_data(room_name):
    with open("backend/inmates.json") as f:
        data = json.load(f)
    room_data = [inmate for inmate in data if inmate["wisma"].replace(" ", "").upper() == room_name.replace(" ", "").upper()]
    return jsonify(room_data)

handler = app  # for Vercel

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)