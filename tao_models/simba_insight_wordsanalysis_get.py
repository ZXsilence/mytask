#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-15

import sys
import os
import  copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaInsightWordsanalysisGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaInsightWordsanalysisGet(object):

    MAX_WORDS = 150

    @classmethod
    @tao_api_exception(1)
    def _get_word_analysis(cls, keywords, stu,nick=None):
        """
        keywords 最多200个词
        不是每个词都返回竞价分布
        """
        req = SimbaInsightWordsanalysisGetRequest()
        req.stu = stu
        req.words = ",".join(keywords)
        if nick:
            req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.in_word_analyses

    @classmethod
    def get_word_analysis(cls, keywords, stu='hprice',nick=None):
        """
        get word analysis 
        """
        word_list = copy.deepcopy(keywords)
        total_list = []
       
        while word_list:
            sub_word_list = word_list[:cls.MAX_WORDS]
            word_list = word_list[cls.MAX_WORDS:]
            sub_list = cls._get_word_analysis(sub_word_list, stu,nick)
            total_list.extend(sub_list)
        return change_obj_to_dict_deeply(total_list)

def test():
    keyword_list = ['三角形围巾', '蓝色丝巾真丝']
    nick = None
    word_analysis = SimbaInsightWordsanalysisGet.get_word_analysis(keyword_list,'hprice',nick)
    for word in word_analysis:
        for k in word:
            print k, word[k]

if __name__ == '__main__':
    test()
