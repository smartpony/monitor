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
    # Имя, заданное пользователем
    name = db.Column(db.Text, nullable=False)
    # Описание
    description = db.Column(db.Text)
    # DNS-имя
    dns = db.Column(db.Text)
    # IP адрес
    ip = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return('<Server ID%d>' % self.id)

# Сенсоры
class Sensor(db.Model):
    __tablename__ = 'Sensor'

    # ID сенсора
    id = db.Column(db.Integer, primary_key=True)
    # Имя, заданное пользователем
    name = db.Column(db.Text, nullable=False)
    # Описание
    description = db.Column(db.Text)
    # Тип (0 - ping, 1 - telnet)
    action = db.Column(db.Integer, nullable=False)
    # Ping: интервал (сек)
    # Telnet: интервал (сек), порт
    property_1 = db.Column(db.Text)
    property_2 = db.Column(db.Text)
    property_3 = db.Column(db.Text)
    property_4 = db.Column(db.Text)

    # Обратная связь с таблицей серверов
    server_id = db.Column(db.Integer, db.ForeignKey('Server.id'))
    server = db.relationship('Server',
        #foreign_keys=[server_id],
        backref=db.backref('sensor', cascade='delete', lazy='dynamic'))

    def __repr__(self):
        return('<Sensor ID%d>' % self.id)