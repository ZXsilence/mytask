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
    def get_keywords_split_qscore(cls, nick, adgroup_id, keyword_id_list):
        ret_list = []
        while keyword_id_list:
            ret_list.extend(cls.get_keywords_split_qscore_sub(nick,adgroup_id,keyword_id_list[:20]))
            keyword_id_list = keyword_id_list[20:]
        return ret_list

    @classmethod
    @tao_api_exception()
    def get_keywords_split_qscore_sub(cls,nick,adgroup_id,keyword_id_list):
        bidword_ids = [str(keyword_id) for keyword_id in keyword_id_list]
        req = SimbaKeywordsQscoreSplitGetRequest()
        req.nick = nick
        req.ad_group_id = adgroup_id
        soft_code = None
        req.bidword_ids =  ','.join(bidword_ids)
        rsp = ApiService.execute(req,nick,soft_code)
        if not rsp.result.toDict():
            return []
        if 'result' not in rsp.result.toDict():
            return []
        if type(rsp.result.toDict()['result']) == dict:
            return rsp.result.toDict()['result'].get('word_score_list',{}).get('wordscorelist',[])
        return change_obj_to_dict_deeply(rsp.result).get('result',{}).get('word_score_list',[])

if __name__ == '__main__':
    nick = '北京学海轩图书专营店'
    adgroup_id = 724526392
    keyword_id_list = [364375757308,364375757315]
    res = SimbaKeywordsQscoreSplitGet.get_keywords_split_qscore(nick, adgroup_id, keyword_id_list)
    print res

