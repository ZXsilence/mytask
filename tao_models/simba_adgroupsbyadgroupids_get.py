#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config
import copy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaAdgroupsbyadgroupidsGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupsbyadgroupidsGet(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception()
    def get_adgroup_list_by_adgroup_ids(cls, nick, adgroup_id_list):
        origin_id_list = copy.deepcopy(adgroup_id_list)
        req = SimbaAdgroupsbyadgroupidsGetRequest()
        req.nick = nick
        req.page_size = cls.PAGE_SIZE 
        req.page_no = 1
        response_dict = {}
        while adgroup_id_list:
            sub_adgroup_id_list = adgroup_id_list[:cls.PAGE_SIZE]
            adgroup_id_list = adgroup_id_list[cls.PAGE_SIZE:]

            req.adgroup_ids = ",".join([str(k) for k in sub_adgroup_id_list])
            logger.debug("get adgroup info adgroup_length:%s nick:%s"%(len(sub_adgroup_id_list), nick))
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            result_adgroup_list = rsp.adgroups.adgroup_list
            for adgroup_object in result_adgroup_list:
                adgroup_id = adgroup_object.toDict()['adgroup_id']
                response_dict[adgroup_id] = adgroup_object

        adgroup_object_list = [None]*(len(origin_id_list))
        for adgroup_id in origin_id_list:
            index = origin_id_list.index(adgroup_id) 
            if response_dict.has_key(adgroup_id):
               adgroup_object_list[index] = response_dict[adgroup_id] 
        return change_obj_to_dict_deeply(adgroup_object_list)


def test():
    nick = 'chinchinstyle'
    adgroup_ids = [336844923,166881055,11] 
    adgroups = SimbaAdgroupsbyadgroupidsGet.get_adgroup_list_by_adgroup_ids(nick, adgroup_ids)
    for adgroup in adgroups:
        print adgroup


if __name__ == '__main__':
    test()
