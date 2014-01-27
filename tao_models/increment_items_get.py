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
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import IncrementItemsGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply


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
    def _get_items_increment(cls, nick, start_modified, end_modified):
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
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        if not rsp.total_results:
            return notify_item_list

        notify_item_list.extend(rsp.notify_items)

        total_pages = (rsp.total_results + cls.PAGE_SIZE - 1)/cls.PAGE_SIZE

        for curr_page_no  in range(2, total_pages+1):
            req.page_no = curr_page_no
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            notify_item_list.extend(rsp.notify_items)

        return notify_item_list


    @classmethod
    @tao_api_exception()
    def _get_items_increment_count(cls, nick, start_modified, end_modified):

        notify_item_list = []

        req = IncrementItemsGetRequest()
        req.nick = nick
        req.page_size =1
        req.page_no = 1
        if start_modified:
            req.start_modified = start_modified.strftime("%Y-%m-%d %H:%M:%S")
        if end_modified:
            req.end_modified = end_modified.strftime("%Y-%m-%d %H:%M:%S")
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return  rsp.total_results

    @classmethod
    def get_items_incremental_changed(cls, nick, start_time, end_time):
        notify_item_list = []

        time_range = cls._split_time(start_time, end_time)
        for s,e in time_range:
            sub_list = cls._get_items_increment(nick, s, e)
            notify_item_list.extend(sub_list)

        return change_obj_to_dict_deeply(notify_item_list)


    @classmethod
    def get_items_incremental_changed_count(cls, nick, start_time, end_time):
        notify_item_count =0
        time_range = cls._split_time(start_time, end_time)
        for s,e in time_range:
            sub_count = cls._get_items_increment_count(nick, s, e)
            notify_item_count += sub_count
        return change_obj_to_dict_deeply(notify_item_count)


def test_split_time():
    start_time = "2012-08-05 00:01:32"
    end_time = "2012-08-09 12:33:33"
    format = "%Y-%m-%d %H:%M:%S"
    s = datetime.strptime(start_time, format)
    e = datetime.strptime(end_time, format)

    print IncrementItemsGet._split_time(s,e)



def test_get_items_incremental_changed():
    nick = 'chinchinstyle'
    start_time = "2014-01-21 12:40:32"
    end_time = "2014-01-27 14:35:33"
    format = "%Y-%m-%d %H:%M:%S"
    s = datetime.strptime(start_time, format)
    e = datetime.strptime(end_time, format)

    print IncrementItemsGet.get_items_incremental_changed(nick, s, e)
    print IncrementItemsGet.get_items_incremental_changed_count(nick, s, e)

if __name__ == '__main__':
    test_get_items_incremental_changed()
