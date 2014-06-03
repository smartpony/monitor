#
# Описание форм для ввода данных
#

from flask_wtf import Form
from wtforms import TextField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms_html5 import IntegerField

class ServerForm(Form):
    name = TextField(validators=[DataRequired()])
    dns = TextField()
    ip = TextField(validators=[DataRequired()])
    description = TextAreaField()

class SensorForm(Form):
    name = TextField()
    description = TextAreaField()
    # Тип (0 - ping, 1 - telnet)
    action = SelectField(choices=[('0', 'Ping'), ('1', 'Telnet')], default=0)
    # Ping: интервал (сек)
    # Telnet: интервал (сек), порт
    property_1 = TextField()
    property_2 = TextField()
    property_3 = TextField()
    property_4 = TextField()