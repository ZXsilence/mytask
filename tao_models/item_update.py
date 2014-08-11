#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-15


import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ItemUpdateRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ItemUpdate(object):

    @classmethod
    @tao_api_exception()
    def update_item_desc(cls,nick,num_iid,desc):
        req = ItemUpdateRequest()
        req.num_iid = num_iid
        req.desc = desc
        rsp = ApiService.execute(req,nick)
        return change_obj_to_dict_deeply(rsp.item)

if __name__ == '__main__':
    nick = '麦苗科技001'
    num_iid = 39120249291 
    desc = '天天waegwae'
    ItemUpdate.update_item_desc(nick,num_iid,desc)
