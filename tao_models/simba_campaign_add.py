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

from TaobaoSdk import SimbaCampaignAddRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaCampaignAdd(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def add_campaign(cls, access_token, nick, title):
        """
        创建一个计划 
        """

        req = SimbaCampaignAddRequest()
        req.nick = nick
        req.title = title

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.error("add_campaign error nick [%s] title [%s] msg [%s] sub_msg [%s]" %(nick, 
                title, rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.campaign




if __name__ == '__main__':

    access_token = '6201011016ade5298c4ZZ0c4bff2e7b98fcad8ebcf11d58520500325'
    nick = 'chinchinstyle'
    title = '麦苗省油宝计划'

    campaign = SimbaCampaignAdd.add_campaign(access_token, nick, title)
    
    print campaign.toDict()
