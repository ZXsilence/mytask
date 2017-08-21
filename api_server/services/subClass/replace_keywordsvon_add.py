#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-10 14:27
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
KeywordChangedTestService = None

class ReplaceKeywordsvonAdd(ReplaceBase):
    '''
    新增关键词
    create_time\modify_time需要单独赋值
    '''
    def replace_ret_values(self):
        global AdgroupDBService
        if not AdgroupDBService:from adgroup_db.services.adgroup_db_service import AdgroupDBService
        global ShopInfo
        if not ShopInfo:from shop_db.db_models.shop_info import ShopInfo
        global KeywordDBService
        if not KeywordDBService:from keyword_db.services.keyword_db_service_new import KeywordDBService
        global KeywordChangedTestService
        if not KeywordChangedTestService: from keyword_db.services.keywords_changed_test_service import KeywordChangedTestService

        if [] == self.fkey:
            logger2.info("新增0个关键词到虚拟库。nick:%s,campaign_id:%s,adgroup_id:%s" \
                        % (self.nick,self.campaign_id,self.adgroup_id))
            return self.fkey
        #异常处理，判断该推广组id是否存在
        sid = ShopInfo.get_sid_by_nick(self.nick)
        adgroup = AdgroupDBService.get_adgroup(sid,self.adgroup_id)
        if not adgroup:
            logger2.error("推广组不存在！nick:%s,adgroup_id:%s" % (self.nick,self.adgroup_id))
            raise ApiVirtualResponseException("推广组不存在！")
        if not self.campaign_id:
            self.campaign_id = adgroup['campaign_id']

        #已有关键词不进行添加
        keywords_list = KeywordDBService.get_keywords_by_adgroup_id(sid,self.adgroup_id)
        keywords_list = [k.toDict() for k in keywords_list ]
        db_words = [k['word'] for k in keywords_list ]
        to_add_words = []
        not_add_words = []
        for v in self.ivalue:
            if v['word'] not in db_words:
                to_add_words.append(v)
            else:
                not_add_words.append(v['word'])
        if not_add_words:
            not_add_len = len(not_add_words)
            logger2.info("有%s个关键词重复，未添加：%s" % (not_add_len ,",".join(not_add_words)))
            self.fkey = self.fkey[:-not_add_len]
            if [] == self.fkey:
                logger2.info("新增0个关键词到虚拟库。nick:%s,campaign_id:%s,adgroup_id:%s" \
                            % (self.nick,self.campaign_id,self.adgroup_id))
                return self.fkey

        #根据加词个数，构造api返回值
        retKeys = self.fkey[0].toDict().keys()
        timeKey = ["modified_time","create_time"]
        save_db_keyword_list = []

        inputLen = len(to_add_words) 

        #api返回值构造
        inputKeys = to_add_words[0].keys()
        kmd5 = hashlib.md5()
        for i in range(inputLen):
            ikeyword = to_add_words[i]
            for ikey in inputKeys:
                ovalue = ikeyword[ikey]
                okey = get_corresponding_key(ikey) #根据入参key转换得到返回值key
                setattr(self.fkey[i],okey,ovalue)
            for t in timeKey:
                setattr(self.fkey[i],t,datetime.now())
            setattr(self.fkey[i],"campaign_id",self.campaign_id)
            setattr(self.fkey[i],"adgroup_id",self.adgroup_id)
            setattr(self.fkey[i],"is_default_price",bool(ikeyword['isDefaultPrice']))
            setattr(self.fkey[i],"audit_status","audit_pass")
            setattr(self.fkey[i],"is_garbage",False)
            setattr(self.fkey[i],"nick",self.nick)
            kmd5.update(ikeyword['word']+str(time.time()))
            m5 = kmd5.hexdigest()
            kid = ""
            for c in m5:
                if c.isalpha():
                    c = str((ord(c)-97)%10)
                kid += c
            kid = int(kid[:12])
            setattr(self.fkey[i],"keyword_id",kid)

            save_db_keyword_list.append(self.fkey[i].toDict())

        #存虚拟库
        KeywordDBService.add_keyword_list(sid,self.nick,save_db_keyword_list)
        logger2.info("新增%s个关键词到虚拟库。nick:%s,campaign_id:%s,adgroup_id:%s,keywords：%s " \
                     % (len(self.fkey),self.nick,self.campaign_id,self.adgroup_id,",".join([k['word'] for k in save_db_keyword_list])))

        #新增的词，更新到 keyword_change_虚拟表中
        KeywordChangedTestService.upsert_keywords_changed(sid,save_db_keyword_list)
        logger2.info("keyword_change_虚拟表中更新成功！")

        return self.fkey
