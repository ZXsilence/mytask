#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumc
@contact: liumingchao@maimiaotech.com
@date: 2014-07-10 13:07
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""


if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import TimeGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
import datetime

class TaobaoTimeGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_taobao_time(self):
        req = TimeGetRequest()
        rsp = ApiService.execute(req)
        return rsp.time
        
if __name__ == '__main__':
    print TaobaoTimeGet.get_taobao_time()
