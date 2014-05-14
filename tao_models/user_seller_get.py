#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12685542', '6599a8ba3455d0b2a043ecab96dfa6f9')

from TaobaoSdk import UserSellerGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)


class UserSellerGet(object):

    DEFAULT_FIELDS = 'user_id,nick,sex,seller_credit,type,has_more_pic,item_img_num,item_img_size,prop_img_num,prop_img_size,auto_repost,promoted_type,status,alipay_bind,consumer_protection,avatar,liangpin,sign_food_seller_promise,has_user_seller,is_lightning_consignment,has_sub_stock,is_golden_seller,vip_info,magazine_subscribe,vertical_market,online_gaming'

    @classmethod
    @tao_api_exception()
    def get_user_seller(cls, access_token, fields=DEFAULT_FIELDS):
        req = UserSellerGetRequest()
        req.fields = fields

        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)

        return rsp.user.toDict()



def test():
    access_token = "620172616d0c462890edd4dd3f6d97a2f2ZZ4ddf23b579b520500325"
    user_seller_info = UserSellerGet.get_user_seller(access_token)
    print user_seller_info
    print user_seller_info['seller_credit'].toDict()


if __name__ == '__main__':
    test()
