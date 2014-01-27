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
    set_api_source('api_test')

from TaobaoSdk import SimbaCustomersAuthorizedGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCustomersAuthorizedGet(object):

    @classmethod
    @tao_api_exception(3)
    def get_authorized_customers(cls, nick):
        """
        given a campaign_id, get the adgroup list in this campaign
        """
        req = SimbaCustomersAuthorizedGetRequest()
        req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.nicks)

if __name__ == '__main__':

    nick = 'chinchinstyle'
    nicks = SimbaCustomersAuthorizedGet.get_authorized_customers(nick)
    for nick in nicks:
        print nick
