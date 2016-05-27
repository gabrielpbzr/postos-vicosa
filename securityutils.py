"""
Utilitarios de seguranca
"""
import string
import random
from binascii import hexlify
from simplecrypt import encrypt
import config

def generate_password(length=16):
    """
    Gera uma senha randomica para o usuario
    param:
        int - length
    return:
        string - encrypted password
    """
    random_string = ""
    chars = string.hexdigits[:16]
    for i in range(0, length):
        random_string += random.choice(chars)
    return random_string

def encrypt_password(password):
    """
    Gera uma string criptografada com a senha fornecida.
    param:
        string - password
    return:
        string - encrypted password
    """
    encrypted_password = encrypt(password, config.SECRET_KEY)
    return hexlify(encrypted_password)
    