#
# Создание базы и таблиц через SQLAlchemy
#

# Импорт модели
from app import db

# Создание базы согласно заданной модели
db.create_all()

# Создание набора серваков
from app.models import Server

srv1 = Server(name='srv1',
    dns='srv1.local',
    ip='10.0.0.1',
    sensor_ping=True,
    sensor_telnet=True)
db.session.add(srv1)

srv2 = Server(name='srv2',
    dns='srv2.local',
    ip='10.0.0.2',
    sensor_ping=True,
    sensor_telnet=True)
db.session.add(srv2)

srv3 = Server(name='srv3',
    dns='srv3.local',
    ip='10.0.0.3',
    sensor_ping=True,
    sensor_telnet=True)
db.session.add(srv3)

db.session.commit()