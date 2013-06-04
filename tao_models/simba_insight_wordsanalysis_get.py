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
    sys.path.append('/home/chengk/Webpage/xuancw/')
    from xuanciw.settings import  trigger_envReady
    #logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import SimbaInsightWordsanalysisGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaInsightWordsanalysisGet(object):
    """
    TODO
    """
    MAX_WORDS = 150

    @classmethod
    @tao_api_exception(1)
    def _get_word_analysis(cls, access_token, nick, keywords, stu):
        """
        keywords 最多200个词
        不是每个词都返回竞价分布
        """
        req = SimbaInsightWordsanalysisGetRequest()
        req.stu = stu
        req.words = ",".join(keywords)

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.in_word_analyses

    @classmethod
    def get_word_analysis(cls, access_token, nick, keywords, stu='hprice'):
        """
        get word analysis 
        """
        word_list = copy.deepcopy(keywords)
        total_list = []
       
        while word_list:
            sub_word_list = word_list[:cls.MAX_WORDS]
            word_list = word_list[cls.MAX_WORDS:]
            sub_list = cls._get_word_analysis(access_token, nick, sub_word_list, stu)
            total_list.extend(sub_list)

        return total_list


def test():
    sid = 62847885
    nick = 'chinchinstyle'
    access_token = '6201115889ceaa0cf4e4db3ZZ1918b607ea748deed8ab48520500325'
    subway_token = '1103075437-19809948-1344938925765-c9bd7d79'
    keyword_list = ['三角形围巾', '蓝色丝巾真丝']
    word_analysis = SimbaInsightWordsanalysisGet.get_word_analysis(access_token, nick, keyword_list)
    for word in word_analysis:
        for k in word.toDict():
            print k, word.toDict()[k]

if __name__ == '__main__':
    test()
