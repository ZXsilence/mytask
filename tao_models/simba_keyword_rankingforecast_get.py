#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumc
@contact: liumingchao@maimiaotech.com
@date: 2014-08-20 14:29
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""



import sys
import os
import datetime
import logging
import logging.config
import json
from time import sleep
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')
    #logging.config.fileConfig('conf/consolelogger.conf')
    
from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception
from TaobaoSdk.Request.SimbaKeywordRankingforecastGetRequest import SimbaKeywordRankingforecastGetRequest
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordRankingforecastGet(object):

    @classmethod
    @tao_api_exception(5)
    def get_keyword_rankingforecast(cls,nick,keyword_ids):
        req = SimbaKeywordRankingforecastGetRequest()
        req.nick = nick
        req.keyword_ids = ','.join([ str(k) for k in keyword_ids])  
        #req.keyword_ids = 72160010359 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.keyword_ranking_forecast)



if __name__ == "__main__":
    nick = "牙齿天天晒"
    keyword_ids = [40312259222]
    res = SimbaKeywordRankingforecastGet.get_keyword_rankingforecast(nick ,keyword_ids)
    print len(res[0]["prices"])
    print res[0]["prices"]
