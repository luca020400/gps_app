#!/usr/bin/env python3

import sqlite3
from flask import Flask, g, jsonify, request
app = Flask(__name__, static_url_path='', static_folder='.')

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/send_gps", methods=['POST'])
def send_gps():
    json_res = request.get_json(force=True)
    db = get_db()
    cur = db.cursor()
    cur.execute("insert into gps_data values (?,?,?,?,?,?)", (
        json_res['uuid'],
        float(json_res['latitude']),
        float(json_res['longitude']),
        float(json_res['altitude']),
        json_res['time'],
        json_res['provider'],
    ))
    cur.close()
    db.commit()
    return jsonify(json_res)

@app.route("/get_gps", methods=['GET'])
def get_gps():
    json_res = []
    data = query_db('select * from gps_data')
    for gps_data in data:
        data = {
            "uuid": gps_data[0],
            "latitude": gps_data[1],
            "longitude": gps_data[2],
            "altitude": gps_data[3],
            "time": gps_data[4],
            "provider": gps_data[5],
        }
        json_res.append(data)
    return jsonify(json_res)

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
