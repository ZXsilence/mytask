#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from xuanciw.settings import  trigger_envReady
    logging.config.fileConfig('../xuanciw/consolelogger.conf')

from TaobaoSdk import ItemsListGetRequest
from TaobaoSdk.Exceptions import  ErrorResponseException

from tao_models.conf.settings import  taobao_client
from tao_models.common.decorator import  tao_api_exception


logger = logging.getLogger(__name__)


class ItemsListGet(object):

    DEFAULT_FIELDS = 'title,price,pic_url,num_iid,detail_url,props_name'
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

            rsp = taobao_client.execute(req, access_token)[0]
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_msg, sub_msg=rsp.sub_msg)

            if rsp.items is None:
                logger.info("get item info, expect %s, actually return: %s"%(len(sub_num_iid_list), 0))
                continue

            logger.info("get item info, expect %s, actually return: %s"%(len(sub_num_iid_list), len(rsp.items)))
            total_item_list.extend(rsp.items)

        return total_item_list



def test():
    access_token = "6200b26ad6dde0735bc63c45618ca4f8bdfhfc1dfd08854100160612"
    num_iids = [16675583313,16675579321]
    ItemsListGet.MAX_NUM_IIDS = 20
    total_item_list = ItemsListGet.get_item_list(access_token, num_iids)

    for item in total_item_list:
        print item.toDict()

if __name__ == '__main__':
    test()