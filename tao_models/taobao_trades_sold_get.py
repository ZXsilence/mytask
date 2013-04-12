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
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import TradesSoldGetRequest 
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception




logger = logging.getLogger(__name__)

class TradesSoldGet(object):

    PAGE_SIZE = 100
    DEFAULT_FIELDS = 'seller_nick, buyer_nick, title, type, created, tid, seller_rate, seller_can_rate, buyer_rate, can_rate, status, payment, discount_fee, adjust_fee, post_fee, total_fee, pay_time, end_time, modified, consign_time, buyer_obtain_point_fee, point_fee, real_point_fee, received_payment, pic_path, num_iid, num, price, cod_fee, cod_status, shipping_type, receiver_state, receiver_city, receiver_district, receiver_zip, seller_flag, alipay_no, is_lgtype, is_force_wlb, is_brand_sale, buyer_area, has_buyer_message, credit_card_fee, lg_aging_type, lg_aging, step_trade_status, step_paid_fee, mark_desc, has_yfx, yfx_fee,yfx_id, yfx_type, trade_source, send_time, seller_phone'

    @classmethod
    @tao_api_exception()
    def get_trades_sold_list(cls, access_token, start_created=None, end_created=None, fields=DEFAULT_FIELDS, flag=False):
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

            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

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

        return total_trade_list



def test_get_trade_list():
    import datetime
    access_token = "6200917df2c6f25102738cd27ZZ8ccc3914d83063c5fd5b925150697"
    start_created_str = "2013-04-10"
    end_created_str = "2013-04-11"
    total_trade_list = TradesSoldGet.get_trades_sold_list(access_token, start_created_str, end_created_str)
    for trade in total_trade_list:
        trade = trade.toDict()
        keys = trade.keys()
        keys.sort()
        for key in keys:
            print key, trade[key]
        break

if __name__ == '__main__':
    test_get_trade_list()
