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

from TaobaoSdk import VasSubscribeGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class VasSubscribeGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(30)
    def get_vas_subscribe(cls, nick, article_code):
        """
        given a campaign_id, get the adgroup list in this campaign
        """

        req = VasSubscribeGetRequest()
        req.nick = nick
        req.article_code = article_code 
        
        rsp = tao_model_settings.taobao_client.execute(req, '')[0]

        if not rsp.isSuccess():
            print rsp.msg, rsp.sub_msg
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.article_user_subscribes




if __name__ == '__main__':

    nick = 'chinchinstyle'
    article_code = 'ts-1796606'
    article_user_subscribes = VasSubscribeGet.get_vas_subscribe(nick, article_code)
    
    for article_user_subscribe in article_user_subscribes:
        print article_user_subscribe.toDict()
