#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangying
@contact: wangying@maimiaotech.com
@date: 2014-09-25 17:08
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

'''['regression', 'new', 'key']'''
import sys
sys.path.append('../../../comm_lib/')
from db_pool.lib.pool_util import PoolUtil

def getTestWorkers():
    conn,cursor = PoolUtil.get_cursor('crm')
    sql = "select email from crm.auth_worker where id in (SELECT DISTINCT worker_id  from crm.auth_worker_groups where group_id in (14,29))"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return [ k[0] for k in rows]

RUNTYPE = ['regression']
NeedLog = True
b64encode = True # 仅当SECRET是base64加密时，b64encode 才是True
b_testMail =False 
MAIL_RECEIVE = '592800277@qq.com' # 当b_testMail = True时才发给MAIL_RECEIVE ，否则发给getTestWorkers()中的人
DIRECTOR = {'EMAIL':'tanglingling@maimiaotech.com',
            'SECRET':'P2xsQG1tMjAxNQ==',
            #'sendserverip':'smtp.qq.com',
            'sendserverip':'smtp.mxhichina.com',
            #'sendserverport':465}
            'sendserverport':25}

