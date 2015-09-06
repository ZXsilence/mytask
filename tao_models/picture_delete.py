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

from TaobaoSdk import PictureDeleteRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class PictureDelete(object):

    @classmethod
    def delete_img(cls, nick,picture_ids):
        
        req = PictureDeleteRequest()
        if type(picture_ids) == type([]):
            picture_ids = ','.join(str(picture_id) for picture_id in picture_ids)
        req.picture_ids = picture_ids 
        req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.isSuccess()


if __name__ == '__main__':
    picture_ids = [171170108501635074] 
    print PictureDelete.delete_img('麦苗科技001',picture_ids)
