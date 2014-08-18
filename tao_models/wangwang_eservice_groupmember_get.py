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

from TaobaoSdk import WangwangEserviceGroupmemberGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply 

logger = logging.getLogger(__name__)


class WangwangEserviceGroupmemberGet(object):

    @classmethod
    def get_group_member_list(cls,nick):
        req = WangwangEserviceGroupmemberGetRequest() 
        req.manager_id = 'cntaobao%s' % nick 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.group_member_list)


if __name__ == "__main__":
    nick = "麦苗科技"
    activity_list = WangwangEserviceGroupmemberGet.get_groupmember(nick)
    print activity_list
