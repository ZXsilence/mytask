# coding=utf8
"""
Created on 2017-5-2
@author: yeyuqiu
"""

import sys
import os
import logging.config


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

import json
from TaobaoSdk import ZuanshiBannerAdgroupCreateRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class ZuanshiAdgroupCreate(object):

    __params = ('campaign_id', 'intelligent_bid', 'name', 'crowds', 'adzone_bid_list')

    @classmethod
    @tao_api_exception()
    def create_adgroup(cls, nick, campaign_id, name, crowds, adzone_bid_list, intelligent_bid=1, soft_code='YZB'):
        req = ZuanshiBannerAdgroupCreateRequest()
        req.campaign_id = campaign_id
        req.name = name
        req.crowds = crowds
        req.adzone_bid_list = adzone_bid_list
        req.intelligent_bid = intelligent_bid
        rsp = ApiService.execute(req, nick, soft_code)
        return change_obj_to_dict_deeply(rsp.result)


if __name__ == '__main__':
    nick = '优美妮旗舰店'
    campaign_id = 217069448
    name = '新建推广单元'
    crowds = [
        {
            'crowd_type': 0,
            "crowd_name": "通投",
            "crowd_value": "10",
            "sub_crowds": [
                {
                    "sub_crowd_name": "通投",
                    "sub_crowd_value": "all"
                }
            ],
            'matrix_price': [
                {
                    'adzone_id': 34492608,
                    'price': 50
                }
            ]
        }
    ]
    adzone_bid_list = [
        {
            "adzone_id": 34492608
        }
    ]
    result = ZuanshiAdgroupCreate.create_adgroup(nick, campaign_id, name, crowds, adzone_bid_list)
    print result
