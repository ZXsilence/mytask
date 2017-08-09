#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-08 11:24
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import os
import sys
import logging
logger2 = logging.getLogger("api_virtual")
logger = logger2
from api_server.services.subClass import *

class ApiVirtualReplaceRetBase(object):
    '''
    api_virtual_service进行返回值替换调用的统一入口
    约定：替换返回值的方法名叫: replace_ret_values
    '''
    def __init__(self,api_name,nick,fkey,ivalue):
        self.api_name = api_name
        self.nick = nick
        self.fkey = fkey
        self.ivalue = ivalue
        self.sub_class_obj = None

    #根据api_name找出应该调用哪个类方法，进行实际返回值替换
    def _get_sub_class_by_api_name(self):
        if not self.sub_class_obj:
            try:
                setting = SUB_CLASS_MAPPINGS.get(self.api_name,None)
                if not setting:
                    logger2.error("错误：未能找到%s对应的子类方法！" % self.api_name)
                sub_class_name = setting["class"]
                sub_class = globals()[sub_class_name]
                self.sub_class_obj = apply(sub_class,(self.api_name,self.nick,self.fkey,self.ivalue))
            except BusiException,e :
                logger2.exception(e.msg)
                raise e
            except Exception,e:
                logger2.exception(e)
        return self.sub_class_obj

    #返回值替换统一入口
    def replace_ret_values(self):
        self._get_sub_class_by_api_name()
        if hasattr(self.sub_class_obj ,"replace_ret_values"):
            func = getattr(self.sub_class_obj,"replace_ret_values")
            if hasattr(func,"__call__"):
                return func()
        return None

if __name__ == "__main__":
    #obj = ApiVirtualReplaceRetBase("test","chinchinstyle",None,None)
    pass
