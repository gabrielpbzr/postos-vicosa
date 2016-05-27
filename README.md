# API Postos
=============

Uma API com informações dos postos de gasolina da cidade de Viçosa-MG. 

## Endpoints

| ENDPOINT    | METHOD | DESCRIPTION                                 |
|-------------|:------:|:--------------------------------------------|
|/postos      | GET    | Lista todos os postos                       |
|/postos/[id] | GET    | Lista um posto pelo seu identificador       |
|/postos      | POST   | Adiciona um novo posto (Exige chave da API) |

### GET /postos
Parâmetros:
==========
    Nenhum parametro especial exigido
 

## Tecnologias empregadas
 - Python
 - Bottle
 - Peewee ORM
 - SQLite
 
