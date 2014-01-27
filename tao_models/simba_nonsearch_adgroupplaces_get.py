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

from TaobaoSdk import SimbaNonsearchAdgroupplacesGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaNonsearchAdgroupplacesGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(3)
    def get_nonsearch_adgroupplaces(cls, nick, campaign_id,adgroup_id_list):
        req = SimbaNonsearchAdgroupplacesGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        adgroup_ids = ','.join([str(adgroup_id) for adgroup_id in adgroup_id_list])
        req.adgroup_ids = adgroup_ids
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        #if not rsp.isSuccess():
        #    logger.debug("get_Adgroupplaces error nick [%s] adgroup_id [%s] msg [%s] sub_msg [%s]" %(nick, 
        #        str(adgroup_ids), rsp.msg, rsp.sub_msg))
        #    if rsp.sub_msg and "当前推广计划不支持该操作" in rsp.sub_msg:
        #        raise NonsearchNotOpenException
        #    raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return change_obj_to_dict_deeply(rsp.adgroup_place_list)

if __name__ == '__main__':

    nick = 'chinchinstyle'
    campaign_id = 3367748
    adgroup_ids = [336844923]
    places_list = SimbaNonsearchAdgroupplacesGet.get_nonsearch_adgroupplaces(nick, campaign_id,adgroup_ids)
    for place in places_list:
        print place

