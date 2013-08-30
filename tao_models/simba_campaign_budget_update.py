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
    #logging.config.fileConfig('conf/consolelogger.conf')


from TaobaoSdk import SimbaCampaignBudgetUpdateRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import CampaignBudgetLessThanCostException


logger = logging.getLogger(__name__)


class SimbaCampaignBudgetUpdate(object):

    @classmethod
    @tao_api_exception()
    def campaign_budget_update(cls, access_token, nick, campaign_id, budget, use_smooth):
        req = SimbaCampaignBudgetUpdateRequest()
        req.nick = nick
        req.budget = budget
        req.campaign_id = campaign_id 
        req.use_smooth = use_smooth

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            logger.debug("update budget error nick [%s] campaign_id [%s] msg [%s] sub_msg [%s]" %(nick
                 , str(campaign_id), rsp.msg, rsp.sub_msg))
            if "Invalid arguments:budget"  in rsp.responseBody or (rsp.sub_msg and  "限额不得小于" in rsp.sub_msg):
                raise CampaignBudgetLessThanCostException(msg="ttt",sub_msg="bbb")
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.campaign_budget

if __name__ == '__main__':
    access_token = '6201c01b4ZZdb18b1773873390fe3ff66d1a285add9c10c520500325'
    nick = 'chinchinstyle'
    campaign_id = '3328400'
    campaign_budget = SimbaCampaignBudgetUpdate.campaign_budget_update(access_token, nick, campaign_id, 41, 'false')

    print campaign_budget.toDict()
