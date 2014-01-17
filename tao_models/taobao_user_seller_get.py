#=utf8
__author__ = "xieguanfu"

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import UserSellerGetRequest  
from tao_models.common.decorator import  tao_api_exception
from tao_models.services.api_service import ApiService
from tao_models.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class UserSellerGet(object):

    @classmethod
    @tao_api_exception()
    def get_user_seller(cls, nick,fields=None):
        req=UserSellerGetRequest()
        if fields is not None:
            req.fields=fields
        else:
            req.fields="user_id,nick,sex,seller_credit,type,has_more_pic,item_img_num,item_img_size,prop_img_num,prop_img_size,auto_repost,promoted_type,status,alipay_bind,consumer_protection,avatar,liangpin,sign_food_seller_promise,has_shop,is_lightning_consignment,has_sub_stock,is_golden_seller,vip_info,magazine_subscribe,vertical_market,online_gaming"
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.user)
   
if __name__=="__main__":
    nick = 'chinchinstyle'
    user=UserSellerGet.get_user_seller(nick)
    print user
