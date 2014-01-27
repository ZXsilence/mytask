#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
import logging.config
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('api_test')

from TaobaoSdk import ItemcatsGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class ItemcatsGet(object):

    @classmethod
    @tao_api_exception()
    def get_child_cats(cls, p_cid):
        req = ItemcatsGetRequest()
        req.fields = 'cid,parent_cid,name,is_parent'
        req.parent_cid = int(p_cid)
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.item_cats)

    @classmethod
    @tao_api_exception()
    def get_cats_by_cids(cls, cids):
        req = ItemcatsGetRequest()
        req.fields = 'cid,parent_cid,name,is_parent'
        req.cids = ",".join([str(k) for k in cids])
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.item_cats)

if __name__ == '__main__':

    item_cats = ItemcatsGet.get_child_cats(0)
    print item_cats

    print '========================='
    item_cats = ItemcatsGet.get_cats_by_cids([50006842])
    print item_cats

