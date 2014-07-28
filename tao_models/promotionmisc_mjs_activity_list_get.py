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

from TaobaoSdk import PromotionmiscMjsActivityListGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class PromotionmiscMjsActivityListGet(object):
    
    PAGE_SIZE = 50

    @classmethod
    @tao_api_exception(10)
    def _get_promotion_list(cls, nick,page_no,type):
        req = PromotionmiscMjsActivityListGetRequest() 
        req.activity_type  = type
        req.page_no = page_no
        req.page_size = cls.PAGE_SIZE
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        if not rsp.isSuccess():
            raise ErrorResponseException(code=l['code'], msg=l['msg'], sub_code=l['sub_code'], sub_msg=l['sub_msg'])
        return change_obj_to_dict_deeply(rsp.mjs_promotion_list)

    @classmethod
    def _get_promotion_list_by_type(cls,nick,type):
        data = []
        page_no = 1
        while True:
            l = PromotionmiscMjsActivityListGet._get_promotion_list(nick,page_no,type)
            data.extend(l)
            if len(l) < cls.PAGE_SIZE:
                break
        return change_obj_to_dict_deeply(data)

    @classmethod
    def get_mjs_promotion_list(cls,nick,type = 'all'):
        if type == 'all':
            data = []
            item_promotion_list = cls._get_promotion_list_by_type(nick,1)
            shop_promotion_list = cls._get_promotion_list_by_type(nick,2)
            data.extend(shop_promotion_list)
            data.extend(item_promotion_list)
            return  data
        else:
            return cls._get_promotion_list_by_type(nick,1)

if __name__ == "__main__":
    nick = "麦苗科技001"
    activity_list = PromotionmiscMjsActivityListGet.get_mjs_promotion_list(nick)
    print len(activity_list)
