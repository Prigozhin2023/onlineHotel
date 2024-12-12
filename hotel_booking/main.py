# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import User, Hotel, Room, Booking

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel_booking.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book_room():
    data = request.json
    user_id = data.get('user_id')
    room_id = data.get('room_id')
    check_in_date = datetime.strptime(data.get('check_in_date'), '%Y-%m-%d').date()
    check_out_date = datetime.strptime(data.get('check_out_date'), '%Y-%m-%d').date()

    booking = Booking(user_id=user_id, room_id=room_id, check_in_date=check_in_date, check_out_date=check_out_date)
    db.session.add(booking)
    db.session.commit()

    return jsonify({'message': 'Booking successful!'})

@app.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{'id': room.id, 'hotel_id': room.hotel_id, 'room_type': room.room_type, 'price_per_night': room.price_per_night} for room in rooms])

@app.route('/room/<int:room_id>', methods=['GET'])
def get_room_by_id(room_id):
    room = Room.query.get(room_id)
    if room is None:
        return jsonify({'error': 'Room not found'}), 404
    return jsonify({
        'id': room.id,
        'hotel_id': room.hotel_id,
        'room_type': room.room_type,
        'price_per_night': room.price_per_night
    })

@app.route('/rooms_list', methods=['GET'])
def rooms_list():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True)