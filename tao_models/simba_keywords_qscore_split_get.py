#! /usr/bin/env python
#! coding: utf-8
# author = 'zjb'

import sys
import os
import  copy
import logging
import logging.config


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import SimbaKeywordsQscoreSplitGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordsQscoreSplitGet(object):

    @classmethod
    @tao_api_exception()
    def get_keywords_split_qscore(cls, nick, adgroup_id, keyword_id_list):
        bidword_ids = [str(keyword_id) for keyword_id in keyword_id_list]
        req = SimbaKeywordsQscoreSplitGetRequest()
        req.nick = nick
        req.ad_group_id = adgroup_id
        req.bidword_ids = ','.join(bidword_ids)
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        if not rsp.result.word_score_list:
            return []
        return change_obj_to_dict_deeply(rsp.result.word_score_list)

if __name__ == '__main__':
    nick = '思锐旗舰'
    adgroup_id = 452452590
    keyword_id_list = [230569335610]
    print SimbaKeywordsQscoreSplitGet.get_keywords_split_qscore(nick, adgroup_id, keyword_id_list)

