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

from TaobaoSdk import ZuanshiAdvertiserTargetAdzoneRtrptsGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num,change2num2
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiTargetAdzoneRtRptsGet(object):

    @classmethod
    @tao_api_exception()
    def get_target_adzone_rt_rpts(cls, nick,rpt_date,campaign_id,adgroup_id,target_id,adzone_id ,soft_code = 'YZB'):
        req = ZuanshiAdvertiserTargetAdzoneRtrptsGetRequest()
        req.log_date = rpt_date.strftime('%Y-%m-%d')
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id 
        req.target_id = target_id
        req.adzone_id = adzone_id
        rsp = ApiService.execute(req,nick,soft_code)
        return change2num2(change_obj_to_dict_deeply(rsp.target_adzone_realtime_rpt_list),True)

if __name__ == '__main__':
    nick = '飞利浦润氏专卖店'
    rpt_date = datetime.datetime(2017,4,23)
    campaign_id = 217069448
    adgroup_id = 217061436
    target_id = 34492608
    adzone_id = 34492608
    try_list = ZuanshiTargetAdzoneRtRptsGet.get_target_adzone_rt_rpts(nick,rpt_date,campaign_id,adgroup_id,target_id,adzone_id)
    print len(try_list)
        
