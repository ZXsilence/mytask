#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    #set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')

from TaobaoSdk import UserGetRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class UserGet(object):
    """
    """

    @classmethod
    @tao_api_exception(3)
    def get_user_by_nick(cls, nick):
        """
        """

        req = UserGetRequest()
        req.nick = nick
        rsp = tao_model_settings.taobao_client.execute(req,'')[0]
        if not rsp.isSuccess():
            print rsp.msg
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp


if __name__ == '__main__':
    nick = 'toto的窝'
    #nick = '十月妈咪旗舰店'
    result = UserGet.get_user_by_nick(nick)
    print type(result)
    print result.toDict()
