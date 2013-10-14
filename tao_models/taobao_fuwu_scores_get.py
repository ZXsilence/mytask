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

import datetime as dt
from datetime import datetime
from TaobaoSdk.Exceptions import  ErrorResponseException
from TaobaoSdk import FuwuScoresGetRequest 
from tao_models.common.decorator import  tao_api_exception
from tao_models.conf import settings as tao_model_settings

logger = logging.getLogger(__name__)

class FuwuScoresGet(object):
    """应用评价"""

    @classmethod
    @tao_api_exception(3)
    def get_fuwu_scores(cls,date_time,access_token):
        req = FuwuScoresGetRequest()
        req.current_page =1
        req.date = date_time
        req.page_size = 100

        rsp = tao_model_settings.taobao_client.execute(req,access_token)[0]
        if not rsp.isSuccess():
            print rsp.msg
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp

if __name__ == "__main__":
    d = datetime.combine(datetime.today(),dt.time()) - dt.timedelta(3)
    access_token = "6201e122dc63b096b076ZZ15b1b1b1c0a32376a01712b6d871727117"
    access_token = "62010003ZZd392c50512638480e7abf1b4edb1e796f26c2111919429"
    print d
    rsp =FuwuScoresGet.get_fuwu_scores(d,access_token)
    print rsp
    print dir(rsp)
    print rsp.responseBody
    print rsp.score_result
