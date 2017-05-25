#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lichen
@contact: lichen@maimiaotech.com
@date: 2017-05-24 17:52
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
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ZuanshiBannerCreativeModifyRequest
from TaobaoSdk.Domain.multipart import FileItem
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ZuanshiCreativeModify(object):


    @classmethod
    @tao_api_exception
    def modify_creative(cls,nick,params,soft_code='YZB'):
        req = ZuanshiBannerCreativeModifyRequest()
        req.id = params['creative_id']
        req.is_trans_to_wifi = params['is_trans_to_wifi']
        if params.get('name'):
            req.name = params['name']
        if pramas.get('image_path'):
            req.image = FileItem(title,open(image_path))
        if params.get('cat_id'):
            req.cat_id = params['cat_id']
        if params.get('click_url'):
            req.click_url = params['click_url']
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result)
