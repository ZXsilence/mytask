#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-09-25 15:47
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import logging
logger2 = logging.getLogger("api_virtual")
import time
import copy
from datetime import datetime
import datetime as dt
from exceptions import ApiVirtualResponseException
from replace_base import ReplaceBase

#导入db_model

class ReplaceSimbaRtrptCustGet(ReplaceBase):
    '''
    账户实时报表虚拟，从样本库中取样，并封装给api返回
    '''
    _from_sample_db = False
    def replace_ret_values(self):
        #输入参数判断
        rt_date = self.ivalue
        if datetime.combine(datetime.now(),dt.time()).strftime("%Y-%m-%d") != str(rt_date):
           logger2.error("输入参数有误，实时时间传入不对！")
           raise ApiVirtualResponseException("输入参数有误，实时时间传入不对！")

        #从样本库获取cust的样本报表
        if self._from_sample_db:
            pass
        else:
            db_cust_rpt = {'impression': '9364', 'cpc': '87.57', 'cost': '3065', 'cpm': '327.32', 'ctr': '0.37', 'roi': '1.3', 'directtransactionshipping': '1', 'indirecttransactionshipping': '0', 'carttotal': '0', 'indirectcarttotal': '0', 'transactionshippingtotal': '1', 'indirecttransaction': '0.0', 'favshoptotal': '2', 'directtransaction': '3990.0', 'favtotal': '2', 'favitemtotal': '0', 'click': '35', 'directcarttotal': '0', 'transactiontotal': '3990.0', 'coverage':'0'}

        #对api返回值进行封装
        #db_keys = db_cust_rpt.keys()
        db_keys = self.fkey[0].toDict().keys()
        self.fkey = self.fkey[:1] #cust的实时报表api会返回多条，但我们这里只返回1条即可。
        for j,key in enumerate(db_keys):
            setattr(self.fkey[0],key,db_cust_rpt[key])
        logger2.info("账户实时报表替换成功！nick:%s " % self.nick)

        return self.fkey
