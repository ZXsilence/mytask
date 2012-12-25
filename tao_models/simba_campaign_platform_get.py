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

from TaobaoSdk import SimbaCampaignPlatformGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaCampaignPlatformGet(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def get_campaign_platform(cls, access_token, nick, campaign_id):
        """
        获得一个计划的推广平台设置 
        """

        req = SimbaCampaignPlatformGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id

        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.campaign_platform




if __name__ == '__main__':

    access_token = '6201f2547291c68de14fbd5ba958d3d50ZZ3e50adc7f9ca1030924525'
    nick = u'雅鹭萱婚纱批发'
    campaign_id = '7922713'
    

    result = SimbaCampaignPlatformGet.get_campaign_platform(access_token, nick, campaign_id)
    
    print result.toDict()
