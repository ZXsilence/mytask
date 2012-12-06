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
    logging.config.fileConfig('conf/consolelogger.conf')
    
from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import  TBDataNotReadyException
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException
from TaobaoSdk.Request.SimbaRptCustbaseGetRequest import SimbaRptCustbaseGetRequest

logger = logging.getLogger(__name__)

class SimbaRptCustbaseGet(object):
    ''
    @classmethod
    @tao_api_exception()
    def get_shop_rpt_base(cls, nick, start_date, end_date, access_token, subway_token):
        ''
        logger.debug('get nick:%s cust base rpt'%nick)
        req = SimbaRptCustbaseGetRequest()
        req.nick = nick
        req.start_time = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        req.end_time = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        req.source = 'SUMMARY'
        req.subway_token = subway_token
        
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        l = json.loads(rsp.rpt_cust_base_list)
        return l