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
from time import sleep
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    #logging.config.fileConfig('conf/consolelogger.conf')
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')
    
from tao_models.common.exceptions import  TaoApiMaxRetryException 
from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from TaobaoSdk.Request.SimbaKeywordRankingforecastGetRequest import SimbaKeywordRankingforecastGetRequest
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordRankingforecastGet(object):

    @classmethod
    @tao_api_exception(6)
    def get_rankingforecast(cls,keyword_id,nick=None):
        """词预估"""
        req = SimbaKeywordRankingforecastGetRequest()
        req.keyword_ids = keyword_id
        if nick:
            req.nick= nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.keyword_ranking_forecast)

if __name__ =="__main__":
    nick = "晓迎"
    keyword_id = 67010196936 
    nick = '麦苗科技001'
    keyword_id = 78483460285 
    price = 10
    rsp = SimbaKeywordRankingforecastGet.get_rankingforecast(keyword_id,nick)
    print len(rsp[0]['prices'])
    for key  in rsp:
        print key
