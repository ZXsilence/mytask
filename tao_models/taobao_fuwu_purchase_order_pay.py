#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yeyuqiu
@contact: yeyuqiu@maimiaotech.com
@date: 2017-08-14 15:47
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

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

from TaobaoSdk import FuwuPurchaseOrderPayRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from api_server.conf.settings import APP_SETTINGS

logger = logging.getLogger(__name__)


class FuwuPurchaseOrderPay(object):

    @classmethod
    @tao_api_exception()
    def pay_fuwu_purchase_order(cls, nick, soft_code='SYB', **kwargs):
        req = FuwuPurchaseOrderPayRequest()
        req.appkey = APP_SETTINGS[soft_code]['app_key']
        for k, v in kwargs.iteritems():
            setattr(req, k, v)
        rsp = ApiService.execute(req, nick, soft_code, False)
        return change_obj_to_dict_deeply(rsp.url)


if __name__ == "__main__":
    nick = '麦苗科技001'
    print FuwuPurchaseOrderPay.pay_fuwu_purchase_order(nick, order_id=311147624140117)

