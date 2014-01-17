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

from TaobaoSdk import SimbaKeywordscatQscoreGetRequest
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordscatQscoreGet(object):

    @classmethod
    @tao_api_exception()
    def get_qscore_list_by_adgroup(cls, nick, adgroup_id):
        """
        get keyword qscore list for some specific adgroup id
        """
        req = SimbaKeywordscatQscoreGetRequest()
        req.nick = nick
        req.adgroup_id = adgroup_id
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.qscore)


def test():
    nick = 'chinchinstyle'
    qscores_dict = SimbaKeywordscatQscoreGet.get_qscore_list_by_adgroup(nick, 336844923)
    print qscores_dict.keys()
    for qscore in qscores_dict['keyword_qscore_list']:
        print qscore


if __name__ == '__main__':
    test()
