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
    #from xuanciw.settings import  trigger_envReady
    #logging.config.fileConfig('../xuanciw/consolelogger.conf')
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import SimbaInsightWordsanalysisGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)

class SimbaInsightWordsanalysisGet(object):
    """
    TODO
    """

    @classmethod
    @tao_api_exception()
    def get_word_analysis(cls, access_token, nick, keywords, stu='hprice'):
        """
        keywords 最多200个词
        不是每个词都返回竞价分布
        """
        req = SimbaInsightWordsanalysisGetRequest()
        req.stu = stu
        req.words = ",".join(keywords)

        rsp = taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.in_word_analyses



def test():
    sid = 62847885
    nick = 'chinchinstyle'
    access_token = "620002172c52321823fe0ff9880b1ZZ1cdd4d2c33aa6e9f520500325"
    keyword_list = ['三角形围巾蓝色丝巾真丝', '减肥药']
    word_analysis = SimbaInsightWordsanalysisGet.get_word_analysis(access_token, nick, keyword_list)
    for word in word_analysis:
        #for k in word.toDict():
        #    print k, word.toDict()[k]
        print word.word, word.toDict()

if __name__ == '__main__':
    test()
