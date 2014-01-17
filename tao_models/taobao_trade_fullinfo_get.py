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
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import TradeFullinfoGetRequest 
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class TradeFullinfoGet(object):
    """
    adjust_fee 0.00
    alipay_no 2013041000001000480051109727
    buyer_area 上海上海有线通
    buyer_nick xuxizhen9995
    buyer_obtain_point_fee 0
    buyer_rate False
    can_rate False
    cod_fee 0.00
    cod_status NEW_CREATED
    consign_time 2013-04-11 08:57:44
    created 2013-04-10 23:52:27
    discount_fee 0.00
    has_yfx False
    is_brand_sale False
    is_force_wlb False
    is_lgtype False
    modified 2013-04-11 08:57:44
    num 3
    num_iid 21872504968
    pay_time 2013-04-10 23:54:22
    payment 30.00
    pic_path http://img03.taobaocdn.com/bao/uploaded/i3/10697019085862011/T1wJ3NXXFaXXXXXXXX_!!0-item_pic.jpg
    point_fee 0
    post_fee 0.00
    price 25.00
    real_point_fee 0
    received_payment 0.00
    receiver_city 上海市
    receiver_district 徐汇区
    receiver_state 上海
    receiver_zip 200030
    seller_can_rate False
    seller_email 189285578@qq.com
    seller_flag 0
    seller_mobile 18052525178
    seller_name 王晨樱
    seller_nick 嘴馋了网
    seller_phone 0519-83295178-
    seller_rate False
    shipping_type express
    status WAIT_BUYER_CONFIRM_GOODS
    tid 208981498818570
    title 嘴馋了零食
    total_fee 75.00
    type fixed
    """
    DEFAULT_FIELDS = 'seller_nick, buyer_nick, title, type, created, tid, seller_rate, seller_can_rate, buyer_rate, can_rate, status, payment, discount_fee, adjust_fee, post_fee, total_fee, pay_time, end_time, modified, consign_time, buyer_obtain_point_fee, point_fee, real_point_fee, received_payment, pic_path, num_iid, num, price, cod_fee, cod_status, shipping_type, receiver_state, receiver_city, receiver_district, receiver_zip, seller_flag, alipay_no, is_lgtype, is_force_wlb, is_brand_sale, buyer_area, has_buyer_message, credit_card_fee, lg_aging_type, lg_aging, step_trade_status, step_paid_fee, mark_desc, has_yfx, yfx_fee,yfx_id, yfx_type, trade_source, send_time, seller_mobile, seller_phone, seller_name, seller_email'

    @classmethod
    @tao_api_exception()
    def get_trade_info(cls, nick, tid, fields=DEFAULT_FIELDS):
        """获取单笔交易的详细信息
        1. 只有在交易成功的状态下才能取到交易佣金，其它状态下取到的都是零或空值 
        2. 只有单笔订单的情况下Trade数据结构中才包含商品相关的信息 
        3. 获取到的Order中的payment字段在单笔子订单时包含物流费用，多笔子订单时不包含物流费用 
        4. 请按需获取字段，减少TOP系统的压力 
        5. 通过异步接口taobao.topats.trades.fullinfo.get可以一次性获取多达100笔订单详情"""
        
        req = TradeFullinfoGetRequest()
        req.fields = fields
        req.tid = tid
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.trade)

def test_get_trade():
    nick = 'chinchinstyle'
    tid = 208981498818570
    trade = TradeFullinfoGet.get_trade_info(nick, tid)
    print trade

if __name__ == '__main__':
    test_get_trade()
