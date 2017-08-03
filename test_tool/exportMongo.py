#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yangmengya
@contact: yangmengya@maimiaotech.com
@date: 2017-08-03 09:23
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import time
import datetime
import pymongo
from pymongo import Connection
import simplejson as json

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))


bak_dir = "./mongobak/"

def useage():
    f = sys.argv[0]
    print "python %s db_name table_name  --同步指定表到测试机/开发机" % (f,)
    print "python %s db_name table_name search_dict  --同步指定表的筛选数据到测试机/开发机,search_dict格式，例如：'{\"finish_num\": 2}'" % (f,)
    print "python %s clear  --清空本地历史dump文件" % (f,)


def clearBak():
    baks = os.listdir(bak_dir)
    if len(baks) > 0:
        for i in range(0,len(baks)):
            d_file = bak_dir + baks[i]
            os.remove(d_file)


def ExportOneMongo(sourceTo,db_name,table_name,search_dict=None):
    db_host = "mm_app_in"
    db_port = 2202
    dump_time = time.strftime("%y%m%d%H%M%S")
    '''
    默认导出格式是Json
    -h 主机ip
    -d 数据库
    -c 数据表
    -q 查询条件
    -o 导出的文件名
    '''
    export_cmd = "mongoexport -h %s --port %s -d %s -c %s -o %s%s_%s.json" %(db_host,db_port,db_name,table_name,bak_dir,table_name,dump_time)
    if search_dict:
        export_cmd = "mongoexport -h %s --port %s -d %s -c %s -q '%s' -o %s%s_%s.json" %(db_host,db_port,db_name,table_name,search_dict,bak_dir,table_name,dump_time)
    os.system(export_cmd)
    host = "mm_app_in"
    port = 2201
    if sourceTo == 'test':
        host = "mm_test_in"
        port = 2201
    #同步前先清空开发机/测试机数据
    conn = Connection(host=host,port=port)
    coll = conn[db_name][table_name]
    coll.remove({})
    #导入线上数据到开发机/测试机
    import_cmd = "mongoimport -h %s --port %s -d %s -c %s %s%s_%s.json" %(host,port,db_name,table_name,bak_dir,table_name,dump_time)
    os.system(import_cmd)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "clear":
        clearBak()
    elif len(sys.argv) == 4:
        sourceTo = sys.argv[1]
        db_name = sys.argv[2]
        table_name = sys.argv[3]
        ExportOneMongo(sourceTo,db_name,table_name)
    elif len(sys.argv) == 5:
        sourceTo = sys.argv[1]
        db_name = sys.argv[2]
        table_name = sys.argv[3]
        search_dict = sys.argv[4]
        if type(search_dict) == str:
            ExportOneMongo(sourceTo,db_name,table_name,search_dict)
        else:
            useage()
    else:
        useage()
    sys.exit(0)

