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
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')
    
from TaobaoSdk import SimbaRptCustbaseGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaRptCustbaseGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_shop_rpt_base(cls, nick, start_date, end_date):
        logger.debug('get nick:%s cust base rpt'%nick)
        req = SimbaRptCustbaseGetRequest()
        req.nick = nick
        req.start_time = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        req.source = 'SUMMARY'
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        l = json.loads(rsp.rpt_cust_base_list.lower())
        if l == {}:
            l = []
        if isinstance(l, dict):
            raise ErrorResponseException(code=l['code'], msg=l['msg'], sub_code=l['sub_code'], sub_msg=l['sub_msg'])
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        return change_obj_to_dict_deeply(l)

if __name__ == "__main__":
    nick = 'chinchinstyle'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    print SimbaRptCustbaseGet.get_shop_rpt_base(nick, start_time, end_time)




