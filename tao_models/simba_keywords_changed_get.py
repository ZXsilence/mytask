#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'


import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    logging.config.fileConfig('conf/consolelogger.conf')

from TaobaoSdk import  SimbaKeywordsChangedGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception



logger = logging.getLogger(__name__)



class SimbaKeywordsChangedGet(object):
    """
    TODO
    """

    PAGE_SIZE = 1000

    @classmethod
    @tao_api_exception()
    def get_keywords_changed(cls, access_token, nick, start_time):
        """
        注意: start_time 改成datetime 传入
        return format:
        {'keyword_id': 15749079502,
        'modified_time': datetime.datetime(2012, 8, 6, 4, 26, 57),
        'nick': u'\u5bc6\u591a\u5e2e\u5df4'}
        """
        keyword_list = []

        req = SimbaKeywordsChangedGetRequest()
        req.nick = nick
        req.start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        print req.start_time
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1

        #first_call
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        if not rsp.keywords.total_item:
            logger.debug("get_keywords_changed ---nick:%s start_time:%s total_changed_keywords:%s "%(nick,
                                                                                                    start_time,
                                                                                                    rsp.keywords.total_item,
                                                                                                    ))
            return keyword_list

        keyword_list.extend(rsp.keywords.keyword_list)

        #continue to call if more than one page

        total_pages = (rsp.keywords.total_item + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE
        logger.debug("get_keywords_changed ---nick:%s start_time:%s total_changed_keywords:%s total_pages:%s "%(nick,
                                                                                                                start_time,
                                                                                                                rsp.keywords.total_item,
                                                                                                                total_pages
                                                                                                                ))
        for curr_page_no in range(2, total_pages+1):
            req.page_no = curr_page_no
            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

            keyword_list.extend(rsp.keywords.keyword_list)

        return keyword_list


def test():
    access_token = "6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612"
    sid = 71506259
    nick = '密多帮巴'
    start_time = "2012-08-06 03:00:00"
    SimbaKeywordsChangedGet.PAGE_SIZE = 300
    keyword_list = SimbaKeywordsChangedGet.get_keywords_changed(access_token,nick,start_time)

    for keyword in keyword_list:
        print keyword.toDict()



if __name__ == '__main__':
    test()
