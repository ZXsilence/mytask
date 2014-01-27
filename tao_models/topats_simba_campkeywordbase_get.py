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
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')
    
from TaobaoSdk import TopatsSimbaCampkeywordbaseGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from TaobaoSdk.Exceptions import ErrorResponseException

logger = logging.getLogger(__name__)

class TopatsSimbaCampkeywordbaseGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_camp_keywordbase_task(cls, nick, campaign_id, time_slot, soft_code):
        req = TopatsSimbaCampkeywordbaseGetRequest()
        req.nick = nick
        req.campaign_id = campaign_id
        req.time_slot = time_slot
        req.search_type = 'SEARCH'
        req.source = 'SUMMARY'
        try:
            rsp = ApiService.execute(req,nick,soft_code)
        except ErrorResponseException,e:
            rsp = e.rsp
            if not rsp.isSuccess():
                if int(rsp.code) == 700:
                    task_id = re.findall('[\d]+', rsp.sub_msg)
                    return int(task_id[0])
                else:
                    raise e
        return change_obj_to_dict_deeply(rsp.task.task_id)

if __name__ == '__main__':
    nick = 'chinchinstyle'    
    campaign_id = 3367748
    time_slot = '7DAY'
    soft_code = 'SYB'
    print TopatsSimbaCampkeywordbaseGet.get_camp_keywordbase_task(nick, campaign_id, time_slot, soft_code)

