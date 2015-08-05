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
from comm_tools.xml_tool import change_xml_2_json,change_json_2_xml
from comm_tools.schema_helper import SchemaHelper

logger = logging.getLogger(__name__)

class TmallItemSchemaIncrementUpdate(object):

    
    @classmethod
    @tao_api_exception(6)
    def update_item_desc(cls,nick,num_iid,desc):
        req = TmallItemSchemaIncrementUpdateRequest()
        req.item_id = num_iid 
        #new_desc = desc.replace('<','&lt;').replace('>','&gt;').replace('&nbsp;','')
        xml_data = '''
        <itemRule>
        <field id="update_fields" name="更新字段列表" type="multiCheck">
            <values>
            <value>description</value>
            </values>
        </field>
        <field id="description" name="商品描述" type="input">
        <value>'''+ new_desc + '''</value>
        </field>
        </itemRule>
        '''
        req.xml_data = xml_data
        rsp = ApiService.execute(req,nick)
        print rsp

    @classmethod
    @tao_api_exception(6)
    def update_item_module_desc(cls,nick,num_iid,desc):
        req = TmallItemSchemaIncrementUpdateRequest()
        req.item_id = num_iid 
        #new_desc = desc.replace('<','&lt;').replace('>','&gt;').replace('&nbsp;','')
        #new_desc = desc.replace('&nbsp;','')
        xml_data = '''
            <itemRule>
                <field id="infos" name="信息" type="label">
                    <label-group name="">
                        <label-group name="dev_infos">
                            <label name="开发者说明" value="1.此为消息机制，并且本条消息为开发者消息；2.DevInfo类型消息在第三方开发者有UI对客户展示时应主动屏蔽此类消息，比如这条消息不该被非开发者看到；3.新接口接入初期，有任何疑问或者发现Bug请到旺旺群（群号：836280177）交流" desc="" />
                            <label name="功能更新" value="【2015-01-29更新】增量接口已经支持店铺类目（即：用户类目），大家可以尽快把使用到店铺类目的更新功能切换到增量接口上来" desc="" />
                        </label-group>
                    </label-group>
                </field>
                <field id="update_fields" name="更新字段列表" type="multiCheck">
                    <rules>
                        <rule name="requiredRule" value="true" />
                    </rules>
                    <options>
                        <option displayName="商品描述" value="description" />
                    </options>
                    <values>
                        <value>description</value>
                    </values>
                </field>
                <field id="description" name="商品描述" type="complex">
                    <rules>
                        <rule name="minLengthRule" value="5" exProperty="include" unit="character" />
                        <rule name="maxLengthRule" value="25000" exProperty="include" unit="character" />
                        <rule name="tipRule" value="最多支持发布20个有内容的描述模块" />
                        <rule name="requiredRule" value="true" />
                    </rules>
                    <complex-values>
                        <field id="desc_module_60_cat_mod" type="complex">
                            <complex-values>
                                <field id="desc_module_60_cat_mod_order" type="input">
                                    <value>5</value>
                                </field>
                                <field id="desc_module_60_cat_mod_content" type="input">
                                    <value>&lt;p&gt;&lt;/p&gt;&lt;p&gt;原价：1360元&lt;/p&gt;&lt;p&gt;出版社：线装书局&lt;/p&gt;&lt;p&gt;&lt;/p&gt;</value>
                                </field>
                            </complex-values>
                        </field>
                        <field id="desc_module_58_cat_mod" type="complex">
                            <complex-values>
                                <field id="desc_module_58_cat_mod_order" type="input">
                                    <value>3</value>
                                </field>
                                <field id="desc_module_58_cat_mod_content" type="input">
                                    <value>&lt;p&gt;书名：四库全书精华&lt;/p&gt;&lt;p&gt;册数：8册16开精装&lt;/p&gt;</value>
                                </field>
                            </complex-values>
                        </field>
                        <field id="desc_module_user_mods" type="multiComplex">
                            <complex-values>
                                <field id="desc_module_user_mod_name" type="input">
                                    <value>自定义</value>
                                </field>
                                <field id="desc_module_user_mod_order" type="input">
                                    <value>12</value>
                                </field>
                                <field id="desc_module_user_mod_content" type="input">
                                    <value>&lt;p&gt; &lt;strong&gt;&lt;font color="#ff0000" size="5"&gt;&lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i1/704188445/T2_smPXiBbXXXXXXXX_!!704188445.jpg"/&gt;&lt;/font&gt;&lt;/strong&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i1/704188445/T2j4RPXcNXXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i3/704188445/T2C0bhXoXXXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i1/704188445/T2wZPhXopXXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i1/704188445/T2iufhXlVXXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i4/704188445/T2MNRPXbpXXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i2/704188445/T2SPjhXfBXXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i2/704188445/T2eWjXXnXaXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i2/704188445/T2P3VPXaJcXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i4/704188445/T2fxBPXo0XXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i1/704188445/T2zNdPXbhbXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt; &lt;p&gt; &lt;img align="absMiddle" src="https://img.alicdn.com/imgextra/i1/704188445/T2IhpPXgFaXXXXXXXX_!!704188445.jpg"/&gt; &lt;/p&gt;</value>
                                </field>
                            </complex-values>
                        </field>
                    </complex-values>
                </field>
            </itemRule>
        '''
        req.xml_data = desc 
        #req.xml_data = xml_data 
        rsp = ApiService.execute(req,nick)
        print rsp

if __name__ == '__main__':
    nick = '恒源图书专营店'
    num_iids = [10371723382]
    #nick = '瑜融数码专营店'
    #num_iids = [37724047487]
    fields = 'title,desc,desc_modules,desc_module_info'
    from items_list_get import ItemsListGet
    from tao_models.tmall_item_update_increment_schema_get import TmallItemIncrementUpdateSchemaGet
    #total_item_list = ItemsListGet.get_item_list(nick,num_iids, fields)
    #print total_item_list[0]['desc']
    #desc = total_item_list[0]['desc']
    data = TmallItemIncrementUpdateSchemaGet.get_item_schema(nick,num_iids[0],'description')
    helper = SchemaHelper(data)
    desc = helper.get_value('description')
    helper.set_value(desc,'description')
    desc = helper.get_parapms()
    print desc
    import pdb; pdb.set_trace()  # XXX BREAKPOINT
    #TmallItemSchemaIncrementUpdate.update_item_module_desc(nick,num_iids[0],desc)
