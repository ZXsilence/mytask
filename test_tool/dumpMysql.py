#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yangmengya
@contact: yangmengya@maimiaotech.com
@date: 2017-08-02 09:23
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import os
import time
import datetime
import MySQLdb
import simplejson as json

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))

from db_pool.conf.prd.settings import RDS1,RDS2,RDS3,RDS4 
from db_pool.conf.dev.settings import RDS1 as DEV_SETTINGS
from db_pool.conf.test.settings import RDS1 as TEST_SETTINGS


bak_dir = "./mysqlbak/"

def useage():
    f = sys.argv[0]
    print "python %s nick sourceTo  --同步指定nick的常用数据表到测试机/开发机" % (f,)
    print "python %s nick sourceTo db_name table_name  --同步指定nick的指定库和表到测试机/开发机" % (f,)
    print "python %s sourceTo db_name table_name  --同步指定数据表到测试机/开发机" % (f,)
    print "python %s sourceTo db_name table_name search_dict  --同步指定数据表到测试机/开发机,筛选条件自定义" % (f,)
    print "python %s clear  --清空本地历史dump文件" % (f,)


def clearBak():
    baks = os.listdir(bak_dir)
    if len(baks) > 0:
        for i in range(0,len(baks)):
            d_file = bak_dir + baks[i]
            os.remove(d_file)


def CommonUse(nick,sourceTo):
    '''
    常用表包括busi库的adgroup_settings、campaign_settings表
    shop_info库的shop_info表
    crm库的orders表
    '''
    db_host = "10.242.173.131 "
    db_user = "maimiao_ops"
    db_password = "maimiaoadmin2014"
    db_port = 4040
    db_name = 'busi'
    tables = ['campaign_settings','adgroup_settings','orders','shop_info']
    dump_time = time.strftime("%y%m%d%H%M%S")
    for i in range(0,len(tables)):
        table_name = tables[i]
        if table_name == 'orders':
            db_name = 'crm'
        elif table_name == 'shop_info':
            db_name = 'shop_info'
        dump_cmd = "mysqldump -t -u%s -p%s -h%s --port %s --databases %s --table %s --where=\"nick='%s'\" --skip-lock-tables >>%s%s_%s.sql" %(db_user,db_password,db_host,db_port,db_name,table_name,nick,bak_dir,table_name,dump_time)
        os.system(dump_cmd)
        host = DEV_SETTINGS['pool_addr']['HOST']
        user = DEV_SETTINGS['pool_addr']['USER'] 
        pwd = DEV_SETTINGS['pool_addr']['PASSWD']
        port = DEV_SETTINGS['pool_addr']['PORT']
        if sourceTo == 'test':
            host = "mm_test_in"
            user = TEST_SETTINGS['pool_addr']['USER'] 
            pwd = TEST_SETTINGS['pool_addr']['PASSWD']
            port = TEST_SETTINGS['pool_addr']['PORT']
        try:
            conn = MySQLdb.connect(host=host,user=user,passwd=pwd,port=port,db=db_name)
            conn.set_character_set("utf8")
            cursor = conn.cursor()
            #同步前先清空开发机/测试机数据
            clear_sql = "DELETE FROM %s.%s WHERE nick='%s'" %(db_name,table_name,nick)
            cursor.execute(clear_sql)
            conn.commit()
            #source线上数据到开发机/测试机
            source_path = "%s%s_%s.sql" %(bak_dir,table_name,dump_time)
            sql = open(source_path).read()
            cursor.execute(sql)
            cursor.close()
            conn.commit()
            conn.close()
        except MySQLdb.Error,e:
            print e
            print "Mysql Error %s" %table_name 


def DumpOneUserMysql(nick,sourceTo,db_name,table_name):
    db_host = None
    db_user =None
    db_password =None
    db_port =None
    for i in [RDS1,RDS2,RDS3,RDS4]:
        rds = i
        if db_name in rds['db_list']:
            db_host = rds['pool_addr']['HOST']
            db_user = rds['pool_addr']['USER']
            db_password = rds['pool_addr']['PASSWD']
            db_port = rds['pool_addr']['PORT']
            break
    dump_time = time.strftime("%y%m%d%H%M%S")
    dump_cmd = "mysqldump -t -u%s -p%s -h%s --port %s --databases %s --table %s --where=\"nick='%s'\" --skip-lock-tables >>%s%s_%s.sql" %(db_user,db_password,db_host,db_port,db_name,table_name,nick,bak_dir,table_name,dump_time)
    os.system(dump_cmd)
    host = DEV_SETTINGS['pool_addr']['HOST']
    user = DEV_SETTINGS['pool_addr']['USER'] 
    pwd = DEV_SETTINGS['pool_addr']['PASSWD']
    port = DEV_SETTINGS['pool_addr']['PORT']
    if sourceTo == 'test':
        host = "mm_test_in"
        user = TEST_SETTINGS['pool_addr']['USER'] 
        pwd = TEST_SETTINGS['pool_addr']['PASSWD']
        port = TEST_SETTINGS['pool_addr']['PORT']
    try:
        conn = MySQLdb.connect(host=host,user=user,passwd=pwd,port=port,db=db_name)
        conn.set_character_set("utf8")
        cursor = conn.cursor()
        #同步前先清空开发机/测试机数据
        clear_sql = "DELETE FROM %s.%s WHERE nick='%s'" %(db_name,table_name,nick)
        cursor.execute(clear_sql)
        conn.commit()
        #source线上数据到开发机/测试机
        source_path = "%s%s_%s.sql" %(bak_dir,table_name,dump_time)
        sql = open(source_path).read()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error,e:
        print e
        print "Mysql Error %s" %table_name 

def DumpSelfDefineMysql(sourceTo,db_name,table_name,search_dict):
    db_host = None
    db_user =None
    db_password =None
    db_port =None
    for i in [RDS1,RDS2,RDS3,RDS4]:
        rds = i
        if db_name in rds['db_list']:
            db_host = rds['pool_addr']['HOST']
            db_user = rds['pool_addr']['USER']
            db_password = rds['pool_addr']['PASSWD']
            db_port = rds['pool_addr']['PORT']
            break
    dump_time = time.strftime("%y%m%d%H%M%S")
    search_keys = search_dict.keys()
    search_values = search_dict.values()
    search_str = ""
    for i in range(0,len(search_keys)):
        if i == 0:
            if type(search_values[i])==str or type(search_values[i]) == unicode:
                #search_str = search_str + search_keys[i] + "=" + %s %(str(search_values[i]).decode("utf-8"))
                tmp = "='%s'" %search_values[i]
                search_str = search_str + search_keys[i] + tmp
            else:
                search_str = search_str + search_keys[i] + "=" + str(search_values[i])
        else:
            if type(search_values[i])==str or type(search_values[i]) == unicode:
                tmp = "='%s'" %search_values[i]
                search_str = search_str + " and " + search_keys[i] + tmp
            else:
                search_str = search_str + " and " + search_keys[i] + "=" + str(search_values[i])
    dump_cmd = '''mysqldump -t -u%s -p%s -h%s --port %s --databases %s --table %s --where="%s" --skip-lock-tables >>%s%s_%s.sql''' %(db_user,db_password,db_host,db_port,db_name,table_name,search_str,bak_dir,table_name,dump_time)
    os.system(dump_cmd)
    host = DEV_SETTINGS['pool_addr']['HOST']
    user = DEV_SETTINGS['pool_addr']['USER'] 
    pwd = DEV_SETTINGS['pool_addr']['PASSWD']
    port = DEV_SETTINGS['pool_addr']['PORT']
    if sourceTo == 'test':
        host = "mm_test_in"
        user = TEST_SETTINGS['pool_addr']['USER'] 
        pwd = TEST_SETTINGS['pool_addr']['PASSWD']
        port = TEST_SETTINGS['pool_addr']['PORT']
    try:
        conn = MySQLdb.connect(host=host,user=user,passwd=pwd,port=port,db=db_name)
        conn.set_character_set("utf8")
        cursor = conn.cursor()
        #同步前先清空开发机/测试机数据
        clear_sql = "DELETE FROM %s.%s WHERE %s" %(db_name,table_name,search_str)
        cursor.execute(clear_sql)
        conn.commit()
        #source线上数据到开发机/测试机
        source_path = "%s%s_%s.sql" %(bak_dir,table_name,dump_time)
        sql = open(source_path).read()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error,e:
        print e
        print "Mysql Error %s" %table_name 

def DumpTableMysql(sourceTo,db_name,table_name):
    db_host = None
    db_user =None
    db_password =None
    db_port =None
    for i in [RDS1,RDS2,RDS3,RDS4]:
        rds = i
        if db_name in rds['db_list']:
            db_host = rds['pool_addr']['HOST']
            db_user = rds['pool_addr']['USER']
            db_password = rds['pool_addr']['PASSWD']
            db_port = rds['pool_addr']['PORT']
            break
    dump_time = time.strftime("%y%m%d%H%M%S")
    dump_cmd = '''mysqldump -t -u%s -p%s -h%s --port %s --databases %s --table %s --skip-lock-tables >>%s%s_%s.sql''' %(db_user,db_password,db_host,db_port,db_name,table_name,bak_dir,table_name,dump_time)
    os.system(dump_cmd)
    host = DEV_SETTINGS['pool_addr']['HOST']
    user = DEV_SETTINGS['pool_addr']['USER'] 
    pwd = DEV_SETTINGS['pool_addr']['PASSWD']
    port = DEV_SETTINGS['pool_addr']['PORT']
    if sourceTo == 'test':
        host = "mm_test_in"
        user = TEST_SETTINGS['pool_addr']['USER'] 
        pwd = TEST_SETTINGS['pool_addr']['PASSWD']
        port = TEST_SETTINGS['pool_addr']['PORT']
    try:
        conn = MySQLdb.connect(host=host,user=user,passwd=pwd,port=port,db=db_name)
        conn.set_character_set("utf8")
        cursor = conn.cursor()
        #同步前先清空开发机/测试机数据
        clear_sql = "DELETE FROM %s.%s" %(db_name,table_name)
        cursor.execute(clear_sql)
        conn.commit()
        #source线上数据到开发机/测试机
        source_path = "%s%s_%s.sql" %(bak_dir,table_name,dump_time)
        sql = open(source_path).read()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error,e:
        print e
        print "Mysql Error %s" %table_name 

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "clear":
        clearBak()
    elif len(sys.argv) == 3:
        nick = sys.argv[1]
        #参数sourceTo='test'表示同步到测试数据机，sourceTo='dev'表示同步到开发机数据库
        sourceTo = sys.argv[2]
        CommonUse(nick,sourceTo)
    elif len(sys.argv) == 4:
        sourceTo = sys.argv[1]
        db_name = sys.argv[2]
        table_name = sys.argv[3]
        DumpTableMysql(sourceTo,db_name,table_name)
    elif len(sys.argv) == 5:
        if sys.argv[1] == 'test' or sys.argv[1] == 'dev':
            sourceTo = sys.argv[1]
            db_name = sys.argv[2]
            table_name = sys.argv[3]
            search_dict = json.loads(sys.argv[4])
            DumpSelfDefineMysql(sourceTo,db_name,table_name,search_dict)
        else:
            nick = sys.argv[1]
            sourceTo = sys.argv[2]
            db_name = sys.argv[3]
            table_name = sys.argv[4]
            DumpOneUserMysql(nick,sourceTo,db_name,table_name)
    else:
        useage()
    sys.exit(0)

