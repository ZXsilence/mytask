#encoding=utf8
"""doc string for module"""
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging

from shop_db.services.shop_db_service import ShopDBService
from tao_models.common.exceptions import  InvalidAccessTokenException
from tao_models.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN
from TaobaoSdk.Exceptions import ErrorResponseException
from TaobaoSdk import  TaobaoClient

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    
logger = logging.getLogger(__name__)

def change_obj_to_dict_deeply(obj):
    result_dict = {}
    if type(obj) == type([]):
        #列表转换
        return [change_obj_to_dict_deeply(sub_obj) for sub_obj in obj]
    elif isinstance(obj,object) and obj.__class__.__module__.startswith('Domain'):
        result_dict = obj.toDict()
    elif type(obj) == type({}):
        result_dict = obj
    else:
        #基本类型，无需转换
        return obj
    keys = result_dict.keys()
    for key in keys:
        #迭代转换
        if isinstance(result_dict[key],object) and result_dict[key].__class__.__module__.startswith('Domain'):
            result_dict[key] = change_obj_to_dict_deeply(result_dict[key])
        elif type(result_dict[key]) == type([]):
            result_dict[key] = [change_obj_to_dict_deeply(obj) for obj in result_dict[key]]
    return result_dict

