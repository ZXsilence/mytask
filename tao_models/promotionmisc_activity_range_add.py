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

from TaobaoSdk import PromotionmiscActivityRangeAddRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class PromotionmiscActivityRangeAdd(object):
    
    PAGE_SIZE = 50

    @classmethod
    @tao_api_exception(12)
    def __add_promotionm_activity_items(cls,nick,activity_id,num_iid_list,soft_code = 'SYB'):
        req = PromotionmiscActivityRangeAddRequest() 
        req.activity_id = activity_id
        req.ids = ','.join(str(num_iid) for num_iid in num_iid_list) 
        rsp = ApiService.execute(req,nick,soft_code)

    @classmethod
    def add_promotionm_activity_items(cls,nick,activity_id,num_iid_list,soft_code = 'SYB'):
        total_pages = (len(num_iid_list) - 1)/cls.PAGE_SIZE + 1
        for page_no in range(total_pages):
            cls.__add_promotionm_activity_items(nick,activity_id,num_iid_list[page_no*cls.PAGE_SIZE:(page_no+1)*cls.PAGE_SIZE],soft_code)

if __name__ == "__main__":
    nick = "麦苗科技001"
    activity_id = 401562069 
    num_iid_list = [21579352934]
    PromotionmiscActivityRangeAdd.add_promotionm_activity_items(nick,activity_id,num_iid_list)
