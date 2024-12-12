from asgiref.wsgi import WsgiToAsgi
from app import app  # Импортируйте ваш Flask-объект

# Адаптируем Flask-приложение к ASGI
asgi_app = WsgiToAsgi(app)