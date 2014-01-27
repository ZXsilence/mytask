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

from TaobaoSdk import SimbaAdgroupsChangedGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class SimbaAdgroupsChangedGet(object):
    """
    get adgroups changed since a start_time
    """

    PAGE_SIZE = 1000

    @classmethod
    @tao_api_exception()
    def _get_sub_adgroups_changed(cls, nick, req):
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp


    @classmethod
    def get_adgroups_changed(cls, nick, start_time):
        adgroup_list = []
        req = SimbaAdgroupsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1

        rsp = SimbaAdgroupsChangedGet._get_sub_adgroups_changed(nick, req)

        if not rsp.adgroups.total_item:
            return adgroup_list

        adgroup_list.extend(rsp.adgroups.adgroup_list)

        #continue to call if more than one page
        total_pages = (rsp.adgroups.total_item + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE
        for curr_page_no in range(2, total_pages+1):
            req.page_no = curr_page_no
            rsp = SimbaAdgroupsChangedGet._get_sub_adgroups_changed(nick, req)
            adgroup_list.extend(rsp.adgroups.adgroup_list)

        return change_obj_to_dict_deeply(adgroup_list)



def test():
    nick = 'chinchinstyle'
    from datetime import datetime,timedelta
    curr_time = datetime.now()
    start_time = curr_time - timedelta(days=20)
    SimbaAdgroupsChangedGet.PAGE_SIZE = 30
    adgroup_list = SimbaAdgroupsChangedGet.get_adgroups_changed(nick,start_time)

    for adgroup in adgroup_list:
        print adgroup


if __name__ == '__main__':
    test()
