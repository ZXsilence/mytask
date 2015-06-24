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
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        
        shop = GetCampaignAdgroup.get_a_valid_shop()
        nick=shop['nick']
        campaign=GetCampaignAdgroup.get_a_valid_campaign(nick)
        campaign_id = campaign['campaign_id']
        adgroup = GetCampaignAdgroup.get_a_valid_adgroup(nick,campaign,"SYB",shop['sid'])
        adgroup_id = adgroup['adgroup_id']    
        start = datetime.datetime.now()-datetime.timedelta(days=7)
        end = datetime.datetime.now()-datetime.timedelta(days=1)
        cls.testData = [{'nick':nick,'campaign_id':campaign_id,'adgroup_id':adgroup_id,'search_type':'SEARCH,CAT','source':'1,2','start':start,'end':end,'popException':False,'exceptClass':None},
                        {'nick':'','campaign_id':campaign_id,'adgroup_id':adgroup_id,'search_type':'SEARCH,CAT','source':'1,2','start':start,'end':end,'popException':False,'exceptClass':None},
                        {'nick':nick,'campaign_id':0,'adgroup_id':0,'search_type':'SEARCH,CAT','source':'1,2','start':start,'end':end,'popException':False,'exceptClass':None},
                        ]
        cls.errs={'adgroupbase_error':'error find in API: simba_rpt_adgroupbase_get',
                  'adgroupeffec_error':'error find in API: simba_rpt_adgroupeffect_get',
                  'creativebase_error':'error find in API: simba_rpt_adgroupcreativebase_get',
                  'keywordbase_error':'error find in API:  simba_rpt_adgroupkeywordbase_get',
                  'assert_error':'assert exception',
                  }
        cls.adgroupbaseKeys=['avgpos','ctr','adgroupid','cpm','searchtype','campaignid','nick','cost','source','date','impressions','click']
        cls.adgroupeffectKeys=['adgroupid','searchtype','source','campaignid','nick','date']
        cls.creativebaseKeys=['avgpos','ctr','adgroupid','cpm','searchtype','campaignid','nick','source','cost','date','impressions','creativeid','click']
        cls.keywordbaseKeys=['avgpos','adgroupid','cpm','ctr','campaignid','nick','click','cost','keywordstr','source','searchtype','keywordid','date','impressions']
    
    def seUp(self):
        pass
    def test_simba_rpt_adgroupbaseEffect_get(self):
        for inputdata in self.testData:
            is_popped = False
            try:
                res = SimbaRptAdgroupBaseGet.get_rpt_adgroupbase_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'], inputdata['end'],inputdata['search_type'],inputdata['source'])
                self.assertEqual(type(res), list, self.errs['adgroupbase_error'])
                if len(res)>0:
                    for k in self.adgroupbaseKeys:
                        self.assertTrue(res[0].has_key(k), self.errs['adgroupbase_error'])

                res =   SimbaRptAdgroupEffectGet.get_rpt_adgroupeffect_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'],inputdata['end'],inputdata['search_type'],inputdata['source'])
                self.assertEqual(type(res), list, self.errs['adgroupeffec_error'])
                if len(res)>0:
                    for k in self.adgroupeffectKeys:
                        self.assertTrue(res[0].has_key(k), self.errs['adgroupeffec_error'])
                res = SimbaRptAdgroupcreativeBaseGet.get_rpt_adgroupcreativebase_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'], inputdata['end'],inputdata['search_type'],inputdata['source'])
                self.assertEqual(type(res), list, self.errs['creativebase_error'])
                if len(res)>0:
                    for k in self.creativebaseKeys:
                        self.assertTrue(res[0].has_key(k), self.errs['creativebase_error'])

                res = SimbaRptAdgroupkeywordbaseGet.get_rpt_adgroupkeywordbase_list(inputdata['nick'], inputdata['campaign_id'],inputdata['adgroup_id'],inputdata['start'], inputdata['end'],inputdata['source'],inputdata['search_type'])
                self.assertEqual(type(res), list, self.errs['keywordbase_error'])
                if len(res)>0:
                    for k in self.keywordbaseKeys:
                        self.assertTrue(res[0].has_key(k), self.errs['keywordbase_error'])

            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['exceptClass'])
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaRptAdgroupnonsearchBaseGet)
