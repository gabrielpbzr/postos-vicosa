#!/usr/bin/python
# -*-coding:utf-8 -*-
"""
Main entrypoint
"""
from model import *
from bottle import Bottle, route, run, request, response, get, debug, abort
import json

app = Bottle()

@app.route('/', methods='GET')
def index():
    return "Hello!"

@app.route('/postos/<id:int>', method='GET')
def get_posto(id):
    try:
        posto = Posto.get(Posto._id==id)
        return posto.toJSON()
    except:
        return abort(404, "Not found")

@app.route('/postos/', method='GET')
def get_all_postos():
    try:
        data = []
        for posto in Posto.select():
            data.append(posto.toJSON())
        return json.dumps(data)
    except:
        print "Deu ruim"
        return None

@app.route('/postos', method='POST')
def save_posto():
    api_key = request.forms.api_key
    if not api_key:
        return abort(code=401, text="Unauthorized. API Key is mandatory")

    nome = request.forms.name
    if not nome:
        return abort(code=400, text="Bad Request. Field \"name\" is required")

    latitude = request.forms.latitude
    if not latitude:
        return abort(code=400, text="Bad Request. Field \"latitude\" is required")

    longitude = request.forms.longitude
    if not longitude:
        return abort(code=400, text="Bad Request. Field \"longitude\" is required")

    posto = Posto(nome=nome, latitude=latitude, longitude=longitude)
    posto.save()

    last_id = get_last_id(table='posto')
    
    response.set_header('Content-Type', 'text/plain');
    response.status=201
    response.body="/postos/%d"%last_id
    return response



def main():
    database.connect()
    database.create_tables([Posto], safe=True)
    debug(True)

    app.run(host='0.0.0.0', port=5000, reloader=True)

if __name__ == '__main__':
    main()
