#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaCampaignPlatformGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCampaignPlatformGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def get_campaign_platform(cls, nick, campaign_id,cache = True):
        """
        获得一个计划的推广平台设置 
        """

        req = SimbaCampaignPlatformGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code,cache = cache)
        return change_obj_to_dict_deeply(rsp.campaign_platform)




if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = '3328400'
    result = SimbaCampaignPlatformGet.get_campaign_platform(nick, campaign_id)
    print result
