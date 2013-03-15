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

from TaobaoSdk import SimbaCampaignScheduleGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaCampaignScheduleGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def get_campaign_schedule(cls, access_token, nick, campaign_id):
        """

        """

        req = SimbaCampaignScheduleGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id

        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.campaign_schedule




if __name__ == '__main__':

    nick = 'chinchinstyle'
    access_token = '6201616c8a94a43419fef76dfh8bbba34c4f2ec3ffadb3b520500325'
    campaign_id = 3367690 

    result = SimbaCampaignScheduleGet.get_campaign_schedule(access_token, nick, campaign_id)
    
    print result.toDict()
