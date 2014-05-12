#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf.set_env import getEnvReady
    getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaCampaignScheduleUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply


logger = logging.getLogger(__name__)

class SimbaCampaignScheduleUpdate(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def update_campaign_schedule(cls, nick, campaign_id,schedule):
        """

        """
        req = SimbaCampaignScheduleUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.schedule = schedule
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.campaign_schedule)




if __name__ == '__main__':

    nick = '麦苗科技001'
    campaign_id = 9329401
    campaign_id = 9843625
    schedule ='00:00-07:30:100,07:30-14:30:40,14:30-24:00:100;00:00-24:00:100;00:00-24:00:100;00:00-24:00:100;00:00-07:30:100,07:30-14:00:200,14:00-24:00:100;00:00-07:30:100,07:30-14:00:200,14:00-24:00:100;00:00-24:00:100' 
    result = SimbaCampaignScheduleUpdate.update_campaign_schedule(nick, campaign_id,schedule)
    print result
    
