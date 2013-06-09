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

from TaobaoSdk import SimbaCampaignAreaGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaCampaignAreaGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def get_campaign_area(cls, access_token, nick, campaign_id):
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

        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.campaign_area




if __name__ == '__main__':

    nick = 'chinchinstyle'
    access_token = '6201616c8a94a43419fef76dfh8bbba34c4f2ec3ffadb3b520500325'
    campaign_id = 3367690 

    result = SimbaCampaignAreaGet.get_campaign_area(access_token, nick, campaign_id)
    
    print result.toDict()
