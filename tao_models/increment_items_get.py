#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'



import sys
import os
import logging
import logging.config
from datetime import datetime
import datetime as dt

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import IncrementItemsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)



class IncrementItemsGet(object):

    PAGE_SIZE = 200
    DELAY_SECS = 180  #该API 数据可能存在延迟，所以为保证数据准确性，需要该时间窗


    @classmethod
    def _split_time(cls, start_time, end_time):
        """
        return: [(s1,e1),(s2,e2)...]
        """
        ret = []
        real_start = start_time - dt.timedelta(seconds=cls.DELAY_SECS)

        if real_start.day == end_time.day:
            ret.append((real_start, end_time))
            return ret

        ret.append((real_start,None))
        s = datetime(real_start.year, real_start.month, real_start.day)
        for i in range(end_time.day - 1 - real_start.day):
            start = s + dt.timedelta(days=i+1)
            ret.append((start,None))
        ret.append((None, end_time))

        return ret

    @classmethod
    @tao_api_exception()
    def _get_items_increment(cls, access_token, nick, start_modified, end_modified):
        """
        this method should only be called by get_items_incremental_changed

        format:
        {'status': 'ItemUpdate', 'sku_id': 29253432552, 'changed_fields': 'price,sku', 'price': 216.0, 'num_iid': 16675583313, 'modified': datetime.datetime(2012, 8, 9, 9, 6, 39), 'nick': u'\u5bc6\u591a\u5e2e\u5df4', 'sku_num': 94}
        {'status': 'ItemDelete', 'nick': u'\u5bc6\u591a\u5e2e\u5df4', 'num_iid': 15549542550, 'modified': datetime.datetime(2012, 8, 9, 8, 57, 51)}
        """
        notify_item_list = []

        req = IncrementItemsGetRequest()
        req.nick = nick
        req.page_size = cls.PAGE_SIZE
        if start_modified:
            req.start_modified = start_modified.strftime("%Y-%m-%d %H:%M:%S")

        if end_modified:
            req.end_modified = end_modified.strftime("%Y-%m-%d %H:%M:%S")

        #first call
        req.page_no = 1
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        if not rsp.total_results:
            #logger.debug("IncrementItems no result,  start_modified:%s end_modified:%s nick:%s"%(start_modified.strftime("%Y-%m-%d %H:%M:%S"),
                                                                                                # end_modified.strftime("%Y-%m-%d %H:%M:%S"),
                                                                                               #  nick))
            return notify_item_list

        notify_item_list.extend(rsp.notify_items)

        total_pages = (rsp.total_results + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE

        for curr_page_no  in range(2, total_pages+1):
            req.page_no = curr_page_no
            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

            notify_item_list.extend(rsp.notify_items)

        return notify_item_list


    @classmethod
    def get_items_incremental_changed(cls, access_token, nick, start_time, end_time):
        notify_item_list = []

        time_range = cls._split_time(start_time, end_time)
        for s,e in time_range:
            sub_list = cls._get_items_increment(access_token, nick, s, e)
            notify_item_list.extend(sub_list)

        return notify_item_list




def test_split_time():
    start_time = "2012-08-05 00:01:32"
    end_time = "2012-08-09 12:33:33"
    format = "%Y-%m-%d %H:%M:%S"
    s = datetime.strptime(start_time, format)
    e = datetime.strptime(end_time, format)

    print IncrementItemsGet._split_time(s,e)



def test_get_items_incremental_changed():
    access_token = "6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612"
    sid = 71506259
    nick = '密多帮巴'
    start_time = "2012-08-06 12:40:32"
    end_time = "2012-08-09 14:35:33"
    format = "%Y-%m-%d %H:%M:%S"
    s = datetime.strptime(start_time, format)
    e = datetime.strptime(end_time, format)

    notify_list = IncrementItemsGet.get_items_incremental_changed(access_token, nick, s, e)

    for notify in  notify_list:
        print notify.toDict()


if __name__ == '__main__':
    test_get_items_incremental_changed()