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

from TaobaoSdk import TmallItemIncrementUpdateSchemaGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class TmallItemIncrementUpdateSchemaGet(object):

    @classmethod
    @tao_api_exception(6)
    def get_item_schema(cls,nick,num_iid,DEFAULT_FIELDS = 'all'):
        req = TmallItemIncrementUpdateSchemaGetRequest()
        req.item_id  = num_iid
        if DEFAULT_FIELDS and DEFAULT_FIELDS != 'all':
            values = str().join(['<value>%s</value>' % k for k in DEFAULT_FIELDS.split(',') if k])
            req.xml_data = '''<?xml version="1.0" encoding="UTF-8"?><itemParam><field id="update_fields" name="更新字段列表" type="multiCheck"><values>'''+values +'''</values></field></itemParam>'''
        rsp = ApiService.execute(req,nick)
        return change_obj_to_dict_deeply(rsp.update_item_result)

if __name__ == '__main__':
    nick = '哲创家居专营店'
    num_iid = 45420792863
    data = TmallItemIncrementUpdateSchemaGet.get_item_schema(nick,num_iid,'description')
    from comm_tools.xml_tool import change_xml_to_dict_deeply
    import xmltodict
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    xml_dict = xmltodict.parse(data)    
    data = change_xml_to_dict_deeply(xml_dict)
    #data['itemRule']['field'][2]['@id']
    print data
