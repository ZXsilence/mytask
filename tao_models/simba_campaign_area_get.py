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

from TaobaoSdk import SimbaCampaignAreaGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCampaignAreaGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def get_campaign_area(cls, nick, campaign_id):
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

        req = SimbaCampaignAreaGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.campaign_area)

if __name__ == '__main__':

    nick = 'chinchinstyle'
    campaign_id = 3367690 
    result = SimbaCampaignAreaGet.get_campaign_area(nick, campaign_id)
    print result
