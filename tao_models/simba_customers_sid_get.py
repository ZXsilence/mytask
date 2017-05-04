#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yeyuqiu
@contact: yeyuqiu@maimiaotech.com
@date: 2017-04-25
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com
"""

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaCustomersSidGetRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class SimbaCustomersSidGet(object):

    @classmethod
    @tao_api_exception(5)
    def get_customers_sid(cls, nick):
        """
        获取用户是否有创意自定义图片上传权限（默认是获取创意1号模板的）
        """
        req = SimbaCustomersSidGetRequest()
        req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req, nick, soft_code)
        return change_obj_to_dict_deeply(rsp.result)


if __name__ == '__main__':
    nick = '麦苗科技001'
    result = SimbaCustomersSidGet.get_customers_sid(nick)
    print result

