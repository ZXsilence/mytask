#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lichen
@contact: lichen@maimiaotech.com
@date: 2017-05-12 18:56
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import sys
import os
import logging
import logging.config
import json
import datetime



if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiBannerAreaCodeFindRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk.Exceptions import ErrorResponseException


logger = logging.getLogger(__name__)

class ZuanshiAreaCodeFind(object):

    @classmethod
    @tao_api_exception()
    def get_area_info(cls,nick,soft_code = 'YZB'):
        req = ZuanshiBannerAreaCodeFindRequest()
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result).get("area_codes").get("area_code")

if __name__ == "__main__":
    nick = '优美妮旗舰店'
    res = ZuanshiAreaCodeFind.get_area_info(nick)
    for r in res:
        print "{code:%s,name:%s}"%(r['code'], r['name'].encode("utf8"))


