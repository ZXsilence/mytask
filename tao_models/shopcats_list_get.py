#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2013-08-01 17:28
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
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import ShopcatsListGetRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException
from tao_models.common.decorator import  tao_api_exception
from tao_models.conf import settings as tao_model_settings

logger = logging.getLogger(__name__)

class ShopcatsListGet(object):

    @classmethod
    @tao_api_exception(3)
    def get_shopcats_list(cls):
        req=ShopcatsListGetRequest()
        req.fields="cid,parent_cid,name,is_parent"
        rsp = tao_model_settings.taobao_client.execute(req, '')[0]
        if not rsp.isSuccess():
            print rsp.msg
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.shop_cats


