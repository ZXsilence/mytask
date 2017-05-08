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

from TaobaoSdk import ZuanshiBannerAdgroupAdzoneFindpageRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiAdgroupAdzoneFindPage(object):

    page_size  = 50
    __params = ('adzone_id_list','page_size','page_num','adzone_size','adzone_name')

    @classmethod
    def get_adzone_list(cls, nick,campaign_id,adgroup_id,soft_code ='YZB' ,**kwargs):
        data_list = []
        page_num = 1
        while True:
            tmp_list = cls.__get_sub_adgroup_list(nick,campaign_id,adgroup_id,soft_code = soft_code,page_num = page_num,**kwargs)
            if tmp_list:
                data_list.extend(tmp_list)
            if not tmp_list or len(tmp_list) < cls.page_size:
                break;
            page_num +=1
        return data_list 

    @classmethod
    @tao_api_exception()
    def __get_sub_adgroup_list(cls, nick,campaign_id,adgroup_id,soft_code = 'YZB',**kwargs):
        req = ZuanshiBannerAdgroupAdzoneFindpageRequest()
        for k,v in kwargs.iteritems():
            if k not in cls.__params:
                raise Exception('不支持该参数,参数名:%s,值:%s,仅支持%s' %(k,v,cls.__params))
            if v is not None:
                setattr(req,k,v)
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        req.page_size = cls.page_size
        rsp = ApiService.execute(req,nick,soft_code)
        adzone_list = change_obj_to_dict_deeply(rsp.result).get('adzones',{}).get('adzone_bid_d_t_o')
        if adzone_list:
            for adzone in adzone_list:
                adzone['adzone_size_list'] = adzone['adzone_size_list']['string']
                adzone['matrix_price_list'] = adzone['matrix_price_list']['matrix_price_d_t_o']
                adzone['allow_ad_format_list'] = adzone['allow_ad_format_list']['number']
        return adzone_list

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    adgroup_id = 217061436
    try_list = ZuanshiAdgroupAdzoneFindPage.get_adzone_list(nick,campaign_id,adgroup_id)
    print try_list
    #for obj in try_list:
    #    print obj
