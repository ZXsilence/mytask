# -*- coding: utf-8 -*-
'''
Created on 2012-11-3

@author: dk
'''
import re
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
from TaobaoSdk.Request.TopatsSimbaCampkeywordbaseGetRequest import TopatsSimbaCampkeywordbaseGetRequest
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException

logger = logging.getLogger(__name__)

class TopatsSimbaCampkeywordbaseGet(object):
    ''
    @classmethod
    @tao_api_exception
    def get_camp_keywordbase_task(cls, nick, campaign_id, time_slot, access_token):
        ''
        req = TopatsSimbaCampkeywordbaseGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.time_slot = time_slot
        req.search_type = 'SEARCH'
        req.source = 'SUMMARY'
        
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            if int(rsp.code) == 700:
                task_id = re.findall('[\d]+', rsp.sub_msg)
                return int(task_id[0])
            else:
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.task.task_id
    
