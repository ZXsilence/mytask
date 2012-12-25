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

from TaobaoSdk import SimbaCampaignPlatformUpdateRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaCampaignPlatformUpdate(object):
    """
    """

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def update_campaign_platform(cls, access_token, nick, campaign_id, search_channels, nonsearch_channels, outside_discount):
        """
        更新一个计划的推广平台设置 
        """

        req = SimbaCampaignPlatformUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.search_channels = search_channels 
        if nonsearch_channels != '':
            req.nonsearch_channels = nonsearch_channels 
        req.outside_discount = outside_discount 

        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            logger.error("update_campaign_channeloptions  error nick [%s] msg [%s] sub_msg [%s]" %(nick
                 , rsp.msg, rsp.sub_msg))
            if "用户无资格投放定向推广" in rsp.sub_msg:
                raise NonsearchNotAllowedException
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.campaign_platform




if __name__ == '__main__':

    access_token = '6201f2547291c68de14fbd5ba958d3d50ZZ3e50adc7f9ca1030924525'
    nick = u'雅鹭萱婚纱批发'
    campaign_id = '7922713'
    search_channels = '1,2,4'
    nonsearch_channels = ''
    outside_discount = 100 
    

    result = SimbaCampaignPlatformUpdate.update_campaign_platform(access_token, nick, campaign_id, search_channels, nonsearch_channels, outside_discount )
    
    print result.toDict()
