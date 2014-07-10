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
    set_api_source('normal_test')

from TaobaoSdk import SimbaKeywordsbykeywordidsGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply
from basic_types.keyword_new import Keyword
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
    
    @classmethod
    def get_keyword_list_by_keyword_ids_new(cls, nick, sid,keyword_id_list):
        keyword_id_list = copy.deepcopy(keyword_id_list)
        MAX_KEYWORD_IDS = 200 
        total_keyword_list = []
        while keyword_id_list:
            sub_keyword_id_list = keyword_id_list[:MAX_KEYWORD_IDS]
            keyword_id_list = keyword_id_list[MAX_KEYWORD_IDS:]
            sub_keywords = cls._sub_get_keyword_list_by_keyword_ids(nick, sub_keyword_id_list)
            for k in sub_keywords:
                k = k.__dict__
                k_obj = Keyword((k['keyword_id'],k['adgroup_id'],k['campaign_id'],sid,nick,k['word'],k['audit_status'],k.get('qscore',5),k.get('rele_score',None),k.get('cvr_score',None),k.get('cust_score',None),k.get('creative_score',None),k.get('match_scope',4),k['max_price'],k['is_default_price'],k['is_garbage'],k['create_time'],k['modified_time']))
                total_keyword_list.append(k_obj)
        return total_keyword_list

def test():
    nick = 'chinchinstyle'
    keyword_ids = [66671648550, 66671648549, 66671648548, 66671648547, 66671648546]
    keywords = SimbaKeywordsbykeywordidsGet.get_keyword_list_by_keyword_ids_new(nick, 123,keyword_ids)
    for keyword in keywords:
        print keyword['keyword_id'],keyword['cvr_score']

if __name__ == '__main__':
    test()
