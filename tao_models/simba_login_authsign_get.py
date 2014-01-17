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
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaLoginAuthsignGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaLoginAuthsignGet(object):

    @classmethod
    @tao_api_exception(20)
    def get_subway_token(cls, soft_code,nick):
        """
        given a campaign_id, get the adgroup list in this campaign
        """
        req = SimbaLoginAuthsignGetRequest()
        req.nick = nick
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.subway_token)

if __name__ == '__main__':
    nick = "chinchinstyle"
    soft_code = 'BD'
    subway_token = SimbaLoginAuthsignGet.get_subway_token(soft_code, nick)
    print subway_token
