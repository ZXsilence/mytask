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

from TaobaoSdk import ItemcatsGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception

logger = logging.getLogger(__name__)

class ItemcatsGet(object):
    """
    """

    @classmethod
    @tao_api_exception()
    def get_child_cats(cls, p_cid):
        req = ItemcatsGetRequest()
        req.fields = 'cid,parent_cid,name,is_parent'
        req.parent_cid = int(p_cid)

        rsp = tao_model_settings.taobao_client.execute(req, '')[0]

        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

        return rsp.item_cats





if __name__ == '__main__':

    item_cats = ItemcatsGet.get_child_cats(0)

    for item_cat in item_cats:
        print item_cat.cid, item_cat.name

    print '========================='
    item_cats = ItemcatsGet.get_child_cats(50006842)

    for item_cat in item_cats:
        print item_cat.cid, item_cat.name