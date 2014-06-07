#
# Обработка запросов клиентов
#

from flask import render_template, redirect, url_for, jsonify, request, abort
import os
from datetime import datetime
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)
import socket
import json

# Импорт других файлов проекта
from app import app, db
from models import Server, Sensor
from forms import ServerForm, SensorForm


# --- ТАБЛИЦА МОНИТОРИНГА -----------------------
@app.route('/')
@app.route('/index')
@app.route('/table')
def index():
    servers = Server.query.all()

    return(render_template('index.html',
        servers=servers))


# --- ТАБЛИЦА МОНИТОРИНГА ОТДЕЛЬНОГО СЕРВЕРА ----
@app.route('/server/table/<server_id>')
def server_table(server_id):
    server = Server.query.get(server_id)

    # Проверка существования объекта
    if not server:
        abort(404)

    return(render_template('server_table.html',
        server=server))


# --- ОБНОВЛЕНИЕ ЧАСТИ ТАБЛИЦЫ МОНИТОРИНГА ------
@app.route('/index-ajax')
def index_ajax():
    sensors_data = {}
    server_id = request.args.get('server')
    if server_id == 'all':
        servers = Server.query.all()
    else:
        servers = [Server.query.get(int(server_id))]

    '''
    Старый кусок с параллельным пингом
    for server in servers:
        if server.sensor_ping:
            ping_results[server.id] = pool.apply_async(os.system, ['ping -n 1 -w 1500 '+server.ip])
        if server.sensor_telnet:
            telnet_ports = json.loads(server.sensor_telnet_ports)
            telnet_results[server.id] = {}
            for port in telnet_ports:
                port = int(port)
                new_socket = socket.socket()
                new_socket.settimeout(0.5)
                socket_res = new_socket.connect_ex((server.ip, port))
                if socket_res == 0:
                    telnet_results[server.id][port] = 'up'
                else:
                    telnet_results[server.id][port] = 'down'
    '''

    # Работа всех сенсоров (последовательно)
    for server in servers:
        sensors_data[server.id] = {}
        for sensor in server.sensor:
            # Ping
            if sensor.action == 0:
                ping_res = os.system('ping -n 1 -w 1500 '+server.ip)
                if ping_res == 0:
                    sensors_data[server.id][sensor.id] = True
                else:
                    sensors_data[server.id][sensor.id] = False
            # Telnet
            elif sensor.action == 1:
                port = int(sensor.property_2)
                new_socket = socket.socket()
                new_socket.settimeout(0.5)
                socket_res = new_socket.connect_ex((server.ip, port))
                if socket_res == 0:
                    sensors_data[server.id][sensor.id] = True
                else:
                    sensors_data[server.id][sensor.id] = False

    return(jsonify(sensors_data))


# --- ДОБАВЛЕНИЕ НОВОГО СЕРВЕРА -----------------
@app.route('/server/add', methods=['GET', 'POST'])
def server_add():
    form = ServerForm()

    if form.validate_on_submit():
        form_name = form.name.data
        form_dns = form.dns.data
        form_ip = form.ip.data
        form_description = form.description.data

        new_server = Server(name=form_name,
            dns=form_dns,
            ip=form_ip,
            description=form_description)
        db.session.add(new_server)
        db.session.commit()

        return(redirect(url_for('index')))

    return(render_template('server_add.html',
        form=form))


# --- ПРОФИЛЬ СЕРВЕРА ---------------------------
@app.route('/server/profile/<server_id>', methods=['GET', 'POST'])
def server_profile(server_id):
    form = ServerForm()
    server = Server.query.get(server_id)

    # Проверка существования объекта
    if not server:
        abort(404)

    if form.validate_on_submit():
        server.name = form.name.data
        server.dns = form.dns.data
        server.ip = form.ip.data
        server.description = form.description.data
        db.session.commit()

        return(redirect(request.referrer))

    # Вывод старого описания, по-другому никак потому что это TextArea
    form.description.data = server.description

    return(render_template('server_profile.html',
        form=form,
        server=server))


# --- УДАЛЕНИЕ СЕРВЕРА --------------------------
@app.route('/server/del/<server_id>')
def server_del(server_id):
    server = Server.query.get(server_id)

    # Проверка существования объекта
    if not server:
        abort(404)

    db.session.delete(server)
    db.session.commit()

    return(redirect(url_for('index')))


# --- ДОБАВЛЕНИЕ СЕНСОРА ------------------------
@app.route('/server/newsensor/<server_id>', methods=['GET', 'POST'])
def sensor_add(server_id):
    form = SensorForm()
    server = Server.query.get(server_id)

    # Проверка существования объекта
    if not server:
        abort(404)

    if form.validate_on_submit():
        form_name = form.name.data
        form_action = int(form.action.data)
        form_property_1 = form.property_1.data
        form_property_2 = form.property_2.data
        form_property_3 = form.property_3.data
        form_property_4 = form.property_4.data
        form_description = form.description.data

        new_sensor = Sensor(name=form_name,
            action=form_action,
            property_1=form_property_1,
            property_2=form_property_2,
            property_3=form_property_3,
            property_4=form_property_4,
            description=form_description,
            server_id=server.id)
        db.session.add(new_sensor)
        db.session.commit()

        return(redirect(url_for('server_profile', server_id=server.id)))

    return(render_template('sensor_add.html',
        form=form))


# --- ПРОФИЛЬ СЕНСОРА ---------------------------
@app.route('/sensor/profile/<sensor_id>', methods=['GET', 'POST'])
def sensor_profile(sensor_id):
    form = SensorForm()
    sensor = Sensor.query.get(sensor_id)

    # Проверка существования объекта
    if not sensor:
        abort(404)

    if form.validate_on_submit():
        sensor.name = form.name.data
        sensor.action = int(form.action.data)
        sensor.property_1 = form.property_1.data
        sensor.property_2 = form.property_2.data
        sensor.property_3 = form.property_3.data
        sensor.property_4 = form.property_4.data
        sensor.description = form.description.data
        db.session.commit()

        return(redirect(url_for('server_profile', server_id=sensor.server_id)))

    # Вывод старого описания, по-другому никак потому что это TextArea
    form.description.data = sensor.description

    return(render_template('sensor_profile.html',
        form=form,
        sensor=sensor))


# --- УДАЛЕНИЕ СЕНСОРА --------------------------
@app.route('/sensor/del/<sensor_id>')
def sensor_del(sensor_id):
    sensor = Sensor.query.get(sensor_id)
    server_id = sensor.server_id

    # Проверка существования объекта
    if not sensor:
        abort(404)

    db.session.delete(sensor)
    db.session.commit()

    return(redirect(url_for('server_profile', server_id=server_id)))



# --- УДАЛЕНИЕ СЕНСОРА --------------------------
@app.route('/plot')
def plot():
    return(render_template('plot.html'))