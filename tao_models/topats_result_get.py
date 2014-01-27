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
    set_api_source('api_test')
    
from TaobaoSdk.Request.TopatsResultGetRequest import TopatsResultGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class TopatsResultGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_task_result(cls, task_id,soft_code,nick):
        req = TopatsResultGetRequest()
        req.task_id = task_id
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.task)


if __name__ == '__main__':
    nick = 'chinchinstyle'
    soft_code = 'SYB'
    task_id = 215621102
    print TopatsResultGet.get_task_result(task_id,soft_code,nick)
