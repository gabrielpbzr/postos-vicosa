#!/usr/bin/python
# -*-coding:utf-8 -*-
"""
Main entry point
"""
import os
from model import DATABASE, Usuario, Posto, get_last_id, APIResponse
from bottle import Bottle, request, response, debug, abort, static_file

app = Bottle()

@app.route('/static/<filename:path>', method='GET')
def serve_static(filename):
    """
    Serve os arquivos estaticos para o cliente
    """
    path = os.getcwd() + os.path.sep + 'static' + os.path.sep
    return static_file(filename, root=path)


@app.route('/', methods='GET')
def index():
    """
    Endpoint pra testar a API! :)
    """
    api_response = APIResponse(data="Hello to our API")
    response.content_type = "application/json"
    return api_response.to_json()

@app.route('/postos/<row_id:int>', method='GET')
def get_posto(row_id):
    """
    Retorna um registro de posto ou 404 caso o mesmo
    nao seja encontrado.
    param:
        int - rowid
    """
    try:
        posto = Posto.get(Posto.id == row_id)
        response.content_type = "application/json"
        api_response = APIResponse(data=posto)
        return api_response.to_json()
    except Exception as exception:
        print "Deu ruim: "+ exception.message
        return abort(404, "Not found")

@app.route('/postos', method='GET')
@app.route('/postos/', method='GET')
def get_all_postos():
    """
    Retorna todos os registros de postos
    """
    try:
        data = []
        for posto in Posto.select():
            data.append(posto.to_json())

        response.content_type = "application/json"
        api_response = APIResponse(data=data)
        return api_response.to_json()
    except:
        return None

@app.route('/postos', method='POST')
def save_posto():
    """
    Processa o POST para salvar um novo registro de posto
    """
    # Le o parametro api_key, enviado no POST
    api_key = request.forms.api_key
    if not api_key:
        return abort(code=401, text="Unauthorized. API Key is mandatory")

    # Busca um usuario pela chave da API passado no POST
    usuario = Usuario.get(Usuario.api_key == api_key)
    if not usuario:
        return abort(code=401, text="Unauthorized. Invalid API Key")

    # Le o parametro nome, enviado no POST
    nome = request.forms.name
    if not nome:
        return abort(code=400, text="Bad Request. Field \"name\" is required")

    # Le o parametro latitude, enviado no POST
    latitude = request.forms.latitude
    if not latitude:
        return abort(code=400, text="Bad Request. Field \"latitude\" is required")

    # Le o parametro longitude, enviado no POST
    longitude = request.forms.longitude
    if not longitude:
        return abort(code=400, text="Bad Request. Field \"longitude\" is required")

    posto = Posto(nome=nome, latitude=latitude, longitude=longitude)
    posto.save()

    last_id = get_last_id(table='posto')

    response.set_header('Content-Type', 'text/plain')
    response.status = 201
    response.body = "/postos/%d"%last_id

    return response

@app.route('/usuarios', method='POST')
def save_user():
    """
    Processa o POST para salvar um novo registro de usuario
    """
    # Le o parametro nome, enviado no POST
    nome = request.forms.name
    if not nome:
        return abort(code=400, text="Bad Request. Field \"name\" is required")

    # Le o parametro latitude, enviado no POST
    email = request.forms.email
    if not email:
        return abort(code=400, text="Bad Request. Field \"email\" is required")
    #Verifica se consegue encontrar um outro usuario usando o email fornecido como parametro
    try:
        usuario = Usuario.get(Usuario.email == email)
        if usuario:
            return abort(code=409, text="Conflict. Email already in use by another account")
    except:
        # O email nao esta vinculado a nenhum usuario. Isso e bom!
        pass
    # Le o parametro longitude, enviado no POST
    password = request.forms.password
    if not password:
        return abort(code=400, text="Bad Request. Field \"password\" is required")

    usuario = Usuario(nome=nome, email=email, senha=password)
    usuario.save()

    last_id = get_last_id(table='usuario')

    api_response = APIResponse(code=201, message="Created", data=usuario)
    response.set_header('Content-Type', 'application/json')
    response.status = 201
    response.body = api_response.to_json()

    return response

@app.hook('before_request')
def on_before_request():
    """
    Função que roda antes de passar a request para a funcao de endpoint
    """
    DATABASE.connect()
    DATABASE.create_tables([Usuario, Posto], safe=True)
    print "Before request"

@app.hook('after_request')
def on_after_request():
    """
    Funcao pra ser executada depois de encerrar a funcao do endpoint
     e retornar o response
    """
    DATABASE.close()
    print "After request"

def main():
    """
    Setup da app
    """
    # Pra exibir mensagens mais claras durante o desenvolvimento
    # (retirar antes do deploy!!)
    debug(True)
    # Coloca o app pra rodar na porta 5000 ouvindo todos os endereços
    # e recarregando automaticamente ao fazer modificações no arquivo
    app.run(host='0.0.0.0', port=5000, reloader=True)

if __name__ == '__main__':
    main()
