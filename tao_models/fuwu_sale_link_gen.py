#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import FuwuSaleLinkGenRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.common.decorator import  tao_api_exception
from tao_models.conf import settings as tao_model_settings

logger = logging.getLogger(__name__)

class FuwuSaleLinkGen(object):
    """
    """

    @classmethod
    @tao_api_exception(3)
    def fuwu_sale_link_gen(cls, nick, param_str):
        """
        """

        req = FuwuSaleLinkGenRequest()
        req.nick = nick 
        req.param_str = param_str 

        rsp = tao_model_settings.taobao_client.execute(req, '')[0]
        if not rsp.isSuccess():
            print rsp.msg
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.url


if __name__ == '__main__':

    nick = 'chinchinstyle'
    param_str = """
        {"param":{"aCode":"ACT_847721042_130517115127","itemList":["ts-1796606-3"],"promIds":[10058712],"type":2},"sign":"E2896D1E94845D1B82FFE9FBF8A9D18E"}
        """
    url = FuwuSaleLinkGen.fuwu_sale_link_gen(nick, param_str)
    print url
