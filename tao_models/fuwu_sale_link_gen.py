#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import FuwuSaleLinkGenRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class FuwuSaleLinkGen(object):

    @classmethod
    @tao_api_exception(3)
    def fuwu_sale_link_gen(cls, nick, param_str,soft_code):
        req = FuwuSaleLinkGenRequest()
        req.nick = nick 
        req.param_str = param_str 
        rsp = ApiService.execute(req,None,soft_code)
        return change_obj_to_dict_deeply(rsp.url)


if __name__ == '__main__':

    nick = 'chinchinstyle'
    soft_code = 'SYB'
    param_str = """
        {"param":{"aCode":"ACT_847721042_130517115127","itemList":["ts-1796606-3"],"promIds":[10058712],"type":2},"sign":"E2896D1E94845D1B82FFE9FBF8A9D18E"}
        """
    url = FuwuSaleLinkGen.fuwu_sale_link_gen(nick, param_str,soft_code)
    print url
