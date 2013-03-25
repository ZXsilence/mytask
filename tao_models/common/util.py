#encoding=utf8
"""doc string for module"""
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import traceback
import inspect

from time import  sleep
from datetime import datetime
import simplejson as json


from pymongo import Connection
from pymongo.errors import AutoReconnect

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    
logger = logging.getLogger(__name__)
mail_logger = logging.getLogger('django.request')

BD_APP = {
        'APP_KEY':'21065688',
        'APP_SECRET':'74aecdce10af604343e942a324641891'
        }

SYB_APP = {
        'APP_KEY':'12685542',
        'APP_SECRET':'6599a8ba3455d0b2a043ecab96dfa6f9'
        }

RMT_APP = {
        'APP_KEY':'12651461',
        'APP_SECRET':'80a15051c411f9ca52d664ebde46a9da'
        }

MGDBS = {
        'bd':{
            'HOST':'xcw.maimiaotech.com',
            'PORT':27017,
            'USER':'',
            'PASSWORD':''
        },

        'syb':{
            'HOST':'syb.maimiaotech.com',
            'PORT':1990,
            'USER':'',
            'PASSWORD':''
        },

        'rmt':{
            'HOST':'xcwtest.maimiaotech.com',
            'PORT':1996,
            'USER':'',
            'PASSWORD':''
        }
}


def get_test_token_dict(type,nick):
    #设置APP_KEY
    from tao_models.conf.settings import set_taobao_client
    if type == 'bd':
        set_taobao_client(BD_APP['APP_KEY'],BD_APP['APP_SECRET']) 
    if type == 'syb':
        set_taobao_client(SYB_APP['APP_KEY'],SYB_APP['APP_SECRET']) 
    if type == 'rmt':
        set_taobao_client(RMT_APP['APP_KEY'],RMT_APP['APP_SECRET']) 
    #获取token
    mongoConn = Connection(host=MGDBS[type]['HOST'],port=MGDBS[type]['PORT'])
    #mongoConn = Connection('xcw.maimiaotech.com',27017)
    coll = mongoConn['CommonInfo']['shop_info']
    shop_info = coll.find_one({'nick':nick})
    print shop_info
    return shop_info


if __name__ == '__main__':
    #get_test_token_dict('rmt','chinchinstyle')
    get_test_token_dict('syb','chinchinstyle')
    #get_test_token_dict('bd','chinchinstyle')


