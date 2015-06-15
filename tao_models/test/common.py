#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangying
@contact: wangying@maimiaotech.com
@date: 2014-09-25 16:36
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import datetime
import copy
import simplejson
from db_pool.lib.pool_util import PoolUtil

class CommonLib(object):
    cat_id = 2
    '''Common Lib'''

    '''对api返回数据的精度进行修改方便比较，去掉不需要的aclick'''
    @classmethod
    def deleteParam(cls,rpt_list):
        for rpt in rpt_list:
            rpt.pop('campaignid')
            rpt.pop('cpc')
            rpt.pop('nick')
            rpt['avgpos'] = int(round(rpt['avgpos'],2))
            rpt['cpc'] = int(round(rpt['cpc'],2))
            rpt['cpm'] = int(round(rpt['cpm'],2))
            rpt['ctr'] = int(round(rpt['ctr'],2))
        return rpt_list

    @classmethod
    def row_to_dict(cls,cat_id, start_date, end_date, rpt):
        report = {}
        report['cat_id'] = int(cat_id)
        report['start_date'] = start_date
        report['end_date'] = end_date
        if rpt:
            for key in ['competition', 'click', 'cost', 'directtransaction', 'indirecttransaction', \
                        'favshoptotal', 'transactionshippingtotal', 'favitemtotal', 'favtotal']:
                report[key] = int(rpt[key])
            for key in ['cpc', 'ctr', 'roi', 'coverage']:
                report[key] = float(rpt[key])
        return report
    @classmethod
    def deleteHyRPTTestData(cls):
        _db = 'syb_web'
        _table = "hy_rpt"
        sql = "delete from %s where cat_id=%d"%(_table,cls.cat_id);
        conn, cursor = PoolUtil.get_cursor(_db)
        cursor.execute(sql)
        conn.commit()
        PoolUtil.close_cursor(conn, cursor)

