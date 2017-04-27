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

from TaobaoSdk import ZuanshiAdvertiserTargetAdzoneRptsTotalGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiTargetAdzoneRptsTotalGet(object):

    page_size  = 3
    __params = ('target_id','adgroup_id','campaign_id','adzone_id','offset','effect','effect_type')

    @classmethod
    def get_rpts_total_list(cls, nick,start_time,end_time,effect =15,effect_type='click',soft_code = 'YZB' ,**kwargs):
        data_list = []
        page_num = 1
        while True:
            tmp_list = cls.__get_sub_data_list(nick,start_time,end_time,effect =effect,effect_type=effect_type,soft_code = soft_code,offset = page_num,**kwargs)
            if tmp_list:
                data_list.extend(tmp_list)
            if not tmp_list or len(tmp_list) < cls.page_size:
                break;
            page_num +=1
        return data_list

    @classmethod
    @tao_api_exception()
    def __get_sub_data_list(cls, nick,start_time,end_time,effect =15,effect_type='click',soft_code = 'YZB',offset = 1 ,**kwargs):
        #获取推广组列表
        req = ZuanshiAdvertiserTargetAdzoneRptsTotalGetRequest()
        for k,v in kwargs.iteritems():
            if k not in cls.__params:
                raise Exception('不支持该参数,参数名:%s,值:%s,仅支持%s' %(k,v,cls.__params))
            if v is not None:
                setattr(req,k,v)
        req.start_time = start_time.strftime('%Y-%m-%d')
        req.end_time = end_time.strftime('%Y-%m-%d')
        req.effect = effect
        req.effect_type = effect_type
        req.offset = (offset -1) * cls.page_size
        req.page_size = cls.page_size
        rsp = ApiService.execute(req,nick,soft_code)
        print len(change_obj_to_dict_deeply(rsp.target_adzone_offline_rpt_total_list))
        #abc = set(['%(adgroup_id)s_%(campaign_id)s_%(adzone_id)s_%(target_id)s' %(obj) for obj in change_obj_to_dict_deeply(rsp.target_adzone_offline_rpt_total_list)])
        return change_obj_to_dict_deeply(rsp.target_adzone_offline_rpt_total_list)

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    start_time = datetime.datetime(2017,4,1)
    end_time = datetime.datetime(2017,4,24)
    try_list = ZuanshiTargetAdzoneRptsTotalGet.get_rpts_total_list(nick,start_time,end_time)
    abc = set(['%(adgroup_id)s_%(campaign_id)s_%(adzone_id)s_%(target_id)s' %(obj) for obj in try_list])
    print len(abc)
    print len(try_list)
    #for obj in try_list:
    #    print obj
