from asgiref.wsgi import WsgiToAsgi
from app import app  # ������������ ��� Flask-������

# ���������� Flask-���������� � ASGI
asgi_app = WsgiToAsgi(app)