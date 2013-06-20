#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import SimbaAccountBalanceGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaAccountBalanceGet(object):
    """
    """

    @classmethod
    @tao_api_exception(3)
    def get_account_balance(cls, access_token, nick):
        """
        """

        req = SimbaAccountBalanceGetRequest()
        req.nick = nick

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.error("nick [%s] get acccount balance failed, msg [%s] sub_msg [%s]", nick, rsp.msg, rsp.sub_msg) 
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.balance


if __name__ == '__main__':

    access_token = '6201d21d3bfa761000e15d6f4c1d3ZZ2331a6010d1ab4a8520500325'
    nick = 'chinchinstyle'

    balance = SimbaAccountBalanceGet.get_account_balance(access_token, nick)
    
    print balance
