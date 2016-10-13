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

from TaobaoSdk import ItemSellerGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ItemGet(object):

    @classmethod
    @tao_api_exception()
    def get_cid(cls,nick, num_iid):
        req = ItemSellerGetRequest()
        req.num_iid = num_iid
        req.fields = 'cid'
        rsp = ApiService.execute(req,nick)
        item = change_obj_to_dict_deeply(rsp.item)
        return item['cid']
    
    @classmethod
    @tao_api_exception()
    def get_item_info(cls,nick,num_iid):
        req = ItemSellerGetRequest()
        req.num_iid = num_iid
        req.fields = 'created,num_iid,title,list_time,price,item_img,pic_url,seller_cids,cid,freight_payer,props_name,modified'
        rsp = ApiService.execute(req,nick)
        return change_obj_to_dict_deeply(rsp.item)

if __name__ == '__main__':
    num_iid = 531885253233
    nick = '飞利浦润诚专卖店'
    num_iids = [531885253233]
    print ItemGet.get_cid(nick,num_iid)
    print ItemGet.get_item_info(nick,531885253233)
