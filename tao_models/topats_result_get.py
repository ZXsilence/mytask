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
    from tao_models.conf import set_env
    set_env.getEnvReady()
    logging.config.fileConfig('conf/consolelogger.conf')
    
from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception
from TaobaoSdk.Request.TopatsResultGetRequest import TopatsResultGetRequest
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException

logger = logging.getLogger(__name__)

class TopatsResultGet(object):
    ''
    @classmethod
    @tao_api_exception()
    def get_task_result(cls, task_id, access_token):

        req = TopatsResultGetRequest()
        req.task_id = task_id

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.task
