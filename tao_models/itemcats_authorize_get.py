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
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import ItemcatsAuthorizeGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply


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
    nick = 'chinchinstyle'
    fields = 'brand.vid, brand.name, item_cat.cid, item_cat.name'
    print ItemcatsAuthorizeGet.get_itemcats_authorize(nick,fields)

