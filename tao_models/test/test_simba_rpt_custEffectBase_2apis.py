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

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaRptCusteffectGet(unittest.TestCase):
    '''
    effect,用户账户报表效果数据查询（只有汇总数据，无分类数据）
    base,客户账户报表基础数据对象
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.testData = [{'nick':'晓迎','start':datetime.datetime(2014,12,11),'end':datetime.datetime(2014,12,18),'popException':False,'exceptClass':None},
                        {'nick':'','start':datetime.datetime(2014,12,11),'end':datetime.datetime(2014,12,18),'popException':True,'exceptClass':TypeError},
                        {'nick':'晓迎','start':datetime.datetime(2014,12,18),'end':datetime.datetime(2014,12,11),'popException':True,'exceptClass':TypeError},
                        ]
        cls.errs={'effect_error':'error find in API: simba_rpt_custeffect_get',
                  'base_error':'error find in API: simba_rpt_custbase_get',
                  'assert_error':'assert exception',
                  }
    
    def seUp(self):
        pass
    def test_get_user_seller(self):
        for inputdata in self.testData:
            is_popped = False
            try:
                res = SimbaRptCusteffectGet.get_shop_rpt_effect(inputdata['nick'], inputdata['start'],inputdata['end'])
                self.assertEqual(type(res),list,self.errs['effect_error'])
                self.assertGreater( len(res), 0 , self.errs['effect_error'])

                res = SimbaRptCustbaseGet.get_shop_rpt_base(inputdata['nick'],inputdata['start'],inputdata['end'])
                self.assertEqual ( type(res), list, self.errs['base_error'])
                self.assertGreater( len(res) , 0 , self.errs['base_error'])

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

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaRptCusteffectGet)
