#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-10 10:40
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
sys.path.append('../')
sys.path.append('../../')
import settings
import datetime
import logging
import logging.config
import unittest
from api_server.conf import set_env
set_env.getEnvReady()
from api_server.conf.settings import set_api_source
from item_get import ItemGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException,SDKRetryException
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类

from simba_rpt_adgroupcreativebase_get import SimbaRptAdgroupcreativeBaseGet
from simba_rpt_adgroupkeywordbase_get import SimbaRptAdgroupkeywordbaseGet
from simba_rpt_adgroupeffect_get import SimbaRptAdgroupEffectGet
from simba_rpt_adgroupbase_get import SimbaRptAdgroupBaseGet
from tao_models.test.getCampaignAdgroup import GetCampaignAdgroup

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaRptAdgroupnonsearchBaseGet(unittest.TestCase):
    '''
    simba_rpt_adgroupcreativebase_get推广组下创意报表基础数据查询(汇总数据，不分类型)
    simba_rpt_adgroupkeywordbase_get推广组下的词基础报表数据查询(明细数据不分类型查询)
    simba_rpt_adgroupeffect_get推广组效果报表数据对象
    simba_rpt_adgroupbase_get推广组基础报表数据对象
    '''
    maxDiff=None
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        
        nick,campaign_id=GetCampaignAdgroup.get_has_adgroup_rpt_nick()
        adgroup = GetCampaignAdgroup.get_a_valid_adgroup(nick,[campaign_id])
        adgroup_id = adgroup['adgroup_id']

        start = datetime.datetime.now()-datetime.timedelta(days=7)
        end = datetime.datetime.now()-datetime.timedelta(days=1)

        cls.testData = [{'nick':nick,u'campaign_id':campaign_id,u'adgroup_id':adgroup_id,u'search_type':'SEARCH,CAT',u'source':'1,2',u'start':start,u'end':end,u'popException':False,u'exceptClass':None},
                        {'nick':'',u'campaign_id':campaign_id,u'adgroup_id':adgroup_id,u'search_type':'SEARCH,CAT',u'source':'1,2',u'start':start,u'end':end,u'popException':False,u'exceptClass':None},
                        {'nick':nick,u'campaign_id':0,u'adgroup_id':0,u'search_type':'SEARCH,CAT',u'source':'1,2',u'start':start,u'end':end,u'popException':False,u'exceptClass':None},
                        ]
        cls.adgroupBaseDefault=[u'avgpos', u'ctr', u'adgroupid', u'cpm', u'searchtype', u'campaignid', u'nick', u'cost', u'source', u'date', u'impressions', u'click']
        cls.adgroupHasClick=[u'cpc']

        cls.adgroupEffectDefault=[u'adgroupid', u'searchtype', u'source', u'campaignid', u'nick', u'date']
        
        cls.creativeBaseDefault=[u'avgpos', u'ctr', u'adgroupid', u'cpm', u'searchtype', u'campaignid', u'nick', u'cost', u'source', u'date', u'impressions', u'creativeid', u'click']
        cls.creativeBaseHasClick=[u'cpc']

        cls.keywordBaseDefault=[u'avgpos',u'adgroupid',u'cpm',u'ctr',u'campaignid',u'nick',u'click',u'cost',u'keywordstr',u'source',u'searchtype',u'keywordid',u'date',u'impressions']
        cls.keywordBaseHasClick=[u'cpc']
    
    def seUp(self):
        pass

    def test_simba_rpt_adgroupbaseEffect_get(self):
        import copy
        for inputdata in self.testData:
            is_popped = False
            try:
                #推广组基础报表
                res = SimbaRptAdgroupBaseGet.get_rpt_adgroupbase_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'], inputdata['end'],inputdata['search_type'],inputdata['source'])
                if len(res)>0:
                    for res0 in res:
                        preKeys= copy.deepcopy(self.adgroupBaseDefault)
                        if res0['click']>0:
                            preKeys += self.adgroupHasClick
                        self.assertEqual(sorted(res0.keys()),sorted(preKeys))
                #推广组效果报表
                res =   SimbaRptAdgroupEffectGet.get_rpt_adgroupeffect_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'],inputdata['end'],inputdata['search_type'],inputdata['source'])
                self.assertEqual(type(res), list)
                if len(res)>0:
                    for res0 in res:
                        preKeys = copy.deepcopy(self.adgroupEffectDefault)
                        self.assertEqual(sorted(res0.keys()),sorted(preKeys))
                #推广组创意基础报表
                res = SimbaRptAdgroupcreativeBaseGet.get_rpt_adgroupcreativebase_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'], inputdata['end'],inputdata['search_type'],inputdata['source'])
                self.assertEqual(type(res), list)
                if len(res)>0:
                    for res0 in res:
                        preKeys= copy.deepcopy(self.creativeBaseDefault)
                        if res0['click']>0:
                            preKeys += self.creativeBaseHasClick
                        self.assertEqual(sorted(res0.keys()),sorted(preKeys)) 
                #推广组下的词基础报表数据查询
                res = SimbaRptAdgroupkeywordbaseGet.get_rpt_adgroupkeywordbase_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'], inputdata['end'],inputdata['source'],inputdata['search_type'])
                self.assertEqual(type(res), list)
                if len(res)>0:
                    for res0 in res:
                        preKeys=copy.deepcopy(self.keywordBaseDefault)
                        if res0.get('click') > 0:
                            preKeys += self.keywordBaseHasClick
                        self.assertEqual(sorted(res0.keys()),sorted(preKeys))
            except Exception, e:
                if inputdata['popException']==False:
                    import traceback;traceback.print_exc() 
                    raise e
                else:
                    self.assertRaises(inputdata['exceptClass'])


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaRptAdgroupnonsearchBaseGet)
