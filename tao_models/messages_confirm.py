#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xieguanfu
@contact: xieguanfu@maimiaotech.com
@date: 2016-07-22 13:30
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import os,sys
import logging

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import TmcMessagesConsumeRequest
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num

logger = logging.getLogger(__name__)

class MessagesConfirm(object):

    @classmethod
    @tao_api_exception()
    def cofirm_message(cls,message_ids):
        if not message_ids:return
        req = TmcMessagesConsumeRequest()
        req.s_message_ids= ','.join(str(id) for id in message_ids)
        nick = None
        soft_code = 'SYB'
        rsp = ApiService.execute(req,nick,soft_code)

if __name__ == '__main__':
    ids = [3161701776715387330]
    MessagesConfirm.cofirm_message(ids)
