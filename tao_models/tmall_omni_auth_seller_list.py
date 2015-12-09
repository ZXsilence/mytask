#encoding=utf8
__author__ = 'zhoujiebing@maimiaotech.com'

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

from TaobaoSdk import TaobaoClient
from TaobaoSdk import TmallOmniAuthSellerListRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from api_server.conf.settings import APP_SETTINGS,SERVER_URL

logger = logging.getLogger(__name__)

class TmallOmniAuthSellerList(object):

    @classmethod
    @tao_api_exception(3)
    def get_authorized_customers(cls):
        """
        """
        req = TmallOmniAuthSellerListRequest()
        req.page_no = 1
        req.page_size = 200
        soft_code = 'philips'
        app_key = APP_SETTINGS[soft_code]['app_key']
        app_secret = APP_SETTINGS[soft_code]['app_secret']
        params = ApiService.getReqParameters(req)
        taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
        while True:
            rsp = ApiService.getResponseObj(taobao_client.execute(params, ''))
            import pdb; pdb.set_trace()  # XXX BREAKPOINT
            break
        #return change_obj_to_dict_deeply(rsp.nicks)

if __name__ == '__main__':
    TmallOmniAuthSellerList.get_authorized_customers()
