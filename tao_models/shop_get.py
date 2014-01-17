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
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import ShopGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class ShopGet(object):

    DEFAULT_FIELDS = 'sid,cid,title,nick,desc,bulletin,pic_path,created,modified,shop_score'

    @classmethod
    @tao_api_exception()
    def get_shop(cls, nick, fields=DEFAULT_FIELDS):
        req = ShopGetRequest()
        req.nick = nick 
        req.fields = fields
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.shop)


def test():
    nick = 'chinchinstyle'
    shop_info = ShopGet.get_shop(nick)
    print shop_info

if __name__ == '__main__':
    test()
