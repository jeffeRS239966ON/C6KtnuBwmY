# 代码生成时间: 2025-09-15 00:51:58
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Password Manager - A simple tool for password encryption and decryption using Bottle framework
"""

from bottle import Bottle, request, response, run
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import os

# Constants
BLOCK_SIZE = 16  # AES block size in bytes
SECRET_KEY = os.urandom(BLOCK_SIZE)  # Generate a random secret key

# Initialize Bottle app
app = Bottle()

"""
Encrypts a password using AES-256
:param password: The password to encrypt
:return: A tuple containing the encrypted password and the initialization vector
"""
def encrypt_password(password):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(password.encode(), BLOCK_SIZE))
    iv = b64encode(cipher.iv).decode('utf-8')
    return iv, b64encode(ct_bytes).decode('utf-8')

"""
Decrypts a password using AES-256
:param password: The encrypted password to decrypt
:return: The decrypted password
"""
def decrypt_password(iv, password):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv=b64decode(iv))
    ct = b64decode(password)
    pt = unpad(cipher.decrypt(ct), BLOCK_SIZE)
    return pt.decode('utf-8')

# Route to encrypt a password
@app.route('/encrypt', method='POST')
def encrypt():
    try:
        password = request.forms.get('password')
        iv, encrypted_password = encrypt_password(password)
        response.content_type = 'application/json'
        return {'iv': iv, 'encrypted_password': encrypted_password}
    except Exception as e:
        response.status = 400
        return {'error': str(e)}

# Route to decrypt a password
@app.route('/decrypt', method='POST')
def decrypt():
    try:
        iv = request.forms.get('iv')
        encrypted_password = request.forms.get('encrypted_password')
        password = decrypt_password(iv, encrypted_password)
        response.content_type = 'application/json'
        return {'password': password}
    except Exception as e:
        response.status = 400
        return {'error': str(e)}

if __name__ == '__main__':
    run(app, host='localhost', port=8080)