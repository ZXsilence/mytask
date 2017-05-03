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

from TaobaoSdk import ZuanshiAdvertiserCampaignRptsDayGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiCampaignRptsDayGet(object):

    @classmethod
    @tao_api_exception()
    def get_campaign_rpts_day(cls, nick,campaign_id,start_time,end_time,effect = 15,campaign_model = 1,effect_type ='click',soft_code = 'YZB'):
        req = ZuanshiAdvertiserCampaignRptsDayGetRequest()
        req.start_time = start_time.strftime('%Y-%m-%d')
        req.end_time = end_time.strftime('%Y-%m-%d')
        req.campaign_id = campaign_id
        req.effect = effect
        req.effect_type = effect_type
        if campaign_model:
            req.campaign_model = campaign_model
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.campaign_offline_rpt_days_list)

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    start_time = datetime.datetime(2017,5,3)
    end_time = datetime.datetime(2017,5,3)
    campaign_id = 217411616
    try_list = ZuanshiCampaignRptsDayGet.get_campaign_rpts_day(nick,campaign_id,start_time,end_time)
    print try_list[0]
        
