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

from TaobaoSdk import ZuanshiBannerCrowdFindRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiCrowdFind(object):

    page_size  = 200
    __params = ('campaign_id','status','name','page_size','adgroup_id_list','page_num')

    @classmethod
    def get_crowd_list(cls, nick,campaign_id,adgroup_id,target_id = None,target_types  = None,soft_code ='YZB'):
        data_list = []
        page_num = 1
        while True:
            tmp_list = cls.__get_sub_data_list(nick,campaign_id,adgroup_id,target_id,target_types,page_num,soft_code = soft_code)
            if tmp_list:
                data_list.extend(tmp_list)
            if not tmp_list or len(tmp_list) < cls.page_size:
                break;
            page_num +=1
        return data_list

    @classmethod
    @tao_api_exception()
    def __get_sub_data_list(cls,nick,campaign_id,adgroup_id,target_id,target_types,page_num,soft_code = 'YZB'):
        req = ZuanshiBannerCrowdFindRequest()
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        if target_id:
            req.target_id = target_id
        if target_types:
            req.target_types = ','.join(target_types)
        req.page_size = cls.page_size
        req.page_num = page_num
        rsp = ApiService.execute(req,nick,soft_code)
        crowd_list = change_obj_to_dict_deeply(rsp.result).get('crowds',{}).get('crowd_d_t_o')
        for crowd in crowd_list:
            crowd['sub_crowds'] = crowd['sub_crowds']['sub_crowd_d_t_o']
            crowd['matrix_prices'] = crowd['matrix_prices']['matrix_price_d_t_o']
        return crowd_list

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    adgroup_id = 217061436
    try_list = ZuanshiCrowdFind.get_crowd_list(nick,campaign_id,adgroup_id)
    print try_list
    #for obj in try_list:
    #    print obj
