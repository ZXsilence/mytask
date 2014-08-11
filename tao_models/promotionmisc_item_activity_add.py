#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-07-17 17:32
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import json
import datetime
import logging

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import PromotionmiscItemActivityAddRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class PromotionmiscItemActivityAdd(object):
    
    PAGE_SIZE = 50

    @classmethod
    @tao_api_exception(10)
    def add_promotionm_item_activity(cls,nick,name,participate_range,start_time,end_time,decrease_amount,discount_rate):
        req = PromotionmiscItemActivityAddRequest() 
        req.name = name
        req.participate_range = participate_range
        req.start_time = start_time
        req.end_time = end_time 
        if discount_rate:
            req.is_discount = 'true'
            req.discount_rate = discount_rate
        elif decrease_amount:
            req.is_decrease_money = 'true'
            req.decrease_amount = decrease_amount
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.activity_id

if __name__ == "__main__":
    nick = "麦苗科技001"
    name = '新品上市'
    participate_range = 1
    start_time = '2014-07-23 00:00:00'
    end_time = '2014-09-23 00:00:00'
    decrease_amount = None
    discount_rate = 900
    activity_id = PromotionmiscItemActivityAdd.add_promotionm_item_activity(nick,name,participate_range,start_time,end_time,decrease_amount,discount_rate)
    print activity_id 
