#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-07 10:35
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import os
import sys
import simplejson
import copy
import logging
logger2 = logging.getLogger("api_virtual")
logger = logger2
if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
from api_server.db_models.api_structure_templates import ApiStructureTemplate
from api_server.services.api_virtual_replace_key_config import ApiVirtualReplaceKeyConfig
from api_server.services.api_virtual_replace_ret_base import ApiVirtualReplaceRetBase

class  ApiVirtualDB(object):


    def __init__(self,params_dict,soft_code,api_source):
        self.api_name = params_dict['method']
        self.nick = params_dict.get("nick",None)
        self.soft_code = soft_code
        self.api_source = api_source
        self.params_dict = params_dict
        self.response = None

    def call_virtual_db(self):
        if not self.api_name:
            logger2.error("Call ApiVirtualDB时，method name不能为空！")
            return None
        len_input_data = 1 #遇到像关键词改价这种，必须指定此次改价的关键词个数，用语后面替换
        for k , v in self.params_dict.iteritems():
            if isinstance(k,list):
                len_input_data = len(k)
                break
        struct = ApiStructureTemplate.get_api_structure_by_name(self.api_name)
        self.len_input_data = len_input_data
        return struct['api_output']


    def replace_virtual_response(self,response):
        #key：返回结构里使用到的替换键值
        #ikey：入参结构里使用到的替换键值
        key = ApiVirtualReplaceKeyConfig.API_OUTPUT_REPLACE_KEY.get(self.api_name)
        ikey = ApiVirtualReplaceKeyConfig.API_INPUT_REPLACE_KEY.get(self.api_name)
        if not key or not ikey:
            logger2.info("Warn:未找到替换键，原数据返回！")
            return None,None

        #入参结构异常捕获
        ivalue = self.params_dict.get(ikey,None)
        if not ivalue:
            logger2.error("错误：入参没有%s字段，无法进行返回值替换！" % ikey)
        #返回结构异常捕获
        if hasattr(response,key):
            fkey = getattr(response,key)
        else:
            logger2.error("错误：response对象没有%s这个属性！不能进行返回值替换！")
            return None,None

        #根据传参重组返回数据长度，主要是写操作时用到
        if self.len_input_data > 1 and isinstance(fkey,list):
            items = [copy.deepcopy(fkey[0]) for k in range(self.len_input_data)]
            fkey.extend(items)
        #返回值替换
        replace_obj = ApiVirtualReplaceRetBase(self.api_name,self.nick,fkey,ivalue)
        try:
            fkey = replace_obj.replace_ret_values()
            if fkey is None: #必须判断为None才报错，因为fkey可能为[]，是允许的
                logger2.error("错误：替换返回值失败！api_name:%s" % self.api_name)
                return None,None
            #替换值重新赋值，主要是非对象类型时需要重新赋值
            if isinstance(fkey,object):
                setattr(response,key,fkey)
        except Exception,e:
            logger2.exception("错误：替换返回值失败！%s" % e)
            return None,None

        rawContent = simplejson.dumps(self.response)
        return response,rawContent


if __name__ == "__main__":
    params_dict = {'timestamp': u'1501809957060', 'keywordid_prices': u'[{"mobileIsDefaultPrice": 0, "maxMobilePrice": 99, "keywordId": 359278253772}]', 'method': u'taobao.simba.keywords.pricevon.set', 'nick': u'\u9ea6\u82d7\u79d1\u6280001'}
    soft_code = "SYB"
    api_source = "test"
    #obj = ApiVirtualDB(params_dict,soft_code,api_source)
    #res = obj.call_virtual_db()
