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

from TaobaoSdk import ZuanshiAdvertiserRptsDownloadDayGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiRptsDownloadDayGet(object):

    __hierarchy_list = ('campaign','adgroup','creative','target','adzone','targetAdzone')

    @classmethod
    @tao_api_exception()
    def get_rpts_task(cls,nick,start_time,end_time,hierarchy,campaign_model =1,effect_type ='impression',soft_code = 'YZB'):
        #钻展广告主分时数据异步下载接口，一次只能下载一天数据
        req = ZuanshiAdvertiserRptsDownloadDayGetRequest()
        req.start_time = start_time .strftime('%Y-%m-%d')
        req.end_time = end_time.strftime('%Y-%m-%d')
        if hierarchy not in cls.__hierarchy_list:
            raise Exception('下载任务类型不对,类型hierarchy必须是:%s中的一种' % cls.__hierarchy_list)
        req.hierarchy = hierarchy
        req.campaign_model = campaign_model 
        req.effect_type = effect_type
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result)

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    start_time = datetime.datetime(2017,4,20)
    end_time = datetime.datetime(2017,4,25)
    hierarchy = 'campaign'
    try_list = ZuanshiRptsDownloadDayGet.get_rpts_task(nick,start_time,end_time,hierarchy)
    print try_list
