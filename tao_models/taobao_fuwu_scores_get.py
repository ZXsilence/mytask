#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2013-09-23 14:09
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import logging
import logging.config
import datetime as dt
from datetime import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import FuwuScoresGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class FuwuScoresGet(object):
    """应用评价"""

    @classmethod
    @tao_api_exception(1)
    def get_fuwu_scores(cls,date_time,soft_code):
        result_list = []
        req = FuwuScoresGetRequest()
        req.current_page =1
        req.date = date_time
        req.page_size = 100
        while (True):
            sub_list = FuwuScoresGet.sub_get_fuwu_scores(req,soft_code)
            result_list.extend(sub_list)
            if len(sub_list) <100:
                break
        return change_obj_to_dict_deeply(result_list)

    @classmethod
    @tao_api_exception(3)
    def sub_get_fuwu_scores(cls,req,soft_code):
        nick = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.score_result

if __name__ == "__main__":
    d = datetime.combine(datetime.today(),dt.time()) - dt.timedelta(3)
    soft_code = 'SYB'
    print FuwuScoresGet.get_fuwu_scores(d,soft_code)

