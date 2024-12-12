# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, User  # Импортируйте db и модель User

# Создаем экземпляр приложения Flask
app = Flask(__name__)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel_booking.db'  # Укажите путь к вашей базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем ненужные сообщения

# Инициализируем SQLAlchemy для приложения
db.init_app(app)

# Главная страница (форма регистрации)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение данных из формы
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверка на уникальность имени пользователя и email
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Имя пользователя уже занято'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email уже занят'}), 400

        # Создание нового пользователя
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Перенаправление на страницу бронирования
        return redirect(url_for('booking'))

    # Если метод GET, отображаем форму регистрации
    return render_template('register.html')

# Страница бронирования
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        room = request.form['room']
        name = request.form['name']
        return render_template('booking_details.html', checkin=checkin, checkout=checkout, room=room, name=name)

    # Если метод GET, отображаем форму бронирования
    return render_template('index.html')

# Маршрут для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получение данных из формы
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Проверка на уникальность имени пользователя и email
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Имя пользователя уже занято'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email уже занят'}), 400

        # Создание нового пользователя
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Перенаправление на страницу бронирования
        return redirect(url_for('booking'))

    # Если метод GET, отображаем форму регистрации
    return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц в базе данных
    app.run(host="0.0.0.0", port=5000,debug=True)
