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

from TaobaoSdk import ZuanshiRptTaskGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiKeywordRptsDownload(object):

    @classmethod
    @tao_api_exception()
    def get_rpts_task(cls, nick,task_id,soft_code = 'YZB'):
        #钻展报表下载任务状态
        req = ZuanshiRptTaskGetRequest()
        req.task_id = task_id
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.rpt_task)

if __name__ == '__main__':
    nick = '飞利浦官方旗舰店'
    adzone_id =7762129 
    task_id = 6924911 
    try_list = ZuanshiKeywordRptsDownload.get_rpts_task(nick,task_id)
    #6924909
    #6924910
    #6924911
    print try_list
