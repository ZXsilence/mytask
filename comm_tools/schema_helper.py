#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xieguanfu
@contact: xieguanfu@maimiaotech.com
@date: 2015-08-05 11:44
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
from comm_tools.xml_tool import change_xml_2_json,change_json_2_xml

class SchemaHelper:

    def __init__(self,xml_string):
        self.json_data = change_xml_2_json(xml_string)
        self.params_data= {}

    def __get_sys_fields(self,keys = 'update_fields'):
        sys_params = [v for v in self.json_data['itemRule']['field'] if v['@id'] in ['update_fields']]

    def __rename_key(self,field_list):
        if not field_list:
            return field_list
        if type(field_list) == list:
            aa = [self.__rename_key(sub_obj) for sub_obj in field_list]
            return aa
        elif type(field_list) == dict:
            ret_dict = {}
            for k,v in field_list.iteritems():
                new_key = k.replace('default-','')
                if type(v) == list or type(v) == dict:
                    ret_dict[new_key] = self.__rename_key(v)
                else:
                    ret_dict[new_key] = v
            return ret_dict 


    def __get_value_by_type(self,data,field_name):
        if 'default-value' in data:
            return data['default-value']
        if field_name == 'description':
            if 'default-complex-values' not in data:
                return None
            field_json = data['default-complex-values']['field']
            field_json = self.__sort_description(field_json)
            if not field_json:
                return None
            field_json = field_json[0]
            key = '%s_content' % (field_json['@id'].replace('mods','mod') if field_json['@id'].endswith('mods') else field_json['@id'])
            field_json = [v for v in field_json['complex-values']['field'] if v['@id'] == key]
            if not field_json:
                return None
            return self.__change_value(field_json[0]['value'])

    def __sort_description(self,complex_values_fields):
        field_orders  = []
        for obj in complex_values_fields:
            key = obj['@id']
            order_key = '%s_order' %(key.replace('mods','mod') if key.endswith('mods') else key)
            order = [k for k in obj['complex-values']['field'] if k['@id'] == order_key][0]['value']
            field_orders.append({'@id':key,'value':int(order)})
        field_orders.sort(key = lambda e:e['value'])
        complex_values_fields_dict = dict((obj['@id'],obj) for obj in complex_values_fields)
        ret_list = []
        for obj in field_orders:
            ret_list.append(complex_values_fields_dict[obj['@id']])
        return ret_list

    def __change_value(self,value):
        if not value:
            return value
        if type(value) == str or type(value) == unicode:
            return value.replace('&lt;','<').replace('&gt;','>').replace('&nbsp;','')
        return value

    def get_value(self,field_name):
        field_data = [v for v in self.json_data['itemRule']['field'] if v['@id'] == field_name]
        if field_data:
            return self.__get_value_by_type(field_data[0],field_name)

    def set_value(self,value,field_name):
        field_data = [v for v in self.json_data['itemRule']['field'] if v['@id'] == field_name]
        if not field_data:
            return
        field_data = field_data[0].copy()
        if 'default-value' in field_data:
            field_data['value'] = self.__change_value(value)
            field_data.pop('default-value')
            return
        if field_name == 'description':
            if 'default-complex-values' not in field_data:
                return
            field_json = field_data['default-complex-values']['field']
            field_json = self.__sort_description(field_json)
            if not field_json:
                return None
            field_json = field_json[0]
            key = '%s_content' % (field_json['@id'].replace('mods','mod') if field_json['@id'].endswith('mods') else field_json['@id'])
            field_json = [v for v in field_json['complex-values']['field'] if v['@id'] == key]
            if not field_json:
                return None
            field_json[0]['value'] = self.__change_value(value)
            field_data['complex-values'] = field_data['default-complex-values']
            field_data.pop('default-complex-values')
        self.params_data[field_name] = field_data

    def get_parapms(self,to_xml = True):
        sys_params = [v for v in self.json_data['itemRule']['field'] if v['@id'] in ['update_fields']]
        field_list = self.__rename_key(sys_params + self.params_data.values())
        #field_list = self.__rename_key(sys_params)
        schema_params = {'itemRule':{'field':field_list}}
        if to_xml:
            return change_json_2_xml(schema_params)
        return schema_params

