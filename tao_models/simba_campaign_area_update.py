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

from TaobaoSdk import SimbaCampaignAreaUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCampaignAreaUpdate(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def update_campaign_area(cls, nick, campaign_id,area):
        """
        Note:如果设置了所有地域，则返回的不是area_id，而是字符串all
        
        目前已知的area_id
        国外:574
        香港:599
        澳门:576
        台湾:578
        西藏自治区:463  子码:464 ~ 470
        新疆维吾尔自治区:471  子码:472,473,476,477,478,479,480,483,484,485,486,602,603,604,625,626

        """

        req =SimbaCampaignAreaUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        if type(area) == type([]):
            req.area = ','.join(str(area_id) for area_id in area) 
        else:
            req.area = area
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.campaign_area)

if __name__ == '__main__':

    nick = 'chinchinstyle'
    campaign_id = 3367690 
    area = 'all'
    area = [532] 
    result = SimbaCampaignAreaUpdate.update_campaign_area(nick, campaign_id,area)
    print result
