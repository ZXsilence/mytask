#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import VasSubscribeGetRequest
from TaobaoSdk import TaobaoClient
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_SOURCE

logger = logging.getLogger(__name__)

class VasSubscribeGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def get_vas_subscribe(cls, nick, soft_code, article_code=None):
        """
        given a campaign_id, get the adgroup list in this campaign
        """
        req = VasSubscribeGetRequest()
        req.nick = nick
        req.article_code = article_code if article_code else APP_SETTINGS[soft_code]['article_code']
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.article_user_subscribes)

    @classmethod
    @tao_api_exception(5)
    def get_vas_subscribe_by_sdk(cls, nick,soft_code):
        req = VasSubscribeGetRequest()
        req.nick = nick
        req.article_code = APP_SETTINGS[soft_code]['article_code']
        app_key = APP_SETTINGS[soft_code]['app_key']
        app_secret = APP_SETTINGS[soft_code]['app_secret']
        params = ApiService.getReqParameters(req)
        taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
        rsp = ApiService.getResponseObj(taobao_client.execute(params, ''))
        if rsp.isSuccess():
            return change_obj_to_dict_deeply(rsp.article_user_subscribes)
        return []



if __name__ == '__main__':
    nick = '麦苗科技001'
    soft_code = 'SYB'
    article_user_subscribes = VasSubscribeGet.get_vas_subscribe(nick, soft_code, 'FW_GOODS-1000495518')
    print article_user_subscribes
