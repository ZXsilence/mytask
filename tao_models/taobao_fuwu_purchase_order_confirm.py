#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yeyuqiu
@contact: yeyuqiu@maimiaotech.com
@date: 2017-08-14 14:07
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

from TaobaoSdk import FuwuPurchaseOrderConfirmRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from api_server.conf.settings import APP_SETTINGS

logger = logging.getLogger(__name__)


class FuwuPurchaseOrderConfirm(object):

    @classmethod
    @tao_api_exception()
    def confirm_fuwu_purchase_order(cls, nick, item_code, cyc_unit, cyc_num, soft_code='SYB', **kwargs):
        # kwargs可选参数out_trade_code，device_type，quantity
        req = FuwuPurchaseOrderConfirmRequest()
        params = {
            'app_key': APP_SETTINGS[soft_code]['app_key'],
            'item_code': item_code,
            'cyc_unit': cyc_unit,
            'cyc_num': cyc_num
        }
        params.update(kwargs)
        req.param_order_confirm_query_d_t_o = params
        rsp = ApiService.execute(req, nick, soft_code, False)
        return change_obj_to_dict_deeply(rsp.url)


if __name__ == "__main__":
    nick = '麦苗科技001'
    # 计量型
    # item_code = 'FW_GOODS-1000485359-1'
    # cyc_unit = '2'
    # cyc_num = '12'
    # other = {
    #     'quantity': 3
    # }
    # print FuwuPurchaseOrderConfirm.confirm_fuwu_purchase_order(nick, item_code, cyc_unit, cyc_num, **other)

    # 周期型
    item_code = 'FW_GOODS-1000495518-1'
    cyc_unit = '3'
    cyc_num = '1'
    print FuwuPurchaseOrderConfirm.confirm_fuwu_purchase_order(nick, item_code, cyc_unit, cyc_num)

