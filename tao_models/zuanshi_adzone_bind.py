# coding=utf8
'''
Created on 2017-5-5

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

from TaobaoSdk import ZuanshiBannerAdgroupAdzoneBindRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply, slice_list
from tao_models.num_tools import change2num
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.date_tools import  split_date

logger = logging.getLogger(__name__)


class ZuanshiAdzoneBind(object):

    @classmethod
    @tao_api_exception()
    def bind_adzone(cls, nick, campaign_id, adgroup_id, adzone_bid_dto_list, soft_code='YZB'):
        req = ZuanshiBannerAdgroupAdzoneBindRequest()
        req.campaign_id = campaign_id
        req.adgroup_id = adgroup_id
        success_adzone_list = []
        failed_adzone_list = []
        for chunk in slice_list(adzone_bid_dto_list, 20):
            # 参数adzone_bid_dto_list最大列表长度：20
            req.adzone_bid_dto_list = chunk
            rsp = ApiService.execute(req, nick, soft_code)
            result = change_obj_to_dict_deeply(rsp.result)
            if result['success']:
                success_adzone_list.extend(chunk)
            else:
                failed_adzone_list.extend(chunk)
        result = {
            'success': False if failed_adzone_list else True,
            'success_list': success_adzone_list,
            'failed_list': failed_adzone_list
        }
        return result


if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    adgroup_id = 217061436
    adzone_bid_dto_list = {
        'adzone_id': '',
        'matrix_price_list': {
            'crowd_id': '',
            'crowd_type': '',
            'price': ''
        }
    }
    result = ZuanshiAdzoneBind.bind_adzone(nick, campaign_id, adgroup_id, adzone_bid_dto_list)
    print result
