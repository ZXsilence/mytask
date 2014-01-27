#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zhoujiebing
@contact: zhoujiebing@maimiaotech.com
@date: 2013-04-11 15:31
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""
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

from TaobaoSdk import TradesSoldGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class TradesSoldGet(object):

    PAGE_SIZE = 100
    DEFAULT_FIELDS = 'seller_nick, buyer_nick, title, type, created, tid, seller_rate, seller_can_rate, buyer_rate, can_rate, status, payment, discount_fee, adjust_fee, post_fee, total_fee, pay_time, end_time, modified, consign_time, buyer_obtain_point_fee, point_fee, real_point_fee, received_payment, pic_path, num_iid, num, price, cod_fee, cod_status, shipping_type, receiver_state, receiver_city, receiver_district, receiver_zip, seller_flag, alipay_no, is_lgtype, is_force_wlb, is_brand_sale, buyer_area, has_buyer_message, credit_card_fee, lg_aging_type, lg_aging, step_trade_status, step_paid_fee, mark_desc, has_yfx, yfx_fee,yfx_id, yfx_type, trade_source, send_time, seller_phone'

    @classmethod
    @tao_api_exception(3)
    def get_trades_sold_list(cls, nick, start_created=None, end_created=None, fields=DEFAULT_FIELDS, flag=False):
        """搜索当前会话用户作为卖家已卖出的交易数据（只能获取到三个月以内的交易信息）
        1.返回的数据结果是以订单的创建时间倒序排列的。
        2.返回的数据结果只包含了订单的部分数据，可通过taobao.trade.fullinfo.get获取订单详情。
        """
        req = TradesSoldGetRequest()
        req.fields = fields
        req.start_created = start_created
        req.end_created = end_created
        req.page_size = cls.PAGE_SIZE
        req.page_no = 1
        total_trade_list = []
        while True:
            soft_code = None
            rsp = ApiService.execute(req,nick,soft_code)
            if rsp.trades is None:
                logger.info("get trade sold, but none return")
                break 
            logger.info("get trades sold info, actually return: %s"%(len(rsp.trades)))
            total_trade_list.extend(rsp.trades)
            if len(rsp.trades) != req.page_size or req.use_has_next:
                break
            if flag:
                break
            req.page_no += 1
        return change_obj_to_dict_deeply(total_trade_list)

def test_get_trade_list():
    nick = '麦苗科技001'
    start_created_str = "2014-01-01"
    end_created_str = "2014-01-15"
    total_trade_list = TradesSoldGet.get_trades_sold_list(nick, start_created_str, end_created_str)
    for trade in total_trade_list:
        print trade

if __name__ == '__main__':
    test_get_trade_list()
