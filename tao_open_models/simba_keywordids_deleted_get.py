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

from TaobaoSdk import SimbaKeywordidsDeletedGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from xuanciw.settings import  taobao_client
from common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)


class SimbaKeywordidsDeletedGet(object):
    """
    TODO
    """
    PAGE_SIZE = 1000


    @classmethod
    @tao_api_exception
    def get_keywordids_deleted(cls, access_token, nick, start_time):


        keyword_id_list = []

        req = SimbaKeywordidsDeletedGetRequest()
        req.nick = nick
        req.start_time = start_time
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1

        #first_call
        rsp = taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        if not rsp.deleted_keyword_ids:
            logger.debug("get_keyword_ids deleted ---nick:%s start_time:%s total_deleted_keywords:%s"%(nick,
                                                                                                       start_time,
                                                                                                       len(keyword_id_list)))
            return keyword_id_list

        keyword_id_list.extend(rsp.deleted_keyword_ids)

        while len(rsp.deleted_keyword_ids) == cls.PAGE_SIZE:
            req.page_no += 1
            rsp = taobao_client.execute(req, access_token)[0]

            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)
            keyword_id_list.extend(rsp.deleted_keyword_ids)


        logger.debug("get_keyword_ids deleted ---nick:%s start_time:%s total_deleted_keywords:%s"%(nick,
                                                                                                  start_time,
                                                                                                  len(keyword_id_list)))


        return keyword_id_list




def test():
    access_token = "6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612"
    sid = 71506259
    nick = '密多帮巴'
    start_time = "2012-07-10 00:00:00"
    keyword_id_list = SimbaKeywordidsDeletedGet.get_keywordids_deleted(access_token,nick,start_time)


if __name__ == '__main__':
    test()