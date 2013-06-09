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

from TaobaoSdk import SimbaCampaignChanneloptionsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaCampaignChanneloptionsGet(object):
    """
    """

    @classmethod
    @tao_api_exception(5)
    def get_campaign_channeloptions(cls, access_token, nick):
        """
        获得一个计划的推广平台设置 
        """
        req = SimbaCampaignChanneloptionsGetRequest()
        req.nick = nick

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.error("get_campaign_channeloptions  error nick [%s] msg [%s] sub_msg [%s]" %(nick
                 , rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.channel_options




if __name__ == '__main__':

    #access_token = '6201f2547291c68de14fbd5ba958d3d50ZZ3e50adc7f9ca1030924525'
    #nick = u'雅鹭萱婚纱批发'
    nick = 'chinchinstyle'
    access_token = '6201616c8a94a43419fef76dfh8bbba34c4f2ec3ffadb3b520500325'

    result = SimbaCampaignChanneloptionsGet.get_campaign_channeloptions(access_token, nick)
    for channel in result:
        print channel.toDict()
