#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2016-06-17 13:13
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import copy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaKeywordsRealtimeRankingBatchGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
import simplejson as json


class SimbaKeywordsRealtimeRankingBatchGet(object):
    
    @classmethod
    def get_keywords_rank(cls,nick,adgroup_id,keyword_ids):
        res = []
        while keyword_ids:
            res.extend(cls._get_keywords_rank_sub(nick,adgroup_id,keyword_ids[:20]))
            keyword_ids=keyword_ids[20:]
        return res

    @classmethod
    @tao_api_exception(5)
    def _get_keywords_rank_sub(cls,nick,adgroup_id,keyword_ids):
        req = SimbaKeywordsRealtimeRankingBatchGetRequest()
        req.nick = nick
        req.ad_group_id = adgroup_id
        req.bidword_ids = ','.join([str(d) for d in keyword_ids]) 
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        res = change_obj_to_dict_deeply(rsp.result)
        return res.get('realtime_rank_list',[])



if __name__ == '__main__':
    nick = "麦苗科技001"
    adgroup_id = 693290415 
    #keyword_ids = [255805868242,255805868243,255805868246]
    #keyword_ids = [274468785611,274468785581,274468785614,274468785545]
    keyword_ids = [276642644500,276642644499,276642644498,276642644496,276642644495,276642644493,276642644492,276642644491,276642644490,276642644489,\
                   276642644488,276642644487,276642644486,276642644485,276642644484,276642644483,276642644482,276642644479,276642644478,276642644477,276642644475,\
                  276642644474]
    res = SimbaKeywordsRealtimeRankingBatchGet.get_keywords_rank(nick,adgroup_id,keyword_ids)
    print len(res)

