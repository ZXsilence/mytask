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

from TaobaoSdk import SimbaCampaignAreaoptionsGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCampaignAreaoptionsGet(object):

    @classmethod
    @tao_api_exception(5)
    def get_campaign_areaoptions(cls):
        req = SimbaCampaignAreaoptionsGetRequest()
        soft_code = None
        nick = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.area_options)


if __name__ == '__main__':

    print SimbaCampaignAreaoptionsGet.get_campaign_areaoptions()

