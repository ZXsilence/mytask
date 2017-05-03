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

from TaobaoSdk import DmpCrowdsGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class DmpCrowdsGet(object):

    page_size = 200
    
    @classmethod
    def get_dmp_crowds(cls, nick, soft_code = 'YZB'):
        req = DmpCrowdsGetRequest()
        req.is_query_all = 1
        req.offset = 0
        req.limit = 20 #时间原因，先不分页了
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.results)

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    try_list = DmpCrowdsGet.get_dmp_crowds(nick)
    print try_list
