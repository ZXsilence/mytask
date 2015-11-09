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
        if not rsp.result.word_score_list:
            return []
        return change_obj_to_dict_deeply(rsp.result.word_score_list)

if __name__ == '__main__':
    nick = '小脚丫之恋'
    adgroup_id = 447735828 
    keyword_id_list = [77408410804,98350035770,98827031438,108796389289,108796389291,213523547854,214203613762,214203613773,214470208343,214470208350,215732053928,215732053931,217115911054,217351738692,218469850069,218469850072,220554059003,224113318440,225270919028,225270919030,226532288817,228116925804,229872203296,230023735722,230178046828,230389794385,231139213521,231139213531,231139213532,231139213535,231361936129,231361936130,231361936132,231361936133,231361936134,231361936137,231361936138,231361936139,231361936140,231361936141,231531546019,231531546020,231531546022,231531546023,231531546028,231531546031,231531546032,231531546033,231531546035,231531546036,231531546039,231531546044,231531546045,231531546046,231531546047,231531546049,231531546050,231652841950,231652841953,231652841954,231652841958,231652841959,231652841960,231652841961,231652841962,231652841967,232103412112,232477162488]
    for i in range(20):
        try:
            print len(SimbaKeywordsQscoreSplitGet.get_keywords_split_qscore(nick, adgroup_id, keyword_id_list))
        except Exception:
            print "call error"

