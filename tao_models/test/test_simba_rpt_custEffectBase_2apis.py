#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-09 04:09
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
from simba_rpt_custeffect_get import SimbaRptCusteffectGet
from simba_rpt_custbase_get import SimbaRptCustbaseGet
from tao_models.test.getCampaignAdgroup import GetCampaignAdgroup
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaRptCusteffectGet(unittest.TestCase):
    '''
    effect,用户账户报表效果数据查询（只有汇总数据，无分类数据）
    base,客户账户报表基础数据对象
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        nick,campaign_id = GetCampaignAdgroup.get_has_adgroup_rpt_nick()
        start = datetime.datetime.now()-datetime.timedelta(days=7)
        end = datetime.datetime.now()-datetime.timedelta(days=1)
        
        cls.testData = [{'nick':nick,'start':start,'end':end,'popException':False,'exceptClass':None},
                        {'nick':'','start':start,'end':end,'popException':False,'exceptClass':None},
                        {'nick':nick,'start':start,'end':end,'popException':True,'exceptClass':TypeError},
                        ]
        cls.assertKeyRptCustEffect=[u'favshopcount', u'directpay', u'nick', u'indirectpay', u'source', u'favitemcount', u'indirectcarttotal', u'indirectpaycount', u'date', u'carttotal', u'directpaycount', u'directcarttotal']
        cls.assertKeyRptCustBase=[u'aclick', u'cpm', u'ctr', u'nick', u'cpc', u'source', u'cost', u'date', u'impressions', u'click']
    def seUp(self):
        pass
    def test_get_user_seller(self):
        for inputdata in self.testData:
            import copy
            try:
                res = SimbaRptCusteffectGet.get_shop_rpt_effect(inputdata['nick'], inputdata['start'],inputdata['end'])
                self.assertEqual(type(res),list)
                preKeys = copy.deepcopy(self.assertKeyRptCustEffect)
                for res0 in res:
                    self.assertEqual(sorted(res0.keys()),sorted(preKeys))
                res = SimbaRptCustbaseGet.get_shop_rpt_base(inputdata['nick'],inputdata['start'],inputdata['end'])
                self.assertEqual ( type(res), list)
                preKeys = copy.deepcopy(self.assertKeyRptCustBase)
                for res0 in res:
                    self.assertEqual(sorted(res0.keys()),sorted(preKeys))
            except TypeError, e:
                self.assertTrue(inputdata['popException'])
            except Exception, e:
                if inputdata['popException']==False:
                    import traceback;traceback.print_exc()
                else:
                    self.assertRaises(inputdata['exceptClass'])

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaRptCusteffectGet)
