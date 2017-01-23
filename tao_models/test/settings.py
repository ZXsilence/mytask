#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangying
@contact: wangying@maimiaotech.com
@date: 2014-09-25 17:08 @version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

'''['regression', 'new', 'key']'''
import sys
sys.path.append('../../../comm_lib/')
from db_pool.lib.pool_util import PoolUtil

def getTestWorkers():
    conn,cursor = PoolUtil.get_cursor('crm')
    sql = "select email from crm.auth_worker where is_active=1 and id in (SELECT DISTINCT worker_id  from crm.auth_worker_groups where group_id in (14,29))"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return [ k[0] for k in rows]

RUNTYPE = ['regression']
NeedLog = True
b_testMail = False
MAIL_RECEIVE = '920194536@qq.com' # 当b_testMail = True时才发给MAIL_RECEIVE ，否则发给getTestWorkers()中的人
DIRECTOR = {'EMAIL':'monitor@maimiaotech.com',
            'SECRET':'Mm@ops2015)',
            'sendserverip':'smtp.mxhichina.com',
            'sendserverport':25}
# 以下是以QQ邮箱发送服务器
#DIRECTOR = {'EMAIL':'592800277@qq.com',
#            'SECRET':'c2p6b29kZGJ2cHVzYmZnZQ==\n',
#            'sendserverip':'smtp.qq.com',
#            'sendserverport':465}
