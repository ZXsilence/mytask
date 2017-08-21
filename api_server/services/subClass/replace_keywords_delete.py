#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-15 09:17
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import logging
logger2 = logging.getLogger("api_virtual")
import simplejson
import hashlib
import time
import copy
from datetime import datetime
from exceptions import ApiVirtualResponseException
from common import get_corresponding_key
from replace_base import ReplaceBase

AdgroupDBService = None
ShopInfo = None
KeywordDBService = None
CampaignDBService = None
KeywordChangedTestService = None

class ReplaceKeywordsDelete(ReplaceBase):
    '''
    关键词删除
    '''
    def replace_ret_values(self):
        global AdgroupDBService
        if not AdgroupDBService:from adgroup_db.services.adgroup_db_service import AdgroupDBService
        global ShopInfo
        if not ShopInfo:from shop_db.db_models.shop_info import ShopInfo
        global KeywordDBService
        if not KeywordDBService:from keyword_db.services.keyword_db_service_new import KeywordDBService
        global CampaignDBService
        if not CampaignDBService:from campaign_db.services.campaign_db_service import CampaignDBService
        global KeywordChangedTestService
        if not KeywordChangedTestService: from keyword_db.services.keywords_changed_test_service import KeywordChangedTestService

        #异常捕获
        if not self.campaign_id:
            logger2.error("输入参数个数有误，未找到campaign_id！nick:%s,api_name:%s" % (self.nick,self.api_name))
            ApiVirtualResponseException("输入参数个数有误，未找到campaign_id！nick:%s,api_name:%s" % (self.nick,self.api_name))
        campaign = CampaignDBService.get_campaign(self.campaign_id)
        if not campaign or campaign['nick'] != self.nick:
            logger2.error("输入参数个数有误，%s 不属于 %s ! api_name :%s" % (self.campaign_id,self.nick,self.api_name))
            ApiVirtualResponseException("输入参数个数有误，%s 不属于 %s ! api_name :%s" % (self.campaign_id,self.nick,self.api_name))

        #剔除预删除 关键词
        sid = ShopInfo.get_sid_by_nick(self.nick)
        to_delete_id = []
        if isinstance(self.ivalue,int):
            to_delete_id = [self.ivalue]
        elif type(self.ivalue) in [unicode,str]:
            to_delete_id =[ int(kid) for kid in  self.ivalue.split(",")]
        else:
            logger2.error("输入参数个数有误，请校验keyword_ids:%s " % self.ivalue)
            ApiVirtualResponseException("输入参数个数有误，请校验keyword_ids:%s " % self.ivalue)

        db_keyword_list = KeywordDBService.get_keywords_by_campaign_id(sid,self.campaign_id)
        to_delete_words = []
        keyword_changed = []
        keyword_list = []
        for k in db_keyword_list:
            if k.get("keyword_id",None):
                if k.get("keyword_id",None) in to_delete_id:
                    to_delete_words.append(k.get("word",None))
                    keyword_changed.append(k)
                else:
                    keyword_list.append(k.toDict())

        #剔除后，返回值替换
        klen = len(keyword_list)
        olen = len(self.fkey)
        if klen > olen:
            self.fkey.extend([ copy.deepcopy(self.fkey[0]) for i in range(klen-olen)])
        elif klen < olen:
            self.fkey = self.fkey[:(olen-klen)]

        #全部删除的情况
        if [] == self.fkey:
            KeywordDBService.del_keywords_by_campaign_id(sid,self.campaign_id)
            return self.fkey

        #删除部分的情况
        keys = keyword_list[0].keys()
        for i in range(klen):
            for k in keys:
                setattr(self.fkey[i],k,keyword_list[i][k])
        logger2.info("返回值替换成功！nick:%s,campaign_id:%s,api_name:%s" % (self.nick,self.campaign_id,self.api_name))

        KeywordDBService.del_keywords_by_keyword_ids(sid,to_delete_id)
        logger2.info("删除虚拟库成功！nick:%s,campaign_id:%s,api_name:%s，删除词：%s" % (self.nick,self.campaign_id,self.api_name, ",".join(to_delete_words)))

        #将删除词，更新到 keyword_change_虚拟表中
        KeywordChangedTestService.upsert_keywords_delete(sid,self.campaign_id,keyword_changed)
        logger2.info("keyword_change_虚拟表中更新成功！")

        return self.fkey
