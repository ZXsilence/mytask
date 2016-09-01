#encoding=utf8
# Django settings for xuanciw project.
import os, sys
import pymongo
from pymongo import Connection
import logging

if pymongo.version.startswith("2.5"):
    import bson.objectid
    import bson.json_util
    pymongo.objectid = bson.objectid
    pymongo.json_util = bson.json_util
    sys.modules['pymongo.objectid'] = bson.objectid
    sys.modules['pymongo.json_util'] = bson.json_util



#MONGODB SETTINGS
MGDBS = {
        'user':{
            'HOST':'10.117.38.235',
            'PORT':2201,
            'USER':'',
            'PASSWORD':''
        }
    }


#利用mongodb 自带的connection poll 来管理数据库连接
mongoConn = None

def get_conn():
    global mongoConn
    if not mongoConn:
        mongoConn = Connection(host=MGDBS['user']['HOST'],port=MGDBS['user']['PORT'],network_timeout=1)
    return mongoConn

def get_collection(db_name,table_name):
    return get_conn()[db_name][table_name]

