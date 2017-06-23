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

from TaobaoSdk import ItemcatsAuthorizeGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply


logger = logging.getLogger(__name__)

class ItemcatsAuthorizeGet(object):

    @classmethod
    @tao_api_exception()
    def get_itemcats_authorize(cls, nick, fields):
        req = ItemcatsAuthorizeGetRequest()
        req.fields = fields
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.seller_authorize)

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    fields = 'brand.name'
    print ItemcatsAuthorizeGet.get_itemcats_authorize(nick,fields)
