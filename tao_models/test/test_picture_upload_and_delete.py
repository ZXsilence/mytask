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

from picture_upload import PictureUpload
from picture_delete import PictureDelete
from tao_models.common.exceptions import InvalidAccessTokenException
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestPictureUploadandDelete(unittest.TestCase):
    '''
    taobao.picture.upload
    上传单张图片
    taobao.picture.delete
    删除图片空间图片
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        cls.tcinfo_delete = 'API Test - taobao.picture.delete'
        cls.tcinfo_upload = 'API Test - taobao.picture.upload'
        cls.testInputDatas_upload = [{'nick':'__NotExistNick__','image_path':'/alidata1/sdk_test/test.jpg','popException':True, 'exceptionClass':InvalidAccessTokenException}
                                     ,{'nick':'麦苗科技001','image_path':'/alidata1/sdk_test/test.jpg','popException':False, 'exceptionClass':None}
                                     ]
        cls.testInputDatas_delete = []
        cls.valueType = {'returnValue':dict}
        cls.valueKeys = ['picture']

    def setUp(self):
        pass

    def test_upload_and_delete_img(self):
        for inputdata in self.testInputDatas_upload:
            self.tcinfo_upload = 'API Test - taobao.picture.upload'
            self.tcinfo_upload += str(inputdata)
            is_poped = False
            try:
                returnValue = PictureUpload.upload_img(inputdata['nick'],inputdata['image_path'])
                pic_id=returnValue['picture']['picture_id']
                self.assertTrue(type(returnValue) == self.valueType['returnValue'], self.tcinfo_upload)
                self.assertTrue(returnValue.keys() == self.valueKeys, self.tcinfo_upload)
                res = PictureDelete.delete_img(inputdata['nick'],[pic_id])
                self.assertEqual(res,True)
            except Exception, e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(inputdata['popException'],is_poped,self.tcinfo_upload)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()

#custtests = unittest.TestSuite(map(TestReportService, ['test_rpt_cust_1']))
alltests = unittest.TestLoader().loadTestsFromTestCase(TestPictureUploadandDelete)
