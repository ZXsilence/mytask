#encoding=utf8
__author__ = 'zhoujiebing@maimiaotech.com'

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

from TaobaoSdk import SimbaCustomersAuthorizedGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaCustomersAuthorizedGet(object):
    """
    """

    @classmethod
    @tao_api_exception(3)
    def get_authorized_customers(cls, access_token, nick):
        """
        given a campaign_id, get the adgroup list in this campaign
        """

        req = SimbaCustomersAuthorizedGetRequest()
        req.nick = nick

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.debug("get_subway_token failed, msg [%s] sub_msg [%s]", rsp.msg, rsp.sub_msg) 
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.nicks

if __name__ == '__main__':

    access_token = '6201330d6b3c8bf9cec0abcb062bf7e59289fegi9ca6031520500325'
    nick = 'chinchinstyle'
    nicks = SimbaCustomersAuthorizedGet.get_authorized_customers(access_token, nick)
    for nick in nicks:
        print nick
