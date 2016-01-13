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
home_path = os.path.normpath(os.path.join(currDir,'../../../comm_lib/'))
sys.path.append(home_path)
from service_server.conf import set_env
set_env.getEnvReady()
API_THRIFT = {
        'host':'183.131.0.206',
        #'host':'10.117.3.35',
        'port':9999
    }

logger = logging.getLogger("api_server")
hdlr = logging.FileHandler('/alidata1/logs/service_server.log')
hdlr.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s:%(lineno)-15d %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
logger.propagate = False
