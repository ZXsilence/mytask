#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2015-09-16 15:09
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaKeywordsRealtimeRankingGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class SimbaKeywordsRealtimeRankingGet(object):
    @classmethod
    @tao_api_exception()
    def get_keyword_realtime_ranking(cls,nick,adgroup_id,bid_price,bidword_id):
        req = SimbaKeywordsRealtimeRankingGetRequest()
        req.nick = nick
        req.ad_group_id = adgroup_id
        req.bid_price = bid_price
        req.bidword_id = bidword_id
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.result)

if __name__ == '__main__':
    bid_price_list = [10,20,30,40,50,60,70,80,90]
    nick = '海立信旗舰店'
    adgroup_id =627139286
    bidword_id =230862053372
    for bid_price in bid_price_list:
        print SimbaKeywordsRealtimeRankingGet.get_keyword_realtime_ranking(nick,adgroup_id,bid_price,bidword_id), bid_price
