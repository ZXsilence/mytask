#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from tao_models.conf import set_env
    set_env.getEnvReady()
    from tao_models.conf.settings import set_taobao_client
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')

from TaobaoSdk import ItemcatsAuthorizeGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class ItemcatsAuthorizeGet(object):
    """
    """

    @classmethod
    @tao_api_exception()
    def get_itemcats_authorize(cls, access_token, fields):
        req = ItemcatsAuthorizeGetRequest()
        req.fields = fields


        rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.seller_authorize



if __name__ == '__main__':

    fields = 'brand.vid, brand.name, item_cat.cid, item_cat.name'

    auth = ItemcatsAuthorizeGet.get_itemcats_authorize(fields)

    print auth.item_cats
    print auth.brands


