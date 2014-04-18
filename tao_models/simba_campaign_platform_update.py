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

from TaobaoSdk import SimbaCampaignPlatformUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCampaignPlatformUpdate(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def update_campaign_platform(cls, nick, campaign_id, search_channels, nonsearch_channels, outside_discount):
        """
        更新一个计划的推广平台设置 
        """
        nonsearch_channels = ','.join([str(e) for e in nonsearch_channels]) 
        search_channels = ','.join([str(e) for e in search_channels]) 
        req = SimbaCampaignPlatformUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.search_channels = search_channels 
        if nonsearch_channels != '':
            req.nonsearch_channels = nonsearch_channels 
        #req.nonsearch_channels = nonsearch_channels 
        req.outside_discount = outside_discount 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.campaign_platform)




if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3328400
    search_channels = [1,2,4]
    nonsearch_channels = []
    outside_discount = 110 
    result = SimbaCampaignPlatformUpdate.update_campaign_platform(nick, campaign_id, search_channels, nonsearch_channels, outside_discount )
    print result
