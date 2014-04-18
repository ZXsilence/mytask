# -*- coding: utf-8 -*-
'''
Created on 2012-11-21

@author: dk
'''
import sys
import os
import datetime
import logging
import logging.config
import json
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')
    
from TaobaoSdk import SimbaRptCusteffectGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaRptCusteffectGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_shop_rpt_effect(cls, nick, start_date, end_date):
        logger.debug('get nick:%s cust effect rpt'%nick)
        req = SimbaRptCusteffectGetRequest()
        req.nick = nick
        req.start_time = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        req.source = 'SUMMARY'
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        l = json.loads(rsp.rpt_cust_effect_list.lower())
        if l == {}:
            l = []
        if isinstance(l, dict):
            raise ErrorResponseException(code=l['code'], msg=l['msg'], sub_code=l['sub_code'], sub_msg=l['sub_msg'])
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return change_obj_to_dict_deeply(l)

if __name__ == '__main__':
    nick = 'chinchinstyle'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    print SimbaRptCusteffectGet.get_shop_rpt_effect(nick, start_time, end_time)

