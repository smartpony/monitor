#
# Описание модели БД для ORM
#

# Импорт главного объекта БД
from app import app, db


# Пользователи
class Server(db.Model):
    __tablename__ = 'Server'

    # ID сервера
    id = db.Column(db.Integer, primary_key=True)
    # Имя для отображения в таблице
    name = db.Column(db.Text, nullable=False)
    # Описание сервера
    description = db.Column(db.Text)
    # DNS-имя
    dns = db.Column(db.Text)
    # IP адрес
    ip = db.Column(db.Text, nullable=False)
    # Сенсор: ping
    sensor_ping = db.Column(db.Boolean, default=False)
    # Сенсор: telnet на 445 порт
    sensor_telnet = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return('<Server ID%d>' % self.id)