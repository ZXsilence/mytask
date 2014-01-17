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
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import UserGetRequest 
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class UserGet(object):

    @classmethod
    @tao_api_exception(3)
    def get_user_by_nick(cls, nick):
        req = UserGetRequest()
        req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp


if __name__ == '__main__':
    nick = 'chinchinstyle'
    result = UserGet.get_user_by_nick(nick)
    print type(result)
    print result.toDict()
