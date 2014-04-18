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

from TaobaoSdk import ItemGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ItemGet(object):

    @classmethod
    @tao_api_exception()
    def get_cid(cls, num_iid):
        req = ItemGetRequest()
        req.num_iid = num_iid
        req.fields = 'cid'
        rsp = ApiService.execute(req)
        item = change_obj_to_dict_deeply(rsp.item)
        return item['cid']
    
    @classmethod
    @tao_api_exception()
    def get_item_info(cls,num_iid):
        req = ItemGetRequest()
        req.num_iid = num_iid
        req.fields = 'created,num_iid,title,list_time,price,item_img,pic_url,seller_cids'
        rsp = ApiService.execute(req)
        return change_obj_to_dict_deeply(rsp.item)

if __name__ == '__main__':
    num_iid = 15493508084
    print ItemGet.get_cid(num_iid)
    print ItemGet.get_item_info(num_iid)
