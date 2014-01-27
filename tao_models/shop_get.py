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

from TaobaoSdk import ShopGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk import TaobaoClient
from TaobaoSdk.Exceptions import ErrorResponseException
from api_server.services.api_record_service import ApiRecordService
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_SOURCE

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

    @classmethod
    @tao_api_exception()
    def get_shop_with_access_token(cls,nick,access_token,soft_code,fields=DEFAULT_FIELDS):
        req = ShopGetRequest()
        req.nick = nick 
        req.fields = fields
        app_key = APP_SETTINGS[soft_code]['app_key']
        app_secret = APP_SETTINGS[soft_code]['app_secret']
        taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
        params = ApiService.getReqParameters(req)
        rsp = ApiService.getResponseObj(taobao_client.execute(params, access_token))
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg,req=params,rsp=rsp)
        return change_obj_to_dict_deeply(rsp.shop)


def test():
    nick = '麦苗科技001'
    access_token = '62011151ddc4cbf3f0777a7ZZa77e61da8cb381c3fcd6b6871727117'
    soft_code = 'SYB'
    shop_info = ShopGet.get_shop_with_access_token(nick,access_token,soft_code)
    print shop_info

if __name__ == '__main__':
    test()
