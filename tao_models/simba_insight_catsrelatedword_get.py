#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')
 
from TaobaoSdk import SimbaInsightCatsrelatedwordGetRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

class SimbaInsightCatsrelatedwordGet(object):

    @classmethod
    @tao_api_exception(5)
    def _get_words_catrelatewords(cls, access_token, nick, words):
        """
        get words catrelatewords 
        """
        req = SimbaInsightCatsrelatedwordGetRequest()
        #req.nick = nick
        req.words = words
        req.result_num = 10

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.related_words

    @classmethod
    def get_words_catrelatewords(cls, access_token, nick, words_list):
        'words_list 应该是小写，简体，半角字符串，而且每个word不应该包含逗号'
        words_str = ','.join(words_list)
        related_words = SimbaInsightCatsrelatedwordGet._get_words_catrelatewords(access_token, nick, words_str)

        return related_words 

if __name__ == '__main__':
    access_token = '620260146ZZc0465e1b4185f7b4ca8ba1c7736c28d1c675871727117' 
    related_words = SimbaInsightCatsrelatedwordGet.get_words_catrelatewords(access_token, '', ['mp3', 'mp4播放器', '手机', '减肥茶', 'mp5', '播放器mp4', '手机电池', '电池手机', '新款女装连衣裙笔记本', '你好', 'mp3'])

    for word in related_words:
        print word 
