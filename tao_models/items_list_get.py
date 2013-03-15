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
    set_taobao_client('12651461', '80a15051c411f9ca52d664ebde46a9da')

from TaobaoSdk import ItemsListGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf import    settings as tao_model_settings
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)


class ItemsListGet(object):

    DEFAULT_FIELDS = 'title,price,pic_url,num_iid,detail_url,props_name,cid,delist_time,list_time'
    MAX_NUM_IIDS = 20

    @classmethod
    @tao_api_exception()
    def get_item_list(cls, access_token, num_iids, fields=DEFAULT_FIELDS):

        num_iid_list = copy.deepcopy(num_iids)
        total_item_list = []

        req = ItemsListGetRequest()
        req.fields = fields

        while num_iid_list:
            sub_num_iid_list = num_iid_list[:cls.MAX_NUM_IIDS]
            num_iid_list = num_iid_list[cls.MAX_NUM_IIDS:]

            req.num_iids = ",".join([str(num_iid) for num_iid in sub_num_iid_list])

            rsp = tao_model_settings.taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

            if rsp.items is None:
                logger.info("get item info, expect %s, actually return: %s"%(len(sub_num_iid_list), 0))
                continue

            logger.debug("get item info, expect %s, actually return: %s"%(len(sub_num_iid_list), len(rsp.items)))
            total_item_list.extend(rsp.items)

        return total_item_list



def test():
    access_token = "620260146ZZc0465e1b4185f7b4ca8ba1c7736c28d1c675871727117"
    #access_token = '111'
    #num_iids = [7794896442,15493508084]
    num_iids = [23221560872]
    ItemsListGet.MAX_NUM_IIDS = 20
    fields = 'title,price,pic_url,num_iid,detail_url,props_name,cid,list_time,delist_time,modified'
    total_item_list = ItemsListGet.get_item_list(access_token, num_iids, fields)

    for item in total_item_list:
        print item.toDict()

if __name__ == '__main__':
    test()
