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

from TaobaoSdk import SimbaNonsearchAdgroupplacesUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaNonsearchAdgroupplacesUpdate(object):

    PAGE_SIZE = 200

    @classmethod
    #@tao_api_exception(3)
    def update_nonsearch_adgroupplaces(cls, nick,campaign_id,origin_jsons):
        if not origin_jsons:
            return []
        adgroup_places_json = []
        for origin_dict in origin_jsons:
            adgroup_place = {}
            adgroup_place['adgroupId'] = origin_dict['adgroup_id']
            adgroup_place['placeId'] = origin_dict['place_id']
            adgroup_place['maxPrice'] = origin_dict['max_price']
            adgroup_place['isDefaultPrice'] = origin_dict['is_defaultprice']
            adgroup_places_json.append(adgroup_place)

        return_list = []
        req = SimbaNonsearchAdgroupplacesUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        while adgroup_places_json:
            sub_list = adgroup_places_json[:cls.PAGE_SIZE]
            adgroup_places_json = adgroup_places_json[cls.PAGE_SIZE:]
            try:
                req.adgroup_places_json = sub_list
                rsp = SimbaNonsearchAdgroupplacesUpdate._update_sub_adgroup_places(nick,req)
            except Exception,e:
                print str(e)+'>>>>>>>'
                continue
            return_list.extend(rsp.adgroup_place_list)
        return change_obj_to_dict_deeply(return_list)

    @classmethod
    @tao_api_exception(8)
    def _update_sub_adgroup_places(cls, nick,req): 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp

if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3367748
    #adgroup_places_json = [{'adgroupId':adgroup_id,'placeId':31,'maxPrice':20,'isDefaultPrice':0}]
    adgroup_places_json = [{'adgroup_id':336844923,'place_id':11,'max_price':20,'is_defaultprice':0}]
    print SimbaNonsearchAdgroupplacesUpdate.update_nonsearch_adgroupplaces(nick,campaign_id,adgroup_places_json)

