#encoding=utf8
__author__ = "xieguanfu"

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

from TaobaoSdk import LogisticsAddressSearchRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class LogisticsAddressSearch(object):
    """
        获取卖家地址库
    """

    @classmethod
    @tao_api_exception()
    def get_logistics_address(cls, nick):
        req =LogisticsAddressSearchRequest()
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.addresses)
   
if __name__=="__main__":
    nick = 'chinchinstyle'
    addresses=LogisticsAddressSearch.get_logistics_address(nick)
    for address in addresses:
        print address
