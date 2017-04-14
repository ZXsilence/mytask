#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yeyuqiu
@contact: yeyuqiu@maimiaotech.com
@date: 2017-04-13 15:31
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""
import sys
import os

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import PictureGetRequest
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply


class PictureGet(object):

    @classmethod
    def get_picture(cls, nick, kwargs_dict):
        req = PictureGetRequest()
        for key, value in kwargs_dict.items():
            setattr(req, key, value)
        soft_code = None
        rsp = ApiService.execute(req, nick, soft_code, cache=False)
        return rsp.totalResults, change_obj_to_dict_deeply(rsp.pictures)


if __name__ == '__main__':
    nick = '麦苗科技001'
    param_dict = {
        'urls': 'https://img.alicdn.com/bao/uploaded/i1/871727117/TB2acLMlmFjpuFjSszhXXaBuVXa_!!871727117.jpg'
    }
    data = PictureGet.get_picture(nick, param_dict)
    print data
