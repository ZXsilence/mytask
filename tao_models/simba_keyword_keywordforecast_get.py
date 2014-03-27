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
    #logging.config.fileConfig('conf/consolelogger.conf')
    
from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from tao_models.common.exceptions import  TBDataNotReadyException
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException
from TaobaoSdk.Request.SimbaKeywordKeywordforecastGetRequest import SimbaKeywordKeywordforecastGetRequest

logger = logging.getLogger(__name__)

class SimbaKeywordKeywordforecastGet(object):
    ''
    @classmethod
    @tao_api_exception()
    def get_keywordforecast(cls,keyword_id,bidword_price,access_token,nick=None):
        """词预估"""
        req = SimbaKeywordKeywordforecastGetRequest()
        req.keyword_id = keyword_id
        req.bidword_price = bidword_price
        if nick:
            req.nick= nick
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp.keyword_forecast.toDict()

if __name__ =="__main__":
    tao_model_settings.set_taobao_client('21065688','74aecdce10af604343e942a324641891')
    keyword_id = 54849998072
    price = 230 
    access_token = "62018175fd80b11fb03e28afdfh7feb0d829efc228b5a93871727117"
    keyword_id = 55108934651
    #keyword_id = 53203700147
    price = 270
    #access_token = "620200488562ZZ4711a5a8f32852f2b81bfcc1954015c7e816221524"
    #nick ="康诺宜家家居旗舰店"
    nick = "栾氏茶业"
    rsp = SimbaKeywordKeywordforecastGet.get_keywordforecast(keyword_id,price,access_token,nick)
    for key ,v in rsp.iteritems():
        print key,v
