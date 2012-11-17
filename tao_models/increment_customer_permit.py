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
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import IncrementCustomerPermitRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)


class IncrementCustomerPermit(object):


    @classmethod
    @tao_api_exception
    def set_customer_permit(cls, access_token):
        logger.info("set customer permit request")
        req = IncrementCustomerPermitRequest()
        req.type = 'get'
        req.topics = 'item'
        req.status = 'all'

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.app_customer




def test():
    access_token = "6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612"
    app_customer = IncrementCustomerPermit.set_customer_permit(access_token)
    print app_customer.toDict()
    for sub in app_customer.subscriptions:
        print sub.toDict()

if __name__ == '__main__':
    test()
