#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-02 13:54
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import thrift
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
from api_server.conf import set_env
set_env.getEnvReady()
from api_server.conf.settings import set_api_source

from wangwang_eservice_receivenum_get import WangwangEserviceReceivenumGet
from tao_models.common.exceptions import TaoApiMaxRetryException
from TaobaoSdk.Exceptions import ErrorResponseException

@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestWangwangEserviceReceivenumGet(unittest.TestCase):
    '''
    根据操作者ID，返回被查者ID指定时间段内每个帐号的"已接待人数"
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')
        
        dend = datetime.datetime.now()
        _30day = datetime.timedelta(days=30)
        yesday = datetime.timedelta(days=1)
        dend = dend - yesday
        minus30day = dend - _30day
        dstart = datetime.datetime(minus30day.year,minus30day.month,minus30day.day,0,0,0)
        dend = dend.strftime("%Y-%m-%d")
        dend = datetime.datetime.strptime(dend,"%Y-%m-%d")

        cls.testInputdata = [{'nick':'麦苗科技001','serivce_nick_list':['cntaobao麦苗科技001:麦麦'],'start_time':dstart,'end_time':dend,'popException':False,'exceptionClass':None},
                             {'nick':'','serivce_nick_list':['cntaobao麦苗科技001:麦麦'],'start_time':dstart,'end_time':dend,'popException':True,'exceptionClass':ErrorResponseException},
                             {'nick':'_nick_not_exsits_','serivce_nick_list':['cntaobao麦苗科技001:麦麦'],'start_time':dstart,'end_time':dend,'popException':True,'exceptionClass':ErrorResponseException},
                             {'nick':'麦苗科技001','serivce_nick_list':[''],'start_time':dstart,'end_time':dend,'popException':True,'exceptionClass':thrift.transport.TTransport.TTransportException}
                             ]
        cls.errs = {'type_error':'return type error','value_error':'return value error','except':'assert except'}
    def test_get_group_member_list(self):
        for inputdata in self.testInputdata:
            is_poped = False
            try:
                activity_list = WangwangEserviceReceivenumGet.get_receivenum_list(inputdata['nick'],inputdata['serivce_nick_list'],inputdata['start_time'],inputdata['end_time'])
                self.assertEqual(type(activity_list), list, self.errs['type_error'])
            except Exception , e:
                is_poped = True
                self.assertRaises(inputdata['exceptionClass'])
            finally:
                self.assertEqual(is_poped , inputdata['popException'],self.errs['except'])

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':                                                       
    unittest.main()
alltests = unittest.TestLoader().loadTestsFromTestCase(TestWangwangEserviceReceivenumGet)
