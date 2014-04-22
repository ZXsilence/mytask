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

from TaobaoSdk import SimbaCampaignScheduleUpdateRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaCampaignScheduleUpdate(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def update_campaign_schedule(cls, access_token, nick, campaign_id,schedule):
        """

        """

        req = SimbaCampaignScheduleUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.schedule = schedule

        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.campaign_schedule




if __name__ == '__main__':

    nick = '麦苗科技001'
    access_token = '6202108d1d8cf9e2ZZ253366904ba8dfe57f094b3bd6ae4871727117'
    campaign_id = 9329401
    campaign_id = 9843625
    schedule ='00:00-07:30:100,07:30-14:30:40,14:30-24:00:100;00:00-24:00:100;00:00-24:00:100;00:00-24:00:100;00:00-07:30:100,07:30-14:00:200,14:00-24:00:100;00:00-07:30:100,07:30-14:00:200,14:00-24:00:100;00:00-24:00:100' 
    result = SimbaCampaignScheduleUpdate.update_campaign_schedule(access_token, nick, campaign_id,schedule)
    print result.toDict()
    
