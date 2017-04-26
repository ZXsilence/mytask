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

from TaobaoSdk import ZuanshiAdvertiserAccountRptsDayGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiAccountRptsDayGet(object):

    @classmethod
    @tao_api_exception()
    def get_account_rpts_day(cls, nick,start_time,end_time,effect = 15,campaign_model = 1,effect_type ='click',soft_code = 'YZB'):
        req = ZuanshiAdvertiserAccountRptsDayGetRequest()
        req.start_time = start_time.strftime('%Y-%m-%d')
        req.end_time = end_time.strftime('%Y-%m-%d')
        req.effect = effect
        req.effect_type = effect_type
        if campaign_model:
            req.campaign_model = campaign_model
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.account_offline_rpt_days_list)

if __name__ == '__main__':
    nick = '飞利浦润氏专卖店'
    start_time = datetime.datetime(2017,4,23)
    end_time = datetime.datetime(2017,4,23)
    try_list = ZuanshiAccountRptsDayGet.get_account_rpts_day(nick,start_time,end_time)
    print len(try_list)
        
