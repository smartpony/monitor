#
# Обработка запросов клиентов
#

from flask import render_template, redirect, url_for, jsonify, request
import os
from datetime import datetime
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)
import socket

# Импорт других файлов проекта
from app import app, db
from models import Server
from forms import AddServer


# --- ТАБЛИЦА МОНИТОРИНГА -----------------------
@app.route('/')
@app.route('/index')
def index():
    servers = Server.query.all()
    return(render_template('index.html',
        servers=servers))


# --- ОБНОВЛЕНИЕ ЧАСТИ ТАБЛИЦЫ МОНИТОРИНГА ------
@app.route('/index-ajax')
def index_ajax():
    servers = Server.query.all()
    ping = {}
    telnet = {}
    PORT = 445

    # Параллельный пинг всех серверов
    # Создание заданий (неспосредственно запуск пингов)
    for server in servers:
        ping[server.id] = pool.apply_async(os.system, ['ping -n 1 -w 1500 '+server.ip])
        new_socket = socket.socket()
        new_socket.settimeout(0.5)
        socket_res = new_socket.connect_ex((server.ip, PORT))
        if socket_res == 0:
            telnet[server.id] = 'up'
        else:
            telnet[server.id] = 'down'
    # Сбор результатов выполненных заданий с ожиданием максимум 2 секунды
    for server_id in ping:
        if not ping[server_id].get(timeout=2):
            ping[server_id] = 'up'
        else:
            ping[server_id] = 'down'
    
    # Вложенный словарь со всеми полученными выше данными
    monitoring_data = {}
    for server in servers:
        sensors = {}
        sensors['ping'] = ping[server.id]
        sensors['telnet'] = telnet[server.id]
        monitoring_data[server.id] = sensors

    return(jsonify(monitoring_data))


# --- ДОБАВЛЕНИЕ НОВОГО СЕРВЕРА -----------------
@app.route('/server/add', methods=['GET', 'POST'])
def server_add():
    form = AddServer()

    if form.validate_on_submit():
        form_name = form.name.data
        form_dns = form.dns.data
        form_ip = form.ip.data
        form_sensor_ping = form.sensor_ping.data
        form_sensor_telnet = form.sensor_telnet.data

        new_server = Server(name=form_name,
            dns=form_dns,
            ip=form_ip,
            sensor_ping=form_sensor_ping,
            sensor_telnet=form_sensor_telnet)
        db.session.add(new_server)
        db.session.commit()

        return(redirect(url_for('index')))

    return(render_template('server_add.html',
        form=form))


# --- ПРОФИЛЬ СЕРВЕРА ---------------------------
@app.route('/server/profile/<server_id>', methods=['GET', 'POST'])
def server_profile(server_id):
    form = AddServer()
    server = Server.query.get(server_id)

    if form.validate_on_submit():
        form_name = form.name.data
        form_dns = form.dns.data
        form_ip = form.ip.data
        form_sensor_ping = form.sensor_ping.data
        form_sensor_telnet = form.sensor_telnet.data

        server.name = form_name
        server.dns = form_dns
        server.ip = form_ip
        server.sensor_ping = form_sensor_ping
        server.sensor_telnet = form_sensor_telnet
        db.session.commit()

        return(redirect(request.referrer))

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