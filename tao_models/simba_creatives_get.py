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

from TaobaoSdk import SimbaCreativesGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaCreativesGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(50)
    def get_creative_list_by_adgroup(cls, nick, adgroup_id):
        creative_list = []
        req = SimbaCreativesGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        #req.creative_ids = ",".join([str(k) for k in creative_ids])
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.creatives)

    @classmethod
    @tao_api_exception(5)
    def get_creative_list_by_creative_ids(cls, nick, creative_ids):
        """
        given a adgroup_id, get the creative list in this adgroup
        """
        creative_list = []
        req = SimbaCreativesGetRequest()
        req.nick = nick
        #req.adgroup_id = adgroup_id
        req.creative_ids = ",".join([str(k) for k in creative_ids])
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.creatives)


if __name__ == '__main__':
    nick = 'chinchinstyle'
    #adgroup_id = 345679857
    #creatives = SimbaCreativesGet.get_creative_list_by_adgroup(nick, adgroup_id)
    creative_id = 373504976
    creatives = SimbaCreativesGet.get_creative_list_by_creative_ids(nick, [creative_id])
    for creative in creatives:
        print creative
