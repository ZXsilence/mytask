#! /usr/bin/env python
#! coding: utf-8
# author = 'zjb'

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

from TaobaoSdk import SimbaKeywordsQscoreSplitGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordsQscoreSplitGet(object):

    @classmethod
    def get_keywords_split_qscore(cls, nick, adgroup_id, keyword_id_list):
        ret_list = []
        while keyword_id_list:
            ret_list.extend(cls.get_keywords_split_qscore_sub(nick,adgroup_id,keyword_id_list[:20]))
            keyword_id_list = keyword_id_list[20:]
        return ret_list

    @classmethod
    @tao_api_exception()
    def get_keywords_split_qscore_sub(cls,nick,adgroup_id,keyword_id_list):
        bidword_ids = [str(keyword_id) for keyword_id in keyword_id_list]
        req = SimbaKeywordsQscoreSplitGetRequest()
        req.nick = nick
        req.ad_group_id = adgroup_id
        soft_code = None
        req.bidword_ids =  ','.join(bidword_ids)
        rsp = ApiService.execute(req,nick,soft_code)
        if not rsp.result.toDict():
            return []
        return rsp.result.toDict()['result']['word_score_list']['wordscorelist']

if __name__ == '__main__':
    nick = 'joeycharm'
    adgroup_id = 704182438 
    keyword_id_list = [2,231139213535,231361936129,231361936130,231361936132,231361936133,231361936134,231361936137,231361936138,231361936139,231361936140,231361936141,231531546019,231531546020,231531546022,231531546023,231531546028,231531546031,231531546032,231531546033,231531546035,231531546036,231531546039,231531546044,231531546045,231531546046,231531546047,231531546049,231531546050,231652841950,231652841953,231652841954,231652841958,231652841959,231652841960,231652841961,231652841962,231652841967,232103412112,232477162488]
    keyword_id_list = [289324570051,289324570050]
    for i in range(1):
        try:
            res = SimbaKeywordsQscoreSplitGet.get_keywords_split_qscore(nick, adgroup_id, keyword_id_list)
            print res
        except Exception:
            print "call error"

