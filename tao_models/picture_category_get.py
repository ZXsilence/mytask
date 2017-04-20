#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zhoujiebing
@contact: zhoujiebing@maimiaotech.com
@date: 2013-04-11 15:31
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""
import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import PictureCategoryGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class PictureCategoryGet(object):

    @classmethod
    def get_picture_category_name(cls, nick, category_name=None, category_id=None, parent_id=-1):
        
        req = PictureCategoryGetRequest()
        if category_name:
            req.picture_category_name = category_name
        if category_id:
            req.picture_category_id = category_id
        req.parent_id = parent_id
        req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code, cache=False)
        return change_obj_to_dict_deeply(rsp.picture_categories)


if __name__ == '__main__':
    nick = '麦苗科技001'
    name = '省油宝创意请勿删除'
    data = PictureCategoryGet.get_picture_category_name(nick,name)
    print data
