#
# Обработка запросов клиентов
#

from flask import render_template, redirect, url_for, jsonify
import os

# Импорт других файлов проекта
from app import app, db
from models import Server
from forms import AddServer


# --- ТАБЛИЦА МОНИТОРИНГА -----------------------
@app.route('/')
@app.route('/index')
def index():
    servers = Server.query.all()
    ping = {}

    for server in servers:
        #if not os.system('ping -n 1 '+server.ip):
        if True:
            ping[server] = 'up'
        else:
            ping[server] = 'down'

    # Вернуть страницу
    return(render_template('index.html',
        states=ping))


# --- ОБНОВЛЕНИЕ ЧАСТИ ТАБЛИЦЫ МОНИТОРИНГА ------
@app.route('/index-ajax')
def index_ajax():
    #servers = Server.query.all()
    #ping = {}

    #for server in servers:
    #    if not os.system('ping -n 1 '+server.ip):
    #        ping[server.dns] = 'up'
    #    else:
    #        ping[server.dns] = 'down'

    #return(render_template('index_upd.html',
    #    states=ping))
    return(jsonify({'term11': 'down'}))


# --- ДОБАВЛЕНИЕ НОВОГО СЕРВЕРА -----------------
@app.route('/server/add', methods=['GET', 'POST'])
def server_add():
    form = AddServer()

    if form.validate_on_submit():
        form_dns = form.dns.data
        form_ip = form.ip.data

        new_server = Server(dns=form_dns, ip=form_ip)
        db.session.add(new_server)
        db.session.commit()

        return(redirect(url_for('index')))

    return(render_template('server_add.html',
        form=form))


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