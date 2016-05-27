# -*- coding: utf-8 -*-
"""
Configurações gerais da aplicação
"""

import os

BASEDIR = os.path.abspath(os.getcwd())
DATABASE_URL = os.path.join(BASEDIR, "db/data.db")
SECRET_KEY = "6b1fc3eee26272c0d79c708f78e7a7c9"