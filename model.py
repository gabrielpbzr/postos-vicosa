# -*- coding utf-8 -*-
"""
Modelos da aplicacao
"""
from peewee import SqliteDatabase, Model, IntegerField, CharField, DoubleField, OperationalError
import config
import json

database = SqliteDatabase(config.DATABASE_URL)

def get_last_id(table):
    """
        Retorna o id do ultimo registro da tabela
        param: @string table - nome da tabela
    """
    try:
        result = database.execute_sql("SELECT MAX(_id) FROM %s"%(table))
        return result.fetchall()[0][0]
    except OperationalError as oe:
        print oe.message
        return None
    

class BaseModel(Model):
    """
    Classe modelo para as classes do banco de dados
    """
    def toJSON(self):
        """
        Retorna a representacao JSON do objeto
        returns: string
        """
        objDict = self.__dict__
        return json.dumps(objDict['_data'])

    class Meta:
        database = database

class Posto(BaseModel):
    """
    Classe representando uma instancia de um posto
    Attributes:
        _id = Integer - identificador do registro
        nome = String - nome do Posto
        longitude e latitude = coordenadas da localizacao do posto no GPS
    """
    _id = IntegerField(primary_key=True)
    nome = CharField(max_length=100)
    longitude = DoubleField(null=False)
    latitude = DoubleField(null=False)

    #def __init__(self, nome, longitude, latitude, _id=None):
    #    self.nome = nome
    #    self.longitude = longitude
    #    self.latitude = latitude
    #    self._id = _id
