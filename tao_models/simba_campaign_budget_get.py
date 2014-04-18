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

from TaobaoSdk import SimbaCampaignBudgetGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCampaignBudgetGet(object):

    @classmethod
    @tao_api_exception(5)
    def campaign_budget_get(cls, nick, campaign_id):
        req = SimbaCampaignBudgetGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        #if not rsp.isSuccess():
        #    if rsp.sub_msg and "未找到指定客户" in rsp.sub_msg:
        #        raise CampaignIdNotBelongToUserException 
        #    raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return change_obj_to_dict_deeply(rsp.campaign_budget)

if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3328400
    campaign_budget = SimbaCampaignBudgetGet.campaign_budget_get(nick, campaign_id)
    print campaign_budget
