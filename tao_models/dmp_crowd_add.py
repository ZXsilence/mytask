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

from TaobaoSdk import DmpCrowdAddRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class DmpCrowdAdd(object):

    @classmethod
    def add_dmp_crowd(cls, nick, crowd_name, selects, looklike=1, soft_code = 'YZB'):
        req = DmpCrowdAddRequest()
        req.crowd_name = crowd_name
        #req.valid_date = '2018-0
        req.selects = selects 
        req.lookalike_multiple = looklike
        rsp = ApiService.execute(req,nick,soft_code)
        return  change_obj_to_dict_deeply(rsp.result)

if __name__ == '__main__':
    nick = '优美妮旗舰店'
    crowd_name = "我的测试"
    selects = [{'tag_id':111160, 'option_group_id':1296, 'values':'50016682'}, \
                       {'tag_id':113122, 'option_group_id':11519, 'values':'1'}]
    try_list = DmpCrowdAdd.add_dmp_crowd(nick, crowd_name, selects)
    print try_list
