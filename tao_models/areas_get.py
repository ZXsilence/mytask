#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-07-17 17:32
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import json
import datetime
import logging

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import AreasGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class AreasGet(object):
    
    @classmethod
    @tao_api_exception(10)
    def get_areas(cls):
        req = AreasGetRequest() 
        req.fields="id,type,name,parent_id"
        soft_code = None
        rsp = ApiService.execute(req,None,soft_code)
        return change_obj_to_dict_deeply(rsp.areas)

if __name__ == "__main__":
    areas = AreasGet.get_areas()
    areas = [obj for obj in areas]
    print areas
    #print len(areas)
    #for area in areas:
    #    if area['type'] ==2:
    #        print area['name'],area['id']
