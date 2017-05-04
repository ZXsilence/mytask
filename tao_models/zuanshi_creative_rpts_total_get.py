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

from TaobaoSdk import ZuanshiAdvertiserCreativeRptsTotalGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiCreativeRptsTotalGet(object):

    page_size = 200

    @classmethod
    def get_creative_rpts_total(cls, nick,sdate,edate,effect = 15,campaign_model= 1,effect_type  = 'click',page_num = 1,campaign_id = None,adgroup_id = None,creative_id = None,soft_code = 'YZB'):
        rpt_list = []
        while True:
            tmp_list = cls.__sub_get_creative_rpts_total(nick,sdate,edate,effect = effect,campaign_model= campaign_model,effect_type  = effect_type,page_num = page_num,campaign_id = campaign_id,adgroup_id = adgroup_id,creative_id=creative_id,soft_code = soft_code)
            if tmp_list:
                rpt_list.extend(tmp_list)
            if not tmp_list or len(tmp_list) < cls.page_size:
                break
            page_num +=1
        return rpt_list

    @classmethod
    @tao_api_exception()
    def __sub_get_creative_rpts_total(cls, nick,sdate,edate,effect = 15,campaign_model= 1,effect_type  = 'click',page_num = 1,campaign_id = None,adgroup_id = None,creative_id = None,soft_code = 'YZB'):
        #campaign_model 1：全店推广；4单品推广
        #effect_type效果类型。“impression”：展现效果；“click”：点击效果
        req = ZuanshiAdvertiserCreativeRptsTotalGetRequest()
        req.start_time = sdate.strftime('%Y-%m-%d')
        req.end_time = edate.strftime('%Y-%m-%d')
        if campaign_id:
            req.campaign_id  = campaign_id
        if adgroup_id:
            req.adgroup_id  = adgroup_id 
        if creative_id :
            req.creative_id  = creative_id 
        req.effect = 15
        req.campaign_model = campaign_model
        req.effect_type = effect_type
        req.page_size = cls.page_size
        req.offset = (page_num - 1)*cls.page_size
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.creative_offline_rpt_total_list)

if __name__ == '__main__':
    nick = '飞利浦润氏专卖店'
    nick = '飞利浦官方旗舰店'
    sdate = datetime.datetime(2017,3,22)
    edate = datetime.datetime(2017,4,18)
    try_list = ZuanshiCreativeRptsTotalGet.get_creative_rpts_total(nick,sdate,edate,effect_type = 'impression')
    for obj in try_list:
        #print obj.keys()
        print obj['campaign_id'],obj['creative_name'],obj['uv'],obj['ad_pv'],obj['ctr'],obj['ecpm'],obj['charge'],obj.get('cvr',0),obj['roi']
