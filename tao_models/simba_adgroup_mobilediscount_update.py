#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2015-09-16 15:32
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaAdgroupMobilediscountUpdateRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class SimbaAdgroupMobilediscountUpdate(object):
    @classmethod
    def update_mobile_discount_by_adgroup_ids(cls,nick,adgroup_ids,mobile_discount):
        success_num = 0
        page_num = len(adgroup_ids) / 20 + 1
        for i in range(page_num):
            sub_adgroup_ids = adgroup_ids[i*20:(i+1)*20]
            success_num += cls._update_mobile_discount_by_adgroup_ids(nick,sub_adgroup_ids,mobile_discount)
        return success_num

    @classmethod
    @tao_api_exception()
    def _update_mobile_discount_by_adgroup_ids(cls,nick,adgroup_ids,mobile_discount):
        req=SimbaAdgroupMobilediscountUpdateRequest()
        req.nick = nick
        req.adgroup_ids = ','.join([str(d) for d in adgroup_ids]) 
        req.mobile_discount = mobile_discount
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result)

if __name__ == '__main__':
    nick = '麦苗科技001'
    adgroup_ids = [497893994]
    mobile_discount = 110
    print SimbaAdgroupMobilediscountUpdate.update_mobile_discount_by_adgroup_ids(nick,adgroup_ids,mobile_discount)
