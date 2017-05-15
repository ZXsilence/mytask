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

from TaobaoSdk import ZuanshiBannerCreativeFindRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiCreativeFind(object):

    page_size  = 200
    __params = ('size_list','campaign_id','adgroup_id','name','creative_level','page_size','audit_status_list','page_num','format_list','online_status')
    number_list_fields = ['audit_status_list', 'format_list']

    @classmethod
    @tao_api_exception()
    def get_paginated_creative_list(cls, nick, soft_code='YZB', **kwargs):
        req = ZuanshiBannerCreativeFindRequest()
        for k, v in kwargs.iteritems():
            if k not in cls.__params:
                raise Exception('不支持该参数,参数名:%s,值:%s,仅支持%s' %(k,v,cls.__params))
            if v is not None:
                if k in cls.number_list_fields:
                    v = ','.join(map(str, v))
                if k == 'size_list':
                    v = ','.join(v)
                setattr(req, k, v)
        rsp = ApiService.execute(req, nick, soft_code)
        result = change_obj_to_dict_deeply(rsp.result)
        total_count = result.get('total_count')
        creative_list = result.get('creatives', {}).get('creative', [])
        return total_count, creative_list

    @classmethod
    def get_creative_list(cls, nick,soft_code ='YZB' ,**kwargs):
        data_list = []
        page_num = 1
        while True:
            tmp_list = cls.__get_sub_data_list(nick,soft_code = soft_code,page_num = page_num,**kwargs)
            if tmp_list:
                data_list.extend(tmp_list)
            if not tmp_list or len(tmp_list) < cls.page_size:
                break;
            page_num +=1
        return data_list

    @classmethod
    @tao_api_exception()
    def __get_sub_data_list(cls, nick,soft_code = 'YZB',**kwargs):
        req = ZuanshiBannerCreativeFindRequest()
        req.page_size = cls.page_size
        for k,v in kwargs.iteritems():
            if k not in cls.__params:
                raise Exception('不支持该参数,参数名:%s,值:%s,仅支持%s' %(k,v,cls.__params))
            if v is not None:
                if k in cls.number_list_fields:
                    v = ','.join(map(str, v))
                if k == 'size_list':
                    v = ','.join(v).replace('x', '*')
                setattr(req,k,v)
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result).get('creatives',{}).get('creative')

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    try_list = ZuanshiCreativeFind.get_creative_list(nick)
    print len(try_list)
    #for obj in try_list:
    #    print obj
