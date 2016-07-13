#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-08 13:22
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
from TaobaoSdk.Exceptions import ErrorResponseException
from tao_models.common.exceptions import W2securityException, InvalidAccessTokenException#导入异常类
from simba_rpt_campaignbase_get import SimbaRptCampaignbaseGet
from simba_rpt_campaigneffect_get import SimbaRptCampaigneffectGet

from  tao_models.test.getCampaignAdgroup import GetCampaignAdgroup

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaRptCampaigneffectbaseGet(unittest.TestCase):
    '''
    effet:推广计划效果报表数据对象 
    base:推广计划报表基础数据对象 
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        soft_code = "SYB"
        nick,campaign_id = GetCampaignAdgroup.get_has_adgroup_rpt_nick()
        print 'Test nick:',nick
        start = datetime.datetime.now()-datetime.timedelta(days=7)
        end = datetime.datetime.now()-datetime.timedelta(days=1)

        cls.testDataBase = [{'nick':nick,'campaign_id':campaign_id,'search_type':'SEARCH,CAT','source':'1,2','start':start,'end':end,'popException':False,'exceptClass':None},
                            {'nick':'','campaign_id':campaign_id,'search_type':'SEARCH,CAT','source':'1,2','start':start,'end':end,'popException':False, 'exceptClass':None},
                            {'nick':nick,'campaign_id':0,'search_type':'SEARCH,CAT','source':'1,2','start':start,'end':end,'popException':False,'exceptClass':None},
                            {'nick':"_nick_not_exists_",'campaign_id':0,'search_type':'SEARCH,CAT','source':'1,2','start':start,'end':end,'popException':True,'exceptClass':InvalidAccessTokenException},
                            ]
        cls.errs={'effet_error':'error found in API: simba_rpt_campaigneffect_get',
                  'base_error':'error found in API: simba_rpt_campaignbase_get',
                  'assert_error':'assert exception',
                  }
        cls.assertBaseDefault=['avgpos', 'aclick', 'cpm', 'ctr', 'campaignid', 'nick', 'cost', 'source', 'searchtype', 'date', 'impressions', 'click']
        #                     ['avgpos','aclick','cpm','searchtype','nick','cpc','ctr','source','cost','campaignid','date','impressions','click']
        cls.assertEffectDefault=['pay','fav','pay_count']
    def seUp(self):
        pass
    def test_SimbaRptCampaignBaseEffectGet(self):
        for inputdata in self.testDataBase:
            is_popped = False
            try:
                res =  SimbaRptCampaignbaseGet.get_camp_rpt_list_by_date(inputdata['nick'], inputdata['campaign_id'],inputdata['search_type'], inputdata['source'], inputdata['start'],inputdata['end'])
                self.assertEqual(type(res), list ,"预期返回类型为list，api却返回%s类型"%(type(res),))
                if len(res)>0:
                    for res0 in res:
                        if res0.get('click') >0:
                            self.assertTrue(res0.has_key('cpc'),"click>0,但未返回cpc.报表为：%s"%(res0,))
                        for k in self.assertBaseDefault:
                            self.assertTrue(res0.has_key(k),"报表中不存在%s键"%(k,))
                res = SimbaRptCampaigneffectGet.get_campaign_effect_accumulate(inputdata['nick'], inputdata['campaign_id'],inputdata['search_type'], inputdata['source'], inputdata['start'],inputdata['end'])
                self.assertEqual( type(res), dict , "预期返回类型为dict，api却返回%s类型"%(type(res),))
                if res :
                    for k in self.assertEffectDefault:
                        self.assertTrue(res.has_key(k),"报表中不存在%s键"%(k,))
            except Exception, e:
                is_popped = True
                try:
                    self.assertRaises(inputdata['exceptClass'])
                except Exception, e:
                    print e
            finally:
                self.assertEqual(is_popped,inputdata['popException'],self.errs['assert_error'])


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaRptCampaigneffectbaseGet)
