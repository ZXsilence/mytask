#=utf8
__author__ = "xieguanfu"

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('21065688', '74aecdce10af604343e942a324641891')

from TaobaoSdk import UserSellerGetRequest  
from TaobaoSdk.Exceptions import  ErrorResponseException
from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)


class UserSellerGet(object):
    """
    """

    @classmethod
    @tao_api_exception()
    def get_user_seller(cls, access_token,fields=None):
        req=UserSellerGetRequest()
        if fields is not None:
            req.fields=fields
        else:
            req.fields="user_id,nick,sex,seller_credit,type,has_more_pic,item_img_num,item_img_size,prop_img_num,prop_img_size,auto_repost,promoted_type,status,alipay_bind,consumer_protection,avatar,liangpin,sign_food_seller_promise,has_shop,is_lightning_consignment,has_sub_stock,is_golden_seller,vip_info,magazine_subscribe,vertical_market,online_gaming"
        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg,sub_code=rsp.sub_code,sub_msg =rsp.sub_msg)
        return rsp.user
   
if __name__=="__main__":
    access_token="62001221e2ef7018e141da64620191ZZ7c7fa4d6a7ccadb871727117"
    user=UserSellerGet.get_user_seller(access_token)
    print user.toDict()
