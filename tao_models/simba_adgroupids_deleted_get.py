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
    set_api_source('normal_test')

from TaobaoSdk import SimbaAdgroupidsDeletedGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class SimbaAdgroupidsDeletedGet(object):

    PAGE_SIZE = 1000

    @classmethod
    @tao_api_exception()
    def _get_sub_adgroupids_deleted(cls, nick, req):
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp

    @classmethod
    def get_adgroupids_deleted(cls, nick, start_time):
        adgroup_id_list = []
        req = SimbaAdgroupidsDeletedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1
        rsp = SimbaAdgroupidsDeletedGet._get_sub_adgroupids_deleted(nick, req)
        if not rsp.deleted_adgroup_ids:
            return adgroup_id_list
        adgroup_id_list.extend(rsp.deleted_adgroup_ids)
        while len(rsp.deleted_adgroup_ids) == cls.PAGE_SIZE:
            req.page_no += 1
            rsp = SimbaAdgroupidsDeletedGet._get_sub_adgroupids_deleted(nick, req)
            adgroup_id_list.extend(rsp.deleted_adgroup_ids)
        return change_obj_to_dict_deeply(adgroup_id_list)


def test():
    nick = '麦苗科技001'
    from datetime import datetime,timedelta
    curr_time = datetime.now()
    start_time = curr_time - timedelta(days=20)
    SimbaAdgroupidsDeletedGet.PAGE_SIZE = 200
    adgroup_id_list = SimbaAdgroupidsDeletedGet.get_adgroupids_deleted(nick,start_time)
    print adgroup_id_list

if __name__ == '__main__':
    test()
