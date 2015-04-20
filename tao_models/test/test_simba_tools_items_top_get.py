#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-08 19:32
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
from simba_tools_items_top_get import SimbaToolsItemsTopGet

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestSimbaToolsItemsTopGet(unittest.TestCase):
    '''
    取得一个关键词的推广组排名列表
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tstData = [{'nick':'','keyword':'围巾','popException':False, 'exceptClass':None},
                       {'nick':'chinchinstyle','keyword':'围巾','popException':False,'exceptClass':None},
                       {'nick':'chinchinstyle','keyword':'','popException':True,'exceptClass':ErrorResponseException}
                       ]
        cls.errs = {'type_error':'return type error',
                    'value_error':'return value error',
                    'except_error':'except error',
                    }
    def seUp(self):
        pass
    def test_get_top_items_by_keyword(self):
        for inputdata in self.tstData:
            is_popped = False
            try:
                res_list =  SimbaToolsItemsTopGet.get_top_items_by_keyword(inputdata['nick'], inputdata['keyword'])
                self.assertEqual( type(res_list), list , self.errs['type_error'] )
                self.assertGreater( len(res_list), 1, self.errs['value_error'] )
            except Exception, e:
                is_popped = True
                self.assertRaises(inputdata['exceptClass'])
            finally:
                self.assertEqual(is_popped, inputdata['popException'], self.errs['except_error'])

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()

alltests = unittest.TestLoader().loadTestsFromTestCase(TestSimbaToolsItemsTopGet)
