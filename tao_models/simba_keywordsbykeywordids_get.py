#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

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

from TaobaoSdk import SimbaKeywordsbykeywordidsGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordsbykeywordidsGet(object):

    @classmethod
    @tao_api_exception()
    def _sub_get_keyword_list_by_keyword_ids(cls, nick, sub_keyword_id_list):
        req = SimbaKeywordsbykeywordidsGetRequest()
        req.nick = nick
        req.keyword_ids = ",".join([str(k) for k in sub_keyword_id_list])
        logger.debug("get keyword info keyword_id_length:%s, nick:%s"%(len(sub_keyword_id_list), nick))
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.keywords

    @classmethod
    def get_keyword_list_by_keyword_ids(cls, nick, keyword_id_list):
        """
        get keyword list given by keyword ids
        """
        keyword_id_list = copy.deepcopy(keyword_id_list)
        MAX_KEYWORD_IDS = 200 
        total_keyword_list = []
        while keyword_id_list:
            sub_keyword_id_list = keyword_id_list[:MAX_KEYWORD_IDS]
            keyword_id_list = keyword_id_list[MAX_KEYWORD_IDS:]
            sub_keywords = cls._sub_get_keyword_list_by_keyword_ids(nick, sub_keyword_id_list)
            total_keyword_list.extend(sub_keywords)
        return change_obj_to_dict_deeply(total_keyword_list)


def test():
    nick = 'chinchinstyle'
    keyword_ids = [50729824879]
    keywords = SimbaKeywordsbykeywordidsGet.get_keyword_list_by_keyword_ids(nick, keyword_ids)
    for keyword in keywords:
        print keyword

if __name__ == '__main__':
    test()
