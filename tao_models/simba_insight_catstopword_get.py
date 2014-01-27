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
 
from TaobaoSdk import SimbaInsightCatstopwordGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class SimbaInsightCatstopwordGet(object):

    @classmethod
    @tao_api_exception(5)
    def _get_cats_topwords(cls, category_ids,nick=None):
        """
        get words catrelatewords 
        """
        req = SimbaInsightCatstopwordGetRequest()
        req.category_ids = category_ids 
        req.result_num = 100
        if nick:
            req.nick = nick
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.top_words

    @classmethod
    def get_cats_topwords(cls, cats_list,nick=None):
        cats_str = ','.join(cats_list)
        top_words = SimbaInsightCatstopwordGet._get_cats_topwords(cats_str,nick)
        return change_obj_to_dict_deeply(top_words)

if __name__ == '__main__':
    top_words = SimbaInsightCatstopwordGet.get_cats_topwords(['1512'],None)
    for word in top_words:
        print word 
