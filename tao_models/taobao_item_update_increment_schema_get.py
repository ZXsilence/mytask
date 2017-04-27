#! /usr/bin/env python
#! coding: utf-8 
# author = jyd
# date = 12-8-15


import sys
import os
import copy
import logging
import logging.config

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import ItemIncrementUpdateSchemaGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply
from comm_tools.schema_helper import SchemaHelper
logger = logging.getLogger(__name__)

class TaobaoItemIncrementUpdateSchemaGet(object):

    @classmethod
    @tao_api_exception(6)
    def get_item_schema(cls,nick,num_iid,DEFAULT_FIELDS = 'all'):
        req = ItemIncrementUpdateSchemaGetRequest()
        req.item_id  = num_iid
        req.update_fields = DEFAULT_FIELDS 
        rsp = ApiService.execute(req,nick)
        return change_obj_to_dict_deeply(rsp.update_rules)

    @classmethod
    def get_item_desc(cls,nick,num_iid):
        item_schema = cls.get_item_schema(nick,num_iid,'description')
        helper = SchemaHelper(item_schema)
        desc = helper.get_value('description')
        return desc

if __name__ == '__main__':
    nick = '麦苗科技001'
    num_iid = 39095987083
    data = TaobaoItemIncrementUpdateSchemaGet.get_item_schema(nick,num_iid,'description,wl_description')
    #data = TaobaoItemIncrementUpdateSchemaGet.get_item_desc(nick,num_iid)
    #open('abc.schema','w').write(data)
    print data
