#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-16

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

from TaobaoSdk import SimbaAdgroupsItemExistRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupsItemExist(object):

    @classmethod
    @tao_api_exception()
    def is_adgroup_item_exist(cls,nick , campaign_id, num_iid):
        req = SimbaAdgroupsItemExistRequest()
        req.campaign_id = campaign_id
        req.item_id = num_iid
        req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.exist)

if __name__ == '__main__':
    nick = 'chinchinstyle'
    campaign_id = 3367748
    #num_iid = 111
    num_iid = 35402689713
    print SimbaAdgroupsItemExist.is_adgroup_item_exist(nick , campaign_id, num_iid)
