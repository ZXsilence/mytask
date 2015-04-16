#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangying
@contact: wangying@maimiaotech.com
@date: 2014-09-25 14:07
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

from picture_category_get import PictureCategoryGet
from tao_models.common.exceptions import InvalidAccessTokenException
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPictureCategoryGet(unittest.TestCase):
    '''
    taobao.picture.category.get
    获取图片分类信息
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo = 'API Test - taobao.picture.category.get'
        cls.testInputDatas = [{'nick':'麦苗科技001','category_name':'省油宝创意请勿删除','popException':False, 'exceptionClass':None},
                              {'nick':'__NOTEXISTEDNICK__','category_name':'elle 女包','popException':True, 'exceptionClass':ErrorResponseException},
                              {'nick':'chinchinstyle','category_name':'省油宝创意请勿删除','popException':False, 'exceptionClass':None},
                              ]
        cls.valueType = {'returnValue':list}
        cls.itemFields = 'picture_category_id,created,modified,parent_id,picture_category_name,position,type'

    def setUp(self):
        pass

    def test_get_picture_category_name(self):
        for inputdata in self.testInputDatas:
            is_poped = False
            try:
                returnValue = PictureCategoryGet.get_picture_category_name(inputdata['nick'],inputdata['category_name'])
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo)
                for i in range(len(returnValue)):
                    itemKeys = returnValue[i].keys()
                    for item in itemKeys:
                        self.assertTrue(item in self.itemFields.split(','), self.tcinfo)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo)


    #@unittest.skip("Unconditionally skip the decorated test")
    #def test_skip(self):
    #    """test"""
    #    pass

    #@unittest.expectedFailure
    #def test_expectedFailure(self):
    #    """test"""
    #    print self.testdata

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

#custtests = unittest.TestSuite(map(TestReportService, ['test_rpt_cust_1']))
alltests = unittest.TestLoader().loadTestsFromTestCase(TestPictureCategoryGet)
