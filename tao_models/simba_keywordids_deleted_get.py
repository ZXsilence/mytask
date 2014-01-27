#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import SimbaKeywordidsDeletedGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaKeywordidsDeletedGet(object):

    PAGE_SIZE = 1000

    @classmethod
    @tao_api_exception()
    def _get_sub_keywordids_deleted(cls, nick , req):
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp

    @classmethod
    def get_keywordids_deleted(cls, nick, start_time,total_calls=1000):
        keyword_id_list = []
        req = SimbaKeywordidsDeletedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1
        rsp = SimbaKeywordidsDeletedGet._get_sub_keywordids_deleted(nick, req)
        if not rsp.deleted_keyword_ids:
            return keyword_id_list

        keyword_id_list.extend(rsp.deleted_keyword_ids)

        while len(rsp.deleted_keyword_ids) == cls.PAGE_SIZE:
            req.page_no += 1
            if req.page_no== total_calls:
                break
            rsp = SimbaKeywordidsDeletedGet._get_sub_keywordids_deleted(nick, req)
            keyword_id_list.extend(rsp.deleted_keyword_ids)

        return change_obj_to_dict_deeply(keyword_id_list)


def test():
    nick = 'chinchinstyle'
    from datetime import datetime,timedelta
    start_time = datetime.now() - timedelta(days=10)
    print SimbaKeywordidsDeletedGet.get_keywordids_deleted(nick,start_time)

if __name__ == '__main__':
    test()
