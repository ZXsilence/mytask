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
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')

from TaobaoSdk import SimbaCreativeDeleteRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaCreativeDelete(object):

    @classmethod
    @tao_api_exception(5)
    def delete_creative(cls, access_token, nick, creative_id):

        req = SimbaCreativeDeleteRequest()
        req.nick = nick
        req.creative_id = creative_id 

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.debug("delete creative error nick [%s] msg [%s] sub_msg [%s]" %(nick
                , rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)


if __name__ == '__main__':
    nick = 'chinchinstyle'
    access_token = '6200e168f708b8167250268dfhe2555e99ed247caa1cdeb520500325'
    creative_id = 174804004 
    SimbaCreativeDelete.delete_creative(access_token,nick,creative_id) 


