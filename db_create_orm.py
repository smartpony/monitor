#
# Создание базы и таблиц через SQLAlchemy
#

# Импорт модели
from app import db

# Создание базы согласно заданной модели
db.create_all()

# Создание набора серваков
from app.models import Server

srv1 = Server(name='server1',
	dns='server1.local',
    ip='10.10.10.1',
    sensor_ping=True)
db.session.add(srv1)

srv2 = Server(name='server2',
	dns='server2.local',
    ip='10.10.10.2',
    sensor_ping=True)
db.session.add(srv2)

srv3 = Server(name='server3',
	dns='server3.local',
    ip='10.10.10.3',
    sensor_ping=True)
db.session.add(srv3)

db.session.commit()