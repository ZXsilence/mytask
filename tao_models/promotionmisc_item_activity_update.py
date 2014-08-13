#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import PromotionmiscItemActivityUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class PromotionmiscItemActivityUpdate(object):

    PAGE_SIZE = 200

    @classmethod
    @tao_api_exception(5)
    def update_item_activity(cls, nick,activity_id,name,participate_range,start_time,end_time,decrease_amount,discount_rate,soft_code = 'SYB'):
        req = PromotionmiscItemActivityUpdateRequest()
        req.activity_id = activity_id 
        req.name = name 
        req.participate_range = participate_range
        req.start_time = start_time
        req.end_time = end_time
        if decrease_amount:
            req.is_decrease_money = 'true'
            req.decrease_amount = decrease_amount
        if discount_rate:
            req.is_discount = 'true'
            req.discount_rate = discount_rate

        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.isSuccess()

    @classmethod
    @tao_api_exception(5)
    def close_item_activity(cls, nick,activity_id,name,participate_range,start_time,end_time):
        req = PromotionmiscItemActivityUpdateRequest()
        req.activity_id = activity_id 
        req.name = name 
        req.participate_range = participate_range
        req.start_time = start_time
        req.end_time = end_time

        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.isSuccess()

if __name__ == '__main__':
    nick = '麦苗科技001'
    activity_id =398760013
    name = '7月巨惠满减'
    participate_range = 1
    start_time = '2014-07-21 14:50:00'
    end_time = '2014-08-21 14:50:00'
    decrease_amount = None
    discount_rate = 800

    result = PromotionmiscItemActivityUpdate.update_item_activity(nick,activity_id,name,participate_range,start_time,end_time,decrease_amount,discount_rate)

    print result
