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

from TaobaoSdk import ZuanshiAdzonesGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiAdzonesGet(object):

    @classmethod
    @tao_api_exception()
    def get_adzones(cls, nick,soft_code = 'YZB'):
        req = ZuanshiAdzonesGetRequest()
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.adzone_list)

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    try_list = ZuanshiAdzonesGet.get_adzones(nick)
    for obj in try_list:
        if 'PC' in obj['adzone_name'] and '首页' in obj['adzone_name']:
            print obj['adzone_name']
        #if obj['adzone_name'] in ['PC_流量包_网上购物_淘宝首页焦点图','PC_网上购物_淘宝首页焦点图右侧banner二','PC_流量包_网上购物_天猫首页焦点图']:
        #    print obj['adzone_name'],obj['adzone_id']
        #if obj['adzone_name'] in ['无线_流量包_网上购物_手淘app_手淘焦点图','无线_流量包_网上购物_触摸版_淘宝首页焦点图','无线_网上购物_app_新天猫首页焦点图2','无线_流量包_网上购物_天猫app首页焦点图','无线_网上购物_app_天猫_首页焦点图 ']:
        #    print obj['adzone_name'],obj['adzone_id']
    print try_list[0].keys()
    print len(try_list)
        
