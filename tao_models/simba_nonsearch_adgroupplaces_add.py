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

from TaobaoSdk import SimbaNonsearchAdgroupplacesAddRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaNonsearchAdgroupplacesAdd(object):

    PAGE_SIZE = 200

    @classmethod
    def add_nonsearch_adgroupplaces(cls, nick,campaign_id,origin_jsons):
        if not origin_jsons:
            return []
        return_list = []
        req = SimbaNonsearchAdgroupplacesAddRequest()
        req.nick = nick
        req.campaign_id = int(campaign_id)
        adgroup_places_json = []
        for origin_dict in origin_jsons:
            adgroup_place = {}
            adgroup_place['adgroupId'] = origin_dict['adgroup_id']
            adgroup_place['placeId'] = origin_dict['place_id']
            adgroup_places_json.append(adgroup_place)
        req.adgroup_places_json = adgroup_places_json
        while adgroup_places_json:
            sub_list = adgroup_places_json[:cls.PAGE_SIZE]
            adgroup_places_json = adgroup_places_json[cls.PAGE_SIZE:]
            req.adgroup_places_json = sub_list
            rsp = SimbaNonsearchAdgroupplacesAdd._add_sub_adgroup_places(nick,req)
            return_list.extend(rsp.adgroup_place_list)
        return change_obj_to_dict_deeply(return_list)

    @classmethod
    @tao_api_exception(8)
    def _add_sub_adgroup_places(cls, nick,req): 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp


if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3367748
    adgroup_ids = [{'adgroup_id':336844923,'place_id':11},{'adgroup_id':336844923,'place_id':31}]
    print SimbaNonsearchAdgroupplacesAdd.add_nonsearch_adgroupplaces(nick, campaign_id,adgroup_ids)
    

