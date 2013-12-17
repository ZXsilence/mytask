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

from TaobaoSdk import SimbaAdgroupidsDeletedGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class SimbaAdgroupidsDeletedGet(object):
    """
    get adgroup deleted since a time
    """
    PAGE_SIZE = 1000

    @classmethod
    @tao_api_exception()
    def _get_sub_adgroupids_deleted(cls, access_token, req):
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        return rsp

    @classmethod
    def get_adgroupids_deleted(cls, access_token, nick, start_time):

        adgroup_id_list = []

        req = SimbaAdgroupidsDeletedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1

        #first_call
        #rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        rsp = SimbaAdgroupidsDeletedGet._get_sub_adgroupids_deleted(access_token, req)

        if not rsp.deleted_adgroup_ids:
            logger.debug("get_adgroupids_deleted ---nick:%s start_time:%s total_deleted_adgroups:%s"%(nick,
                                                                                                       start_time,
                                                                                                       0))
            return adgroup_id_list

        adgroup_id_list.extend(rsp.deleted_adgroup_ids)

        while len(rsp.deleted_adgroup_ids) == cls.PAGE_SIZE:
            req.page_no += 1
            #rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            rsp = SimbaAdgroupidsDeletedGet._get_sub_adgroupids_deleted(access_token, req)

            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
            adgroup_id_list.extend(rsp.deleted_adgroup_ids)


        logger.debug("get_adgroupids_deleted ---nick:%s start_time:%s total_deleted_adgroups:%s"%(nick,
                                                                                                  start_time,
                                                                                                  len(adgroup_id_list)))


        return adgroup_id_list


def test():
    access_token = "6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612"
    sid = 71506259
    nick = '密多帮巴'
    start_time = "2012-08-01 00:00:00"
    SimbaAdgroupidsDeletedGet.PAGE_SIZE = 200
    adgroup_id_list = SimbaAdgroupidsDeletedGet.get_adgroupids_deleted(access_token,nick,start_time)

    print adgroup_id_list

if __name__ == '__main__':
    test()
