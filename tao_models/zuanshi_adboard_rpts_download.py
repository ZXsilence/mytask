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

from TaobaoSdk import ZuanshiAdvertiserAdboardRptsDownloadRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiAdboardRptsDownload(object):

    @classmethod
    @tao_api_exception()
    def get_rpts_task(cls, nick,start_date,end_date,rpt_type,soft_code = 'YZB'):
        #创意报表下载,计划类型，1代表展示网络，2代表明星店铺，3代表视频网络 
        req = ZuanshiAdvertiserAdboardRptsDownloadRequest()
        req.rpt_type = rpt_type
        req.start_time= start_date.strftime('%Y-%m-%d')
        req.end_time= end_date.strftime('%Y-%m-%d')
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.task_id

if __name__ == '__main__':
    nick = '飞利浦官方旗舰店'
    start_date = datetime.datetime(2017,3,22)
    end_date = datetime.datetime(2017,4,18)
    rpt_type = 3
    try_list = ZuanshiAdboardRptsDownload.get_rpts_task(nick,start_date,end_date,rpt_type)
    print try_list
