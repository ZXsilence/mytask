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

from TaobaoSdk import SimbaCampaignBudgetGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception
from tao_models.exceptions import CampaignIdNotBelongToUserException


logger = logging.getLogger(__name__)


class SimbaCampaignBudgetGet(object):

    @classmethod
    @tao_api_exception(5)
    def campaign_budget_get(cls, access_token, nick, campaign_id):
        req = SimbaCampaignBudgetGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id 
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            if "未找到指定客户" in rsp.sub_msg:
                raise CampaignIdNotBelongToUserException 
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.campaign_budget

if __name__ == '__main__':
    access_token = '6201c01b4ZZdb18b1773873390fe3ff66d1a285add9c10c520500325'
    nick = 'chinchinstyle'
    campaign_id = '3328400'
    campaign_budget = SimbaCampaignBudgetGet.campaign_budget_get(access_token, nick, campaign_id)

    print campaign_budget.toDict()
