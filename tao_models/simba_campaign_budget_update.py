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
    set_api_source('api_test')

from TaobaoSdk import SimbaCampaignBudgetUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class SimbaCampaignBudgetUpdate(object):

    @classmethod
    @tao_api_exception()
    def campaign_budget_update(cls, nick, campaign_id, budget, use_smooth):
        req = SimbaCampaignBudgetUpdateRequest()
        req.nick = nick
        req.budget = budget
        req.campaign_id = campaign_id 
        req.use_smooth = use_smooth
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.campaign_budget)

if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3328400
    use_smooth = 'false'
    budget = 42
    campaign_budget = SimbaCampaignBudgetUpdate.campaign_budget_update(nick, campaign_id, budget,use_smooth)
    print campaign_budget
