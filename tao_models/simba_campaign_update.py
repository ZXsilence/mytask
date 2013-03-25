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

from TaobaoSdk import SimbaCampaignUpdateRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaCampaignUpdate(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def update_campaign(cls, access_token, nick, campaign_id, title, online_status):
        """
        更新一个计划的标题和上下线 
        """

        req = SimbaCampaignUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.title = title
        req.online_status = online_status

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.error("update_campaign error nick [%s] msg [%s] sub_msg [%s]" %(nick
                , rsp.msg, rsp.sub_msg))
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.campaign




if __name__ == '__main__':

    nick = 'chinchinstyle'
    access_token = '6201616c8a94a43419fef76dfh8bbba34c4f2ec3ffadb3b520500325'
    campaign_id = '3328400'
    title = '麦苗省油宝计划'
    online_status = 'online'

    campaign = SimbaCampaignUpdate.update_campaign(access_token, nick, campaign_id, title, online_status)
    
    print campaign.toDict()
