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

from TaobaoSdk import ZuanshiAdvertiserAccountRtrptsGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiAdzoneRtRptsGet(object):

    @classmethod
    @tao_api_exception()
    def get_account_rt_rpts(cls, nick,rpt_date,campaign_model =1,soft_code = 'YZB'):
        req = ZuanshiAdvertiserAccountRtrptsGetRequest()
        req.log_date = rpt_date.strftime('%Y-%m-%d')
        req.campaign_model = campaign_model
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.advertiser_realtime_rpt_list)

if __name__ == '__main__':
    nick = '飞利浦润氏专卖店'
    rpt_date = datetime.datetime(2017,4,23)
    campaign_id = 217069448
    adgroup_id = 217061436
    adzone_id = 34492608
    try_list = ZuanshiAdzoneRtRptsGet.get_account_rt_rpts(nick,rpt_date)
    print len(try_list)
        
