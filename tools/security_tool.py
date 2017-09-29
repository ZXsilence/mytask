#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : CarlosLee
# * Email         : lichen@maimiaotech.com
# * Create time   : 2017-09-20 17:44
# * Last modified : 2017-09-20 17:44
# * Filename      : security_tool.py
# * Description   : 
# **********************************************************


class AesSecurity():

    @classmethod
    def decrypt_aes(cls,message,key,iv='0102030405060708'):
        from Crypto.Cipher import AES  
        import base64
        #数据解密
        real_key = base64.b64decode(key)
        obj = AES.new(real_key, AES.MODE_CBC, iv)
        message_decode = base64.b64decode(message)
        ciphertext = obj.decrypt(message_decode)
        unpad = lambda s : s[0:-ord(s[-1])] 
        ciphertext = unpad(ciphertext)
        return ciphertext

    @classmethod
    def encrypt_aes(cls,message,key,iv='0102030405060708'):
        from Crypto.Cipher import AES  
        import base64
        #数据加密
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        message = pad(message)
        key = base64.b64decode(key)
        obj = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = obj.encrypt(message)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext 

if __name__ == '__main__':
    import base64
    import simplejson as json
    a = '{"nick":"carlos","sid":1234515}'
    key = '123lee0000000000'
    a = base64.b64encode(a)
    key = base64.b64encode(key)
    secret = AesSecurity.encrypt_aes(a,key)
    print secret
    express = AesSecurity.decrypt_aes(secret,key)
    print json.loads(base64.b64decode(express))['nick']
