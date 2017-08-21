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
import datetime
logger2 = logging.getLogger("api_virtual")
logger = logger2
if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
from api_server.db_models.api_structure_templates import ApiStructureTemplate
from api_server.services.api_virtual_replace_key_config import ApiVirtualReplaceKeyConfig
from api_server.services.api_virtual_replace_ret_base import ApiVirtualReplaceRetBase
from api_server.services.subClass.common import get_corresponding_key

class  ApiVirtualService(object):


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
        struct = ApiStructureTemplate.get_api_structure_by_name(self.api_name)
        if not struct:
            return None
        return struct['api_output']


    def replace_virtual_response(self,response):

        #key：返回结构里使用到的替换键值
        #ikey：入参结构里使用到的替换键值
        okey = ApiVirtualReplaceKeyConfig.API_OUTPUT_REPLACE_KEY.get(self.api_name)
        ikey = ApiVirtualReplaceKeyConfig.API_INPUT_REPLACE_KEY.get(self.api_name)
        if not okey or not ikey:
            logger2.info("Warn:未找到替换键，原数据返回！")
            return None,None

        #入参结构异常捕获
        if not self.params_dict.get(ikey,None):
            logger2.error("错误：入参没有%s字段，无法进行返回值替换！" % ikey)
            return None,None

        #入参值处理
        try:
            iv = self.params_dict[ikey]
            iv = simplejson.loads(iv)
        except ValueError,e:
            if ikey in ("adgroup_id","campaign_id"): #这里后续有类型继续加进去！！
                iv = int ( iv)
            else:
                iv = iv

        if self.params_dict.get("page_no",None) and self.params_dict.get("page_size",None):
            ivalue = {}
            ivalue["page_no"] = self.params_dict["page_no"]
            ivalue["page_size"] = self.params_dict["page_size"]
            ivalue["ivalue"] = iv
        else:
            ivalue = iv 

        #返回结构异常捕获
        self.response = response
        if hasattr(response,okey):
            fkey = getattr(response,okey)
        else:
            logger2.error("错误：response对象没有%s这个属性！不能进行返回值替换！")
            return None,None


        #根据传参重组返回数据长度，主要是写操作时用到 . 读操作还是需要在具体替换类中单独实现
        if isinstance(fkey,list) and isinstance(ivalue,list):
            inputLen = len(ivalue)
            outputLen = len(fkey)
            if inputLen > outputLen:
                fkey.extend([copy.deepcopy(fkey[0]) for i in range(inputLen-outputLen)])
            elif inputLen < outputLen:
                fkey = fkey[:(outputLen-inputLen)]

        #返回值替换
        campaign_id = self.params_dict.get("campaign_id",None)
        adgroup_id = self.params_dict.get("adgroup_id",None)
        campaign_id = int(campaign_id) if campaign_id else campaign_id
        adgroup_id = int(adgroup_id) if adgroup_id else adgroup_id

        replace_obj = ApiVirtualReplaceRetBase(self.api_name,self.nick,fkey,ivalue,campaign_id,adgroup_id)
        try:
            fkey = replace_obj.replace_ret_values() #返回值替换公共入口
            if fkey is None: #必须判断为None才报错，因为fkey可能为[]，是允许的
                logger2.error("错误：替换返回值失败！api_name:%s" % self.api_name)
                return None,None
            #替换值重新赋值，主要是非对象类型时需要重新赋值
            setattr(self.response,okey,fkey)
        except Exception,e:
            logger2.exception("错误：替换返回值失败！%s" % e)
            return None,None

        # rawContent 没毛用, 结构和实际api的rawContent不一样。但都把键值返回

        content = copy.deepcopy(fkey)
        rawContent={}
        response_name = self.response.__module__.split(".")[-1]
        response_name = get_corresponding_key(response_name)[1:]
        rawContent[response_name] = {}
        if isinstance(content,list):
            rawContent[response_name][okey] = covertObjRecursively(content)
        else:
            attrs = [k for k in dir(content) if not k.startswith("_") and k != "toDict" ]
            for attr in attrs:
                rawContent[response_name][attr] = covertObjRecursively(getattr(content,attr))
        rawContent = simplejson.dumps(rawContent)
        return self.response,rawContent

#递归寻找，将为list的对象显示出来
BASE_TYPE = [str,bool,int,long,float,tuple,dict,datetime,unicode]
def covertObjRecursively(attr):
    if isinstance(attr,list): #是list对象
        if len(attr)==0:
            return []
        if type(attr[0]) in BASE_TYPE:
                return attr
        try:
            if isinstance(attr[0].toDict(),dict):
                res = [k.toDict() for k in attr ]
                for res0 in res:
                    for k ,v in res0.iteritems():
                        if type(v) == type(datetime.datetime.now()):
                            res0[k] = datetime.datetime.strftime(v,"%Y-%m-%d %H:%M:%S")
                return res
        except Exception,e:
            logger2.exception("原值返回！attr:%s , type(attr):%s " % (attr,type(attr)))
            return attr
    elif type(attr) in BASE_TYPE:# 属性是基础类型
        return attr
    else: #还是class继续递归
        ats = [k for k in dir(attr) if not k.startswith("_") ]
        for at in ats:
            setattr(attr,at,covertObjRecursively(getattr(attr,at)))

if __name__ == "__main__":
    params_dict = {'timestamp': u'1501809957060', 'keywordid_prices': u'[{"mobileIsDefaultPrice": 0, "maxMobilePrice": 99, "keywordId": 359278253772}]', 'method': u'taobao.simba.keywords.pricevon.set', 'nick': u'\u9ea6\u82d7\u79d1\u6280001'}
    soft_code = "SYB"
    api_source = "test"
    #obj = ApiVirtualDB(params_dict,soft_code,api_source)
    #res = obj.call_virtual_db()
