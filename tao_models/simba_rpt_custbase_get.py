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
    
from TaobaoSdk import SimbaRptCustbaseGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaRptCustbaseGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_shop_rpt_base(cls, nick, start_date, end_date,source = 'SUMMARY'):
        logger.debug('get nick:%s cust base rpt'%nick)
        req = SimbaRptCustbaseGetRequest()
        req.nick = nick
        req.start_time = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        req.source = source
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        keys_int  =["click","impressions"]
        keys_float = ["cpm","avgpos","ctr","cost"]
        l = json.loads(rsp.rpt_cust_base_list.lower())
        if l == {}:
            l = []
        for rpt in l:
            rpt['date'] = datetime.datetime.strptime(rpt['date'], '%Y-%m-%d')
        rpt_list  = change_obj_to_dict_deeply(l)
        for item in  rpt_list:
            for key in item.keys():
                if key in keys_int:
                    item[key] = int(item[key])
                elif key in keys_float:
                    item[key] = float(item[key])
        return rpt_list

if __name__ == "__main__":
    nick = '晓迎'
    start_time = datetime.datetime.now() - datetime.timedelta(days=10)
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    start_time = datetime.datetime(2015,1,18)
    end_time = datetime.datetime(2015,2,18)
    list = SimbaRptCustbaseGet.get_shop_rpt_base(nick, start_time, end_time)
    for obj in list:
        print obj




