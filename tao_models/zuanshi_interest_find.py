# coding=utf8
'''
Created on 2017-05-08
@author: yeyuqiu
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

from TaobaoSdk import ZuanshiBannerInterestFindRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)


class ZuanshiInterestFind(object):

    __params = ('nickname', 'item_ids', 'keyword')

    @classmethod
    @tao_api_exception()
    def get_interest_list(cls, nick, soft_code ='YZB', **kwargs):
        req = ZuanshiBannerInterestFindRequest()
        for k, v in kwargs.iteritems():
            if k not in cls.__params:
                raise Exception('不支持该参数,参数名:%s,值:%s,仅支持%s' %(k,v,cls.__params))
            if v is not None:
                if k == 'item_ids':
                    v = ','.join(map(str, v))
                setattr(req, k, v)
        rsp = ApiService.execute(req, nick, soft_code)
        interests = change_obj_to_dict_deeply(rsp.result).get('interests', {}).get('interest_d_t_o', [])
        return interests


if __name__ == '__main__':
    nick = '优美妮旗舰店'
    params_dict = {
        'nickname': '优美妮旗舰店'
    }
    interests = ZuanshiInterestFind.get_interest_list(nick, **params_dict)
    print interests
