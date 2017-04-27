#encoding=utf8
'''
Created on 2012-8-10

@author: dk
'''
import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiShopItemFindRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiShopItemFind(object):

    page_size  = 15
    __params = ('campaign_id','status','name','page_size','adgroup_id_list','page_num')

    @classmethod
    def get_shop_item(cls,nick,item_name = None,soft_code = 'YZB'):
        data_list = []
        page_num = 1
        while True:
            tmp_list = cls.__get_sub_data_list(nick,item_name,page_num,soft_code)
            if tmp_list:
                data_list.extend(tmp_list)
            if not tmp_list or len(tmp_list) < cls.page_size:
                break;
            page_num +=1
            data_list.extend(tmp_list)
        return data_list

    @classmethod
    @tao_api_exception()
    def __get_sub_data_list(cls, nick,item_name = None,page_num=1,soft_code = 'YZB'):
        req = ZuanshiShopItemFindRequest()
        if item_name:
            req.item_name = item_name
        req.page_size = cls.page_size
        req.page_num = page_num
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result).get('items').get('item_d_t_o')

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    item_name = ''
    try_list = ZuanshiShopItemFind.get_shop_item(nick,item_name = item_name)
    print len(try_list)
