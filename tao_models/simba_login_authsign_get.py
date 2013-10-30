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

from TaobaoSdk import SimbaLoginAuthsignGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaLoginAuthsignGet(object):
    """
    """

    @classmethod
    @tao_api_exception(20)
    def get_subway_token(cls, access_token, nick):
        """
        given a campaign_id, get the adgroup list in this campaign
        """

        req = SimbaLoginAuthsignGetRequest()
        req.nick = nick

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.debug("get_subway_token failed, msg [%s] sub_msg [%s]", rsp.msg, rsp.sub_msg) 
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.subway_token




if __name__ == '__main__':

    access_token = '620121280fd0192a7a96ZZ0aeab0b2ec9692374e165b5b9871727117'
    #nick = "十月妈咪旗舰店"
    nick = "热风旗舰店"
    subway_token = SimbaLoginAuthsignGet.get_subway_token(access_token, nick)
    print nick,"\t",subway_token 
