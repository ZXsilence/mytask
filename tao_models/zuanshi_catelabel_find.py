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

from TaobaoSdk import ZuanshiBannerCatelabelFindRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)

class ZuanshiCatelabelFind(object):

    @classmethod
    @tao_api_exception()
    def get_catelabel_list(cls, nick,soft_code = 'YZB'):
        req = ZuanshiBannerCatelabelFindRequest()
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result).get('labels',{}).get('cat_label_d_t_o', [])

if __name__ == '__main__':
    nick = '飞利浦官方旗舰店'
    adzone_id =7762129 
    try_list = ZuanshiCatelabelFind.get_catelabel_list(nick)
    print try_list
