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
    set_api_source('normal_test')

import urllib
import simplejson
from TaobaoSdk import TopAuthTokenCreateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk import TaobaoClient
from TaobaoSdk.Exceptions import ErrorResponseException
from api_server.services.api_record_service import ApiRecordService
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_SOURCE

logger = logging.getLogger(__name__)


class TaoBaoAuthTokenCreate(object):

    @classmethod
    @tao_api_exception()
    def get_auth_token(cls,code,soft_code):
        req = TopAuthTokenCreateRequest()
        req.code = code
        app_key = APP_SETTINGS[soft_code]['app_key']
        app_secret = APP_SETTINGS[soft_code]['app_secret']
        taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
        params = ApiService.getReqParameters(req)
        rsp = taobao_client.execute(params,None)
        if 'error_response' in rsp:
            info = rsp['error_response']
            raise ErrorResponseException(code=info['code'], msg=info['msg'], sub_code=info['sub_code'], sub_msg=info['sub_msg'])
        token_result = simplejson.loads(rsp['top_auth_token_create_response']['token_result'])
        token_result['taobao_user_nick'] = urllib.unquote_plus(token_result['taobao_user_nick'])
        return token_result

if __name__ == '__main__':
    code = 'sO1BKVG1BZiIAMSVmdcsnRId374808'
    TaoBaoAuthTokenCreate.get_auth_token(code,'SYB')
