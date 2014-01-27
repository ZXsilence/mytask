#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config
from datetime import datetime
import datetime as dt

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import IncrementCustomerPermitRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class IncrementCustomerPermit(object):

    @classmethod
    @tao_api_exception()
    def set_customer_permit(cls, nick,soft_code):
        logger.info("set customer permit request")
        req = IncrementCustomerPermitRequest()
        req.type = 'get'
        req.topics = 'item'
        req.status = 'all'
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.app_customer)

def test():
    nick = 'chinchinstyle'
    soft_code = 'SYB'
    app_customer = IncrementCustomerPermit.set_customer_permit(nick,soft_code)
    print app_customer

if __name__ == '__main__':
    test()
