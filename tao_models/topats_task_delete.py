# -*- coding: utf-8 -*-
'''
Created on 2012-11-3

@author: dk
'''
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
    
from tao_models.common.decorator import  tao_api_exception
from TaobaoSdk.Request.TopatsTaskDeleteRequest import TopatsTaskDeleteRequest
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class TopatsTaskDelete(object):
    ''
    @classmethod
    @tao_api_exception()
    def delete_task(cls, task_id, nick,soft_code):
        req = TopatsTaskDeleteRequest()
        req.task_id = task_id
        rsp = ApiService.execute(req,nick,soft_code)

if __name__ == '__main__':
    task_id = 255749308
    nick = "陈灿龙6898"
    soft_code = 'SYB'
    TopatsTaskDelete.delete_task(task_id,nick,soft_code)
