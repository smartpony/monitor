#
# Описание форм для ввода данных
#

from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired

class AddServer(Form):
    name = TextField(validators=[DataRequired()])
    description = TextField()
    dns = TextField()
    ip = TextField(validators=[DataRequired()])
    sensor_ping = BooleanField(default=False)