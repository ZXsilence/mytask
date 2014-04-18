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

from TaobaoSdk import SimbaAdgroupNonsearchpricesUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupNonsearchpricesUpdate(object):

    PAGESIZE = 200

    @classmethod
    @tao_api_exception(1)
    def set_adgroups_nonsearchprices(cls,nick,campaign_id,adgroupid_price_json):
        if not adgroupid_price_json:
            return []
        return_list = []
        size = cls.PAGESIZE
        page_num = len(adgroupid_price_json)/size+ 1
        if len(adgroupid_price_json) % size== 0:
            page_num -= 1
        for i in range(page_num):
            sub_json_list= adgroupid_price_json[i*size: (i+1)*size]
            adgroup_list = SimbaAdgroupNonsearchpricesUpdate.sub_set_adgroups_nonsearchprices(nick,campaign_id,sub_json_list)
            return_list.extend(adgroup_list)
        return change_obj_to_dict_deeply(return_list)


    @classmethod
    @tao_api_exception(10)
    def sub_set_adgroups_nonsearchprices(cls,nick,campaign_id,adgroupid_price_json):
        req = SimbaAdgroupNonsearchpricesUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.adgroupid_price_json = adgroupid_price_json
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.adgroup_list

if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3367748
    change_list = [{'adgroupId':335469824,'nonsearchMaxPrice':31,'isNonsearchDefaultPrice':'false'}]
    print SimbaAdgroupNonsearchpricesUpdate.set_adgroups_nonsearchprices(nick,campaign_id,change_list)

