#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')
 
from TaobaoSdk import SimbaInsightCatsrelatedwordGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class SimbaInsightCatsrelatedwordGet(object):

    @classmethod
    @tao_api_exception(5)
    def _get_words_catrelatewords(cls, words,nick=None):
        """
        get words catrelatewords 
        """
        req = SimbaInsightCatsrelatedwordGetRequest()
        if nick:
            req.nick = nick
        req.words = words
        req.result_num = 10
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.related_words

    @classmethod
    def get_words_catrelatewords(cls, words_list,nick=None):
        'words_list 应该是小写，简体，半角字符串，而且每个word不应该包含逗号'
        words_str = ','.join(words_list)
        related_words = SimbaInsightCatsrelatedwordGet._get_words_catrelatewords(words_str,nick)
        return change_obj_to_dict_deeply(related_words)

if __name__ == '__main__':
    words = ['mp3', 'mp4播放器', '手机', '减肥茶', 'mp5', '播放器mp4', '手机电池', '电池手机', '新款女装连衣裙笔记本', '你好', 'mp3']
    related_words = SimbaInsightCatsrelatedwordGet.get_words_catrelatewords(words,None)
    for word in related_words:
        print word 
