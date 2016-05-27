# -*- coding utf-8 -*-
"""
Modelos da aplicacao
author: Gabriel P. Bezerra
"""
import json
from peewee import SqliteDatabase, Model, IntegerField, CharField, \
                   DoubleField, ForeignKeyField, OperationalError
import config
import securityutils as su


DATABASE = SqliteDatabase(config.DATABASE_URL)

def get_last_id(table):
    """
        Retorna o id do ultimo registro da tabela
        param: string table - nome da tabela
    """
    try:
        result = DATABASE.execute_sql("SELECT MAX(id) FROM %s"%(table))
        return result.fetchall()[0][0]
    except OperationalError as o_error:
        print o_error.message
        return None


class BaseModel(Model):
    """
    Classe modelo para as classes do banco de dados baseada na
    classe Model do peewee
    """
    def to_json(self):
        """
        Retorna a representacao JSON do objeto
        returns: string
        """
        obj_dict = self.__dict__
        return obj_dict['_data']

    class Meta:
        database = DATABASE

class Usuario(BaseModel):
    """
    Classe representando o usuario do sistema
    Attributes:
        uid: Integer - identificador do registro
        nome: String
        email: String
        senha: String
        api_key: String
    """
    nome = CharField(max_length=100)
    email = CharField(max_length=100, null=False, unique=True)
    senha = CharField(max_length=255, null=False)
    api_key = CharField(max_length=128, unique=True)

    def __init__(self, nome, email, senha, api_key=None):
        # Chama o construtor da super classe
        super(Usuario, self).__init__(self)
        self.nome = nome
        self.email = email
        self.senha = su.encrypt_password(senha)
        if not api_key:
            api_key = su.generate_password(length=32)
        self.api_key = api_key

    def to_json(self):
        obj_dict = super(Usuario, self).to_json()
        del obj_dict['senha']
        return obj_dict

class Posto(BaseModel):
    """
    Classe representando uma instancia de um posto
    Attributes:
        pid = Integer - identificador do registro
        nome = String - nome do Posto
        longitude e latitude = coordenadas da localizacao do posto no GPS
    """
    nome = CharField(max_length=100)
    longitude = DoubleField(null=False)
    latitude = DoubleField(null=False)
    usuario = ForeignKeyField(rel_model=Usuario, related_name="postos")

class APIResponse(object):
    """
    Classe que representa a estrutura de resposta da API
    """
    def __init__(self, code=200, message="OK", data=None):
        """
        Inicializa um objeto APIResponse
        Parameters:
        code: HTTP status code,
        message: A response message to display
        data: the data to be sent
        """
        self.code = code
        self.message = message
        self.data = data

    def to_json(self):
        """
        Retorna a representacao JSON do objeto
        """
        obj_dict = {}
        obj_dict['code'] = self.code
        obj_dict['message'] = self.message
        if isinstance(self.data, BaseModel):
            obj_dict['data'] = self.data.to_json()
        else:
            obj_dict['data'] = self.data
        return json.dumps(obj_dict)

    