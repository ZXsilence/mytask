#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yeyuqiu
@contact: yeyuqiu@maimiaotech.com
@date: 2017-08-16 09:09
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import logging.config
import simplejson as json
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import FuwuSpBillreordAddRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from api_server.conf.settings import APP_SETTINGS

logger = logging.getLogger(__name__)


class FuwuSpBillreordAdd(object):

    @classmethod
    @tao_api_exception()
    def add_fuwu_sp_billrecord(cls, nick, order_id, out_confirm_id, fee, soft_code='SYB', **kwargs):
        req = FuwuSpBillreordAddRequest()
        param = {
            'start_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 1,
            'nick': nick,
            'appkey': APP_SETTINGS[soft_code]['app_key'],
            'type': 1,
            'order_id': order_id,
            'out_confirm_id': out_confirm_id,
            'fee': fee
        }
        param.update(kwargs)
        req.param_bill_record_d_t_o = json.dumps(param)
        rsp = ApiService.execute(req, nick, soft_code, False)
        return change_obj_to_dict_deeply(rsp.add_result)


if __name__ == "__main__":
    nick = '麦苗科技001'
    # nick = '觅千草'
    print FuwuSpBillreordAdd.add_fuwu_sp_billrecord(nick)

