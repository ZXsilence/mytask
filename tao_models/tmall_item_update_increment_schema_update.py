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

from TaobaoSdk import TmallItemSchemaIncrementUpdateRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService 
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class TmallItemSchemaIncrementUpdate(object):

    
    @classmethod
    @tao_api_exception(6)
    def update_item_desc(cls,nick,num_iid,desc):
        req = TmallItemSchemaIncrementUpdateRequest()
        req.item_id = num_iid 
        xml_data = '''
        <itemRule>
        <field id="update_fields" name="更新字段列表" type="multiCheck">
            <values>
            <value>description</value>
            </values>
        </field>
        <field id="description" name="商品描述" type="input">
        <value>'''+ desc + '''</value>
        </field>
        </itemRule>
        '''
        req.xml_data = xml_data
        rsp = ApiService.execute(req,nick)
        print rsp

if __name__ == '__main__':
    nick = '麦苗科技001'
    num_iid = 45420792863
    desc = '宝贝描述信息'
    TmallItemSchemaIncrementUpdate.update_item_desc(nick,num_iid,desc)
