#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'


import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import SimbaAdgroupsChangedGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)


class SimbaAdgroupsChangedGet(object):
    """
    get adgroups changed since a start_time
    """

    PAGE_SIZE = 1000

    @classmethod
    @tao_api_exception()
    def get_adgroups_changed(cls, access_token, nick, start_time):
        """

        return format:

        """
        adgroup_list = []

        req = SimbaAdgroupsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1

        #first_call
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        if not rsp.adgroups.total_item:
            logger.debug("get_adgroups_changed ---nick:%s start_time:%s total_changed_adgroups:%s "%(nick,
                                                                                                     start_time,
                                                                                                     rsp.adgroups.total_item,
                ))
            return adgroup_list

        adgroup_list.extend(rsp.adgroups.adgroup_list)

        #continue to call if more than one page
        total_pages = (rsp.adgroups.total_item + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE
        logger.debug("get_adgroups_changed ---nick:%s start_time:%s total_changed_adgroups:%s total_pages:%s "%(nick,
                                                                                                                start_time,
                                                                                                                rsp.adgroups.total_item,
                                                                                                                total_pages
            ))
        for curr_page_no in range(2, total_pages+1):
            req.page_no = curr_page_no
            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

            adgroup_list.extend(rsp.adgroups.adgroup_list)

        return adgroup_list



def test():
    access_token = "6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612"
    sid = 71506259
    nick = '密多帮巴'
    start_time = "2012-08-06 03:00:00"
    SimbaAdgroupsChangedGet.PAGE_SIZE = 30
    adgroup_list = SimbaAdgroupsChangedGet.get_adgroups_changed(access_token,nick,start_time)

    for adgroup in adgroup_list:
        print adgroup.toDict()


if __name__ == '__main__':
    test()
