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
 
from TaobaoSdk import SimbaInsightCatstopwordGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

class SimbaInsightCatstopwordGet(object):

    @classmethod
    @tao_api_exception(5)
    def _get_cats_topwords(cls, access_token, nick, category_ids):
        """
        get words catrelatewords 
        """
        req = SimbaInsightCatstopwordGetRequest()
        req.category_ids = category_ids 
        req.result_num = 100

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.top_words

    @classmethod
    def get_cats_topwords(cls, access_token, nick, cats_list):
        cats_str = ','.join(cats_list)
        top_words = SimbaInsightCatstopwordGet._get_cats_topwords(access_token, nick, cats_str)

        return top_words 

if __name__ == '__main__':
    access_token = '620260146ZZc0465e1b4185f7b4ca8ba1c7736c28d1c675871727117' 
    top_words = SimbaInsightCatstopwordGet.get_cats_topwords(access_token, '', ['1512'])

    for word in top_words:
        print word 
