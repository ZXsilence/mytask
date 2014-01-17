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

from TaobaoSdk import SimbaAdgroupNonsearchstatesUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupNonsearchstatesUpdate(object):

    PAGESIZE = 200

    @classmethod
    @tao_api_exception(1)
    def set_adgroups_nonsearchstates(cls,nick,campaign_id,adgroupid_nonsearchstate_json):
        if not adgroupid_nonsearchstate_json:
            return []
        return_list = []
        size = cls.PAGESIZE
        page_num = len(adgroupid_nonsearchstate_json)/size+ 1
        if len(adgroupid_nonsearchstate_json) % size== 0:
            page_num -= 1
        for i in range(page_num):
            sub_json_list= adgroupid_nonsearchstate_json[i*size: (i+1)*size]
            adgroup_list = SimbaAdgroupNonsearchstatesUpdate.sub_set_adgroups_nonsearchstates(nick,campaign_id,sub_json_list)
            return_list.extend(adgroup_list)
        return change_obj_to_dict_deeply(return_list)


    @classmethod
    @tao_api_exception(10)
    def sub_set_adgroups_nonsearchstates(cls,nick,campaign_id,adgroupid_nonsearchstate_json):
        req = SimbaAdgroupNonsearchstatesUpdateRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.adgroupid_nonsearchstate_json = adgroupid_nonsearchstate_json
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.adgroup_list

if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3328400
    change_list = [{'adgroupId':346519023,'nonsearchStatus':0}]
    print SimbaAdgroupNonsearchstatesUpdate.set_adgroups_nonsearchstates(nick,campaign_id,change_list)

