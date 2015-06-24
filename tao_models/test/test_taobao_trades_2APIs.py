#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2015-04-08 16:42
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
from taobao_trades_sold_get import TradesSoldGet
from taobao_trade_fullinfo_get import TradeFullinfoGet
from tao_models.test.getCampaignAdgroup import GetCampaignAdgroup
@unittest.skipUnless('regression' in settings.RUNTYPE, "Regression Test Case")
class TestTradesSoldGet(unittest.TestCase):
    '''
    搜索当前会话用户作为卖家已卖出的交易数据（只能获取到三个月以内的交易信息） 
    1. 返回的数据结果是以订单的创建时间倒序排列的。 
    2. 返回的数据结果只包含了订单的部分数据，可通过taobao.trade.fullinfo.get获取订单详情。 
    注意：type字段的说明，如果该字段不传，接口默认只查4种类型订单，非默认查询的订单是不返回。
    遇到订单查不到的情况的，通常都是这个原因造成。
    解决办法就是type加上订单类型就可正常返回了。
    用taobao.trade.fullinfo.get 查订单fields返回type 很容易的能知道订单的类型（type）
    '''
    @classmethod
    def setUpClass(cls):
        set_api_source('SDK_TEST')

        shop = GetCampaignAdgroup.get_a_valid_shop()
        nick=shop['nick']
        start = datetime.datetime.strftime(datetime.datetime.now()-datetime.timedelta(1),"%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
        cls.testData = [{'nick':nick,'start':start,'end':end,'popException':False,'exceptClass':None},
                        {'nick':'','start':start,'end':end,'popException':False,'exceptClass':None},
                        {'nick':'_nick_not_exists_','start':start,'end':end,'popException':True,'exceptClass':InvalidAccessTokenException},
                        ]
        cls.errs = {'trades':'error find in API:taobao_trades_sold_get',
                    'fullinfo':'error find in API:taobao_trade_fullinfo_get',
                    'assert_error':'assert exception ',
                    }

    def seUp(self):
        pass
    def test_get_user_seller(self):
        for inputdata in self.testData:
            is_popped = False
            try:
                res = TradesSoldGet.get_trades_sold_list(inputdata['nick'], inputdata['start'],inputdata['end'])
                self.assertEqual(type(res),list,self.errs['trades'])
                if inputdata['nick']=='':
                    self.assertGreater( len(res), 0 , self.errs['trades'])
                if len(res)>=0:
                    tid = res[0]['tid']
                    trade = TradeFullinfoGet.get_trade_info(inputdata['nick'], tid) # test taobao_trade_fullinfo_get
                    self.assertEqual( type(trade), dict , self.errs['fullinfo'])
                    self.assertEqual( trade['tid'], tid , self.errs['fullinfo'])

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

alltests = unittest.TestLoader().loadTestsFromTestCase(TestTradesSoldGet)
