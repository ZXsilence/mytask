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
    set_api_source('normal_test')

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
        soft_code = soft_code
        rsp = ApiService.execute(req,nick=nick,soft_code=soft_code)
        return change_obj_to_dict_deeply(rsp.url)


if __name__ == '__main__':

    nick = '麦苗科技001'
    soft_code = "YZB"
    param_str = """
    {"param":{"aCode":"ACT_1101933802_170622134424","itemList":["FW_GOODS-1000078795-1:1*2"],"promIds":[1002011602],"type":1},"sign":"9DBE865F21001748E0EDC0FAA22CC1F9"}
        """
    url = FuwuSaleLinkGen.fuwu_sale_link_gen(nick, param_str,soft_code)
    print url
