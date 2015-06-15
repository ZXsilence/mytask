#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging
import logging.config
import json
import datetime
from copy import deepcopy


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaRtrptCustGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from tao_models.num_tools import change2num, KEYS_RT

logger = logging.getLogger(__name__)

class SimbaRtRptCustGet(object):

    @classmethod
    @tao_api_exception()
    def get_cust_rt_rpt(cls, nick, the_date):
        """
        获取账户实时报表
        """
        req = SimbaRtrptCustGetRequest()
        req.nick = nick
        req.the_date = datetime.datetime.strftime(the_date, '%Y-%m-%d')
        
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        l = rsp.results
        if not l:
            return {}
        
        cust_rpt = change2num(change_obj_to_dict_deeply(l))[0]
        for key in KEYS_RT:
            if not cust_rpt.has_key(key):
                cust_rpt[key] = 0
        cust_rpt['impressions'] = cust_rpt['impression']
        return cust_rpt
    
        
if __name__ == '__main__':
    nick = sys.argv[1]
    the_date = datetime.datetime.now()
    try_list = SimbaRtRptCustGet.get_cust_rt_rpt(nick, the_date)
    print try_list
        
