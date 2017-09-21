#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yeyuqiu
@contact: yeyuqiu@maimiaotech.com
@date: 2017-08-14 11:09
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

from TaobaoSdk import FuwuSkuGetRequest
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from api_server.conf.settings import APP_SETTINGS

logger = logging.getLogger(__name__)


class FuwuSkuGet(object):

    @classmethod
    @tao_api_exception()
    def get_fuwu_sku(cls, article_code, nick, soft_code='SYB'):
        req = FuwuSkuGetRequest()
        req.article_code = article_code
        req.nick = nick
        req.appKey = APP_SETTINGS[soft_code]['app_key']
        rsp = ApiService.execute(req, nick, soft_code, False)
        return change_obj_to_dict_deeply(rsp.result)


if __name__ == "__main__":
    article_code = 'FW_GOODS-1000495518'
    nick = '麦苗科技001'
    print FuwuSkuGet.get_fuwu_sku(article_code, nick)
