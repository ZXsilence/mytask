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

from TaobaoSdk import SimbaCampaignUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCampaignUpdate(object):
    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def update_campaign(cls, nick, campaign_id, title, online_status):
        """
        更新一个计划的标题和上下线 
        """
        req = SimbaCampaignUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.title = title
        req.online_status = online_status
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.campaign)


if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3328400
    title = '麦苗省油宝计划test'
    online_status = 'offline'
    campaign = SimbaCampaignUpdate.update_campaign(nick, campaign_id, title, online_status)
    print campaign

