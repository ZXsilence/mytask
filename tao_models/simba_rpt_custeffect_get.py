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
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')
#    logging.config.fileConfig('conf/consolelogger.conf')
    
from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import  TBDataNotReadyException
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException
from TaobaoSdk.Request.SimbaRptCusteffectGetRequest import SimbaRptCusteffectGetRequest

logger = logging.getLogger(__name__)

class SimbaRptCusteffectGet(object):
    ''
    @classmethod
    @tao_api_exception()
    def get_shop_rpt_effect(cls, nick, start_date, end_date, access_token, subway_token):
        ''
        logger.debug('get nick:%s cust effect rpt'%nick)
        req = SimbaRptCusteffectGetRequest()
        req.nick = nick
        req.start_time = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        req.source = 'SUMMARY'
        req.subway_token = subway_token
        
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        l = json.loads(rsp.rpt_cust_effect_list)
        #TODO: 临时处理掉
        if isinstance(l, dict):
            raise ErrorResponseException(code=l['code'], msg=rsp['msg'], sub_code=rsp['sub_code'], sub_msg=rsp['sub_msg'])
        return l

if __name__ == '__main__':
    nick = '大玛旗舰店'
    #sid:69690113
    import datetime as dt
    start_date = '2012-12-25'
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = '2012-12-30' 
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')
    access_token = '620290861d5fd7fbdfcc9cc88d93dbc1ce898ab9ca2aba2520500325'
    subway_token = '1103984138-29938505-1356958423724-caff8f0d'
    l = SimbaRptCusteffectGet.get_shop_rpt_effect(nick, start_date, end_date, access_token, subway_token)
    print l 
    
