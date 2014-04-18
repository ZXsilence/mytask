#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf.set_env import getEnvReady
    getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaAccountBalanceGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAccountBalanceGet(object):

    @classmethod
    @tao_api_exception(3)
    def get_account_balance(cls, nick):
        req = SimbaAccountBalanceGetRequest()
        req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.balance)

if __name__ == '__main__':
    balance = SimbaAccountBalanceGet.get_account_balance('麦苗科技001')
    print balance

