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
    set_api_source('api_test')

from TaobaoSdk import SimbaLoginAuthsignGetRequest
from TaobaoSdk import TaobaoClient
from TaobaoSdk.Exceptions import ErrorResponseException
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_SOURCE
from tao_models.common.decorator import  tao_api_exception
from api_server.common.util import change_obj_to_dict_deeply
from api_server.services.api_service import ApiService

logger = logging.getLogger(__name__)

class SimbaLoginAuthsignGet(object):

    """     
       为了保证access_token和subway_token同时存在
       该接口单独调用taobao_client
    """

    @classmethod
    @tao_api_exception(20)
    def get_subway_token_with_access_token(cls, soft_code,nick,access_token):
        req = SimbaLoginAuthsignGetRequest()
        req.nick = nick
        app_key = APP_SETTINGS[soft_code]['app_key']
        app_secret = APP_SETTINGS[soft_code]['app_secret']
        params = ApiService.getReqParameters(req)
        taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
        rsp = ApiService.getResponseObj(taobao_client.execute(params, access_token))
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg,req=params,rsp=rsp)
        return change_obj_to_dict_deeply(rsp.subway_token)

if __name__ == '__main__':
    nick = "麦苗科技001"
    soft_code = 'SYB'
    access_token = '62011151ddc4cbf3f0777a7ZZa77e61da8cb381c3fcd6b6871727117'
    subway_token = SimbaLoginAuthsignGet.get_subway_token_with_access_token(soft_code, nick,access_token)
    print subway_token


