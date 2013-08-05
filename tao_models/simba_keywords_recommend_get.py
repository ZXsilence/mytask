#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import  copy
import logging
import logging.config

#if __name__ == '__main__':
#    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
#    from xuanciw.settings import  trigger_envReady
#    logging.config.fileConfig('../xuanciw/consolelogger.conf')

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import ItemsListGetRequest

from TaobaoSdk import SimbaKeywordsRecommendGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception





logger = logging.getLogger(__name__)

class SimbaKeywordsRecommendGet(object):
    """
    """

    @classmethod
    @tao_api_exception()
    def __get_keywords_recommend_by_adgroup(cls, access_token, nick, adgroup_id, page_no):
        """
        """

        req = SimbaKeywordsRecommendGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        req.page_size = 200
        req.page_no = page_no 
        req.order_by = 'relevance'

        logger.debug('get keywords recommend by adgroup_id nick:%s adgroup_id:%s access_token:%s page_no:%d'%(nick, adgroup_id, access_token, page_no))
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.recommend_words.recommend_word_list

    
    @classmethod
    @tao_api_exception()
    def get_keywords_recommend_by_adgroup(cls, access_token, nick, adgroup_id):
        """
        """
        page_no = 1
        keywords_recommend = []
        while True:
            sub_keywords_recommend = SimbaKeywordsRecommendGet.__get_keywords_recommend_by_adgroup(access_token, nick, adgroup_id, page_no)
            keywords_recommend.extend(sub_keywords_recommend)
            if len(sub_keywords_recommend) <= 100:
                break
            page_no += 1

        return keywords_recommend

def test():
    access_token = "6202a15148e3e8130586bbfhj7010db194b655fce05bb5a871727117"
    sid = 101240238 
    #nick = '麦苗科技001'
    #adgroup_id = 230551157
    nick = '蓝天碧游'
    adgroup_id = 232499295 
    keyword_list = SimbaKeywordsRecommendGet.get_keywords_recommend_by_adgroup(access_token, nick, adgroup_id)
    for keyword in keyword_list:
        print keyword.toDict()['word']



if __name__ == '__main__':
    test()
