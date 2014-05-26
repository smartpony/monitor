#
# Создание базы и таблиц через SQLAlchemy
#

# Импорт модели
from app import db

# Создание базы согласно заданной модели
db.create_all()

# Создание набора серваков
from app.models import Server, Sensor

# Серверы
srv1 = Server(name='term11',
    description='Citrix terminal',
	dns='blgatb-term11.atb.su',
    ip='10.52.203.44')
db.session.add(srv1)

srv2 = Server(name='bsd-dns',
    description='DNS server',
    ip='10.52.3.31')
db.session.add(srv2)

srv3 = Server(name='prtg',
    description='Monitoring system',
	dns='blgatb-prtg.atb.su',
    ip='10.52.3.187')
db.session.add(srv3)

db.session.commit()


# Сенсоры
snr11 = Sensor(name='ping',
    action=0,
    property_1='5',
    server_id=1)
db.session.add(snr11)
snr12 =Sensor(name='telnet',
    description='Microsoft DS',
    action=1,
    property_1='5',
    property_2='445',
    server_id=1)
db.session.add(snr12)

snr21 = Sensor(name='ping',
    action=0,
    property_1='5',
    server_id=2)
db.session.add(snr21)
snr22 =Sensor(name='telnet',
    description='DNS',
    action=1,
    property_1='5',
    property_2='53',
    server_id=2)
db.session.add(snr22)
snr23 =Sensor(name='telnet',
    description='SSH',
    action=1,
    property_1='5',
    property_2='22',
    server_id=2)
db.session.add(snr23)

snr31 = Sensor(name='ping',
    action=0,
    property_1='5',
    server_id=3)
db.session.add(snr31)
snr32 =Sensor(name='telnet',
    description='Microsoft DS',
    action=1,
    property_1='5',
    property_2='445',
    server_id=3)
db.session.add(snr32)

db.session.commit()