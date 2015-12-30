#encoding=utf8
import os, sys
import pymongo
from pymongo import Connection
import logging
import MySQLdb
from DBUtils.PooledDB import PooledDB

if pymongo.version.startswith("2.5"):
    import bson.objectid
    import bson.json_util
    pymongo.objectid = bson.objectid
    pymongo.json_util = bson.json_util
    sys.modules['pymongo.objectid'] = bson.objectid
    sys.modules['pymongo.json_util'] = bson.json_util

currDir = os.path.normpath(os.path.dirname(__file__))
BACKENDS = os.path.normpath(os.path.join(currDir,'../../../backends/'))
sys.path.append(BACKENDS)
API_HOST = "121.199.170.144"
API_PORT = 30002 
SERVER_URL = "http://%s:%s/router/rest" %(API_HOST,API_PORT)

API_THRIFT = {
        'host':'localhost',
        'port':9090
    }


logger = logging.getLogger("api_server")
hdlr = logging.FileHandler('/alidata1/logs/service_server.log')
hdlr.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s:%(lineno)-15d %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
logger.propagate = False

