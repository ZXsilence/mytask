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

    @classmethod
    @tao_api_exception()
    def get_shop_item(cls,nick,item_name,soft_code = 'YZB'):
        req = ZuanshiShopItemFindRequest()
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        req.item_name = item_name
        rsp = ApiService.execute(req,nick,soft_code)
        import pdb; pdb.set_trace()  # XXX BREAKPOINT
        return change_obj_to_dict_deeply(rsp.result).get('items')

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    name = '新品'
    try_list = ZuanshiShopItemFind.get_shop_item(nick,name)
    print try_list
