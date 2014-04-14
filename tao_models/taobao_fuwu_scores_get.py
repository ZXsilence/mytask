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

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

import datetime as dt
from datetime import datetime
from TaobaoSdk.Exceptions import  ErrorResponseException
from TaobaoSdk import FuwuScoresGetRequest 
from tao_models.common.decorator import  tao_api_exception
from tao_models.conf import settings as tao_model_settings

logger = logging.getLogger(__name__)

class FuwuScoresGet(object):
    """应用评价"""
    PAGE_SIZE = 100

    @classmethod
    @tao_api_exception(3)
    def get_fuwu_scores(cls,date_time,page_no = 1):
        """获取指定页的评价"""
        req = FuwuScoresGetRequest()
        req.current_page = page_no
        req.date = date_time
        req.page_size = cls.PAGE_SIZE

        rsp = tao_model_settings.taobao_client.execute(req)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.score_result

    @classmethod
    def get_all_fuwu_scores(cls,date_time):
        """获取所有评价"""
        page_no = 1
        data_list = []
        flag = True
        while flag:
            page_data = cls.get_fuwu_scores(date_time,page_no)
            if not page_data or len(page_data) < cls.PAGE_SIZE:
                flag = False
            page_no += 1
            if page_data:
                data_list.extend(page_data)
        return data_list

            
if __name__ == "__main__":
    d = datetime.combine(datetime.today(),dt.time()) - dt.timedelta()
    access_token = "6201e122dc63b096b076ZZ15b1b1b1c0a32376a01712b6d871727117"
    access_token = "62010003ZZd392c50512638480e7abf1b4edb1e796f26c2111919429"
    print d
    d ="2014-04-04"
    data_list =FuwuScoresGet.get_fuwu_scores(d)
    data_list = FuwuScoresGet.get_all_fuwu_scores(d)
    print len(data_list)
