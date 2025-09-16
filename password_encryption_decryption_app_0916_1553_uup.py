# 代码生成时间: 2025-09-16 15:53:58
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Password Encryption Decryption Tool
==============================
A simple Bottle web application for encrypting and decrypting passwords.
"""

from bottle import route, run, request, response
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import binascii
import os


class PasswordCrypto:
    """
    A class for encrypting and decrypting passwords.
    """"
    def __init__(self, key):
        self.key = key
        self.cipher = AES.new(self.key, AES.MODE_CBC)

    def encrypt(self, plaintext):
        """
        Encrypt the plaintext using AES.
        :param plaintext: The password to be encrypted.
        :return: The encrypted password.
        """
        plaintext_bytes = plaintext.encode('utf-8')
        padded_plaintext = pad(plaintext_bytes, AES.block_size)
        encrypted_bytes = self.cipher.encrypt(padded_plaintext)
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(self, ciphertext):
        """
        Decrypt the ciphertext using AES.
        :param ciphertext: The encrypted password to be decrypted.
        :return: The decrypted password.
        """
        encrypted_bytes = base64.b64decode(ciphertext)
        decrypted_bytes = unpad(self.cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted_bytes.decode('utf-8')


# Generate a secure random key
key = get_random_bytes(16)
crypto = PasswordCrypto(key)


@route('/encrypt', method='POST')
def encrypt_password():
    """
    Endpoint to encrypt a password.
    """
    try:
        plaintext = request.json.get('password')
        if not plaintext:
            response.status = 400
            return {"error": "Password is required"}

        encrypted_password = crypto.encrypt(plaintext)
        return {"encrypted_password": encrypted_password}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}


@route('/decrypt', method='POST')
def decrypt_password():
    """
    Endpoint to decrypt a password.
    """
    try:
        ciphertext = request.json.get('password')
        if not ciphertext:
            response.status = 400
            return {"error": "Encrypted password is required"}

        decrypted_password = crypto.decrypt(ciphertext)
        return {"decrypted_password": decrypted_password}
    except (ValueError, binascii.Error) as e:
        response.status = 400
        return {"error": "Invalid encrypted password"}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}


if __name__ == '__main__':
    run(host='localhost', port=8080)
