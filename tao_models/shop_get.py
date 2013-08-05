#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')

from TaobaoSdk import ShopGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)


class ShopGet(object):

    DEFAULT_FIELDS = 'sid,cid,title,nick,desc,bulletin,pic_path,created,modified,shop_score'

    @classmethod
    @tao_api_exception()
    def get_shop(cls, nick, fields=DEFAULT_FIELDS):
        req = ShopGetRequest()
        req.nick = nick 
        req.fields = fields

        rsp = tao_model_settings.taobao_client.execute(req, '')[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.shop.toDict()



def test():
    nick = 'chinchinstyle'
    shop_info = ShopGet.get_shop(nick)
    print shop_info


if __name__ == '__main__':
    test()
