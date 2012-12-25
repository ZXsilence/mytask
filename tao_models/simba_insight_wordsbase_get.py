#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')
 
from TaobaoSdk import SimbaInsightWordsbaseGetRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import taobao_client
from tao_models.common.decorator import  tao_api_exception

class SimbaInsightWordsbaseGet(object):

    @classmethod
    @tao_api_exception(5)
    def get_words_base(cls, access_token, nick, time, words):
        """
        get words base 
        """
        req = SimbaInsightWordsbaseGetRequest()
        req.nick = nick
        req.time = time
        req.words = words
        req.filter = 'PV|CLICK|AVGCPC|COMPETITION'

        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        print 'success .....'
        return rsp.in_word_bases

if __name__ == '__main__':
    access_token = "620260146ZZc0465e1b4185f7b4ca8ba1c7736c28d1c675871727117"
    nick = '牙齿天天晒'
    word_info_list = SimbaInsightWordsbaseGet.get_words_base(access_token, nick, '3MONTH', '登山鞋,冲锋衣,登山包,户外鞋,徒步鞋')
    print 'word_info_list', word_info_list
    for word_info in word_info_list:
        print  word_info.word
        for x in word_info.in_record_base_list:
            print x.date, x.pv

