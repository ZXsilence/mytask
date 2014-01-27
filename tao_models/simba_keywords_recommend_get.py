#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

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
    set_api_source('api_test')

from TaobaoSdk import SimbaKeywordsRecommendGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordsRecommendGet(object):

    @classmethod
    @tao_api_exception()
    def __get_keywords_recommend_by_adgroup(cls, nick, adgroup_id, page_no):

        req = SimbaKeywordsRecommendGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.page_size = 200
        req.page_no = page_no 
        req.order_by = 'relevance'
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.recommend_words.recommend_word_list
    
    @classmethod
    @tao_api_exception()
    def get_keywords_recommend_by_adgroup(cls, nick, adgroup_id):
        page_no = 1
        keywords_recommend = []
        while True:
            sub_keywords_recommend = SimbaKeywordsRecommendGet.__get_keywords_recommend_by_adgroup(nick, adgroup_id, page_no)
            keywords_recommend.extend(sub_keywords_recommend)
            if len(sub_keywords_recommend) <= 100:
                break
            page_no += 1
        return change_obj_to_dict_deeply(keywords_recommend)

def test():
    nick = 'chinchinstyle'
    adgroup_id = 336844923
    keyword_list = SimbaKeywordsRecommendGet.get_keywords_recommend_by_adgroup(nick, adgroup_id)
    for keyword in keyword_list:
        print keyword['word']

if __name__ == '__main__':
    test()
