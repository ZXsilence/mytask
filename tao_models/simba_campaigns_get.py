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
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaCampaignsGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCampaignsGet(object):

    """
    campaign_format:
    {
	"online_status" : "online",
	"settle_status" : "online",
	"campaign_id" : 7295832,
	"modified_time" : ISODate("2012-06-29T09:18:55Z"),
	"nick" : "密多帮巴",
	"create_time" : ISODate("2012-06-16T22:35:08Z"),
	"title" : "喜宝计划201206290918"
    }

    """
    @classmethod
    @tao_api_exception()
    def get_campaign_list(cls, nick):
        req = SimbaCampaignsGetRequest()
        req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.campaigns)

if __name__ == '__main__':
    campaigns = SimbaCampaignsGet.get_campaign_list('chinchinstyle')
    for campaign in campaigns:
        print campaign
