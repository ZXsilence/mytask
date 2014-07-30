#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-07-17 17:32
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import json
import datetime
import logging

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import PromotionmiscMjsActivityUpdateRequest 
from tao_models.common.decorator import tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)


class PromotionmiscMjsActivityUpdate(object):
    """创建满就送活动,创建时先用MjsPromotionActivityFactory 工厂生成活动详情再请求api最终执行"""


    @classmethod
    @tao_api_exception(12)
    def update_promotionm_mjs_activity(self,nick,req):
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.isSuccess()

    class MjsPromotionActivityFactory(object):
        """变异的匿名工厂方法,进行创建满就送活动.方便引和组装活动"""

        __mjs_promotion_request = None

        @classmethod
        def create_mjs_promotion_update(cls):
            factory = PromotionmiscMjsActivityUpdate.MjsPromotionActivityFactory()
            factory.__mjs_promotion_request = PromotionmiscMjsActivityUpdateRequest()
            return factory

        def add_mjs_base_condition(self,activity_id,name,start_time,end_time,participate_range):
            """添加满就送活动的必须条件"""
            self.__mjs_promotion_request.activity_id = activity_id
            self.__mjs_promotion_request.name = name
            self.__mjs_promotion_request.participate_range = participate_range 
            self.__mjs_promotion_request.type = type 
            self.__mjs_promotion_request.start_time = start_time 
            self.__mjs_promotion_request.end_time = end_time 

        def add_mjs_item_condition(self,item_count,is_item_multiple):
            """添加满就送活动的满件条件"""
            self.__mjs_promotion_request.is_item_count_over = 'true'
            self.__mjs_promotion_request.is_amount_over = 'false'
            self.__mjs_promotion_request.item_count = item_count 
            if is_item_multiple:
                self.__mjs_promotion_request.is_item_multiple = 'true'

        def add_mjs_price_condition(self,total_price,is_amount_multiple):
            """添加满就送活动的满元条件"""
            self.__mjs_promotion_request.is_item_count_over = 'false'
            self.__mjs_promotion_request.is_amount_over = 'true'
            self.__mjs_promotion_request.total_price = total_price 
            if is_amount_multiple:
                self.__mjs_promotion_request.is_amount_multiple = 'true'

        def decrease_money_condition(self,decrease_amount):
            """减钱方式"""
            self.__mjs_promotion_request.is_decrease_mone = 'true' 
            self.__mjs_promotion_request.is_discount  = 'false' 
            self.__mjs_promotion_request.decrease_amount = decrease_amount 

        def decrease_discount_condition(self,discount_rate):
            """打折方式"""
            self.__mjs_promotion_request.is_decrease_mone = 'false' 
            self.__mjs_promotion_request.is_discount  = 'true' 
            self.__mjs_promotion_request.discount_rate = discount_rate 

        def add_gift_condition(self,is_send_gift,gift_name):
            """送礼"""
            if is_send_gift:
                self.__mjs_promotion_request.is_send_gift = 'true'
            self.__mjs_promotion_request.gift_name = gift_name 

        def add_free_post_condition(self,is_free_post,exclude_area):
            """免邮"""
            if is_free_post:
                self.__mjs_promotion_request.is_free_post = 'true'
            if exclude_area:
                self.__mjs_promotion_request.exclude_area = exclude_area

        def build_promotion_request(self):
            return  self.__mjs_promotion_request


if __name__ == "__main__":
    nick = "麦苗科技001"
    name = '新品上市'
    participate_range = 1
    start_time = '2014-07-23 00:00:00'
    end_time = '2014-09-23 00:00:00'
    decrease_amount = None
    discount_rate = 900
    activity_id = 404526601
    factory = PromotionmiscMjsActivityUpdate.MjsPromotionActivityFactory.create_mjs_promotion_update()
    factory.add_mjs_base_condition(activity_id,name,start_time,end_time,1)
    factory.add_mjs_item_condition(1,'true')
    factory.decrease_money_condition(1000)
    factory.add_gift_condition('true','小狗狗')
    req = factory.build_promotion_request()
    print PromotionmiscMjsActivityUpdate.update_promotionm_mjs_activity(nick,req)
