#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SellercatsListGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SellercatsListGet(object):

    @classmethod
    @tao_api_exception()
    def get_seller_cats_list(cls, nick):
        req = SellercatsListGetRequest()
        req.nick = nick 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        if not rsp.seller_cats:
            return []
        return change_obj_to_dict_deeply(rsp.seller_cats)

if __name__ == '__main__':
    print SellercatsListGet.get_seller_cats_list('chinchinstyle')

