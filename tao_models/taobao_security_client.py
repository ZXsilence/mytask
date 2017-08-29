#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xieguanfu
@contact: xieguanfu@maimiaotech.com
@date: 2017-08-29 11:11
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
if __name__ == '__main__':
    import os,sys
    sys.path.append('../../comm_lib/')
    sys.path.append('../../TaobaoOpenPythonSDK/')
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')
    from tao_models.secret_get import SecretGet


import time
from datetime import datetime

class TaoBaoSecurityClient():

    SPLIT_CHAR_DICT = {'nick':'~', 'normal':unichr(0x01), 'search':'~', 'phone':'$', 'receiver_name':'~', 'simple':'~'}
    SECRET_CACHE = {}
    IV = '0102030405060708'

    @classmethod
    def decrypt(cls,data,decrypt_type,session,nick,soft_code = 'SYB',current_version = None):
        #用户解密入口
        assert decrypt_type in cls.SPLIT_CHAR_DICT
        ##获取分隔符
        char_value = cls.SPLIT_CHAR_DICT[decrypt_type]
        ##校验
        if not (data[0] == char_value and data[-1] == char_value):
            return data

        if data[len(data) -2] == char_value:
            #未用到,我们不需要使用
            secret_dto = cls.get_index_secret_data(data,char_value)
        else:
            secret_dto = cls.get_secret_data(data,char_value)

        ##非法密文
        if not secret_dto:
            return data
        user_secret_data = cls.get_user_secret(session,nick,soft_code,current_version)
        if not user_secret_data:
            raise Exception('not get user secret')
        user_secret = user_secret_data['secret']
        decrypt_value = AesSecurity.decrypt_aes(secret_dto['origin_base64'],user_secret,cls.IV)
        if decrypt_type == 'phone' and not secret_dto.get('is_search'):
            decrypt_value = secret_dto.get('origin_value','') + decrypt_value
        return decrypt_value

    @classmethod
    def encrypt(cls,data,decrypt_type,session,nick,soft_code = 'SYB',current_version = None):
        #用户加密入口
        assert decrypt_type in cls.SPLIT_CHAR_DICT and cls.SPLIT_CHAR_DICT.get(decrypt_type)
        char_value = cls.SPLIT_CHAR_DICT[decrypt_type]
        #user_secret_data = {'secret':'cVE1/bLZlGy5llntfRjr+g==','secret_version':1}
        user_secret_data = cls.get_user_secret(session,nick,soft_code,current_version)
        if not user_secret_data:
            raise Exception('not get user secret')
        user_secret = user_secret_data['secret']
        version = user_secret_data['secret_version']
        if 'phone' == decrypt_type:
            data = str(data)
            prefix_number = data[:len(data)-8]
            encrypt_value = AesSecurity.encrypt_aes(data[-8:],user_secret,cls.IV)
            encrypt_value = char_value + prefix_number + char_value + encrypt_value + char_value + str(version) + char_value
        else:
            encrypt_value = AesSecurity.encrypt_aes(data,user_secret,cls.IV)
            encrypt_value = char_value + encrypt_value + char_value + str(version) + char_value
        return encrypt_value

    @classmethod
    def get_secret_data(cls,data,char_value):
        if cls.SPLIT_CHAR_DICT['phone'] == char_value:
            data_list = [item for item in data.split(char_value) if item.strip() or item == 0]
            if len(data_list) != 3:
                return
            version = data_list[2]
            if version.isdigit():
                return {'version':version,'origin_value':data_list[0],'origin_base64':data_list[1]}
        else:
            data_list = data.split(char_value)
            data_list = [item for item in data.split(char_value) if item.strip() or item == 0]
            if len(data_list) != 2:
                return
            version = data_list[1]
            if version.isdigit():
                return {'version':version,'origin_base64':data_list[0]}

    @classmethod
    def get_index_secret_data(cls,data,char_value):
        pass

    @classmethod
    def get_user_secret(cls,session,nick,soft_code,version):
        from tao_models.secret_get import SecretGet
        cache_key = '%s%s' %(session,version) if version else session
        secret_data = cls.SECRET_CACHE.get(cache_key)
        now = datetime.now()
        _t = long(time.mktime(now.utctimetuple())*1000)
        if secret_data and secret_data['invalid_time'] > _t:
            return secret_data
        elif not secret_data or secret_data['invalid_time'] < _t:
            data = SecretGet.get_secret(nick,soft_code)
            if not data:
                return
            item = {'secret_version':data['secret_version'],'secret':data['secret'],'invalid_time':_t + data['interval'] * 1000,\
                    'max_invalid_time':_t + data['max_interval'] * 1000}
            cls.SECRET_CACHE[cache_key] = item
            return item
        else:
            return secret_data

class AesSecurity():

    @classmethod
    def decrypt_aes(cls,message,key,iv):
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
    def encrypt_aes(cls,message,key,iv):
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
        print ciphertext
        return ciphertext 

if __name__ == '__main__':
    nick = '麦苗科技001'
    session = '6200d01c6ZZa832f6187a7f120bc4bab8b9226e3fd2dae0871727117'
    decrypt_type = 'simple'
    data = '~0CIwQjv4HrtmeUyEuRe79A==~1~'
    data = '~i7/JXRUo/SdDNv5z1yEPqsPAoU67PG4pT6lqMBwLenQ=~1~'

    data = '娃儿高伟光235额外'
    decrypt_type = 'simple'
    ret_data = TaoBaoSecurityClient.encrypt(data,decrypt_type,session,nick)
    print ret_data
    ret_data = TaoBaoSecurityClient.decrypt(ret_data,decrypt_type,session,nick)
    print ret_data

