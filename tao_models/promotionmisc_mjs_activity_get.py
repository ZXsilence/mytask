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

from TaobaoSdk import PromotionmiscMjsActivityGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class PromotionmiscMjsActivityGet(object):
    
    @classmethod
    @tao_api_exception(10)
    def get_promotionm_mjs_activity(cls,nick,activity_id):
        req = PromotionmiscMjsActivityGetRequest() 
        req.activity_id = activity_id
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.mjs_promotion)

if __name__ == "__main__":
    nick = "麦苗科技001"
    activity_id = 400184451
    activity = PromotionmiscMjsActivityGet.get_promotionm_mjs_activity(nick,activity_id)
    print len(activity.keys())
