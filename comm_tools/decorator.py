#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luxiaowen
@contact: luxiaowen@maimiaotech.com
@date: 2015-09-11 07:49
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import cProfile
import pstats
import coverage
import random
import time

import os, sys
import logging
sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
logger = logging.getLogger("decorator")
hdlr = logging.FileHandler('/tmp/set_log.log')
hdlr.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s:%(lineno)-15d %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.propagate = False

'''
sort_stats()指定需要排序的维度

Valid Arg       Meaning
'calls'         call count
'cumulative'    cumulative time
'cumtime'       cumulative time
'file'          file name
'filename'      file name
'module'        file name
'ncalls'        call count
'pcalls'        primitive call count
'line'          line number
'name'          function name
'nfl'           name/file/line
'stdname'       standard name
'time'          internal time
'tottime'       internal time

print_stats()指定输出的条数
'''
def do_cprofile(func):
    def profiled_func(*args,**kwargs):
        prof = cProfile.Profile()
        try:
            ret = prof.runcall(func, *args, **kwargs)
            prof.dump_stats("prof.txt")
        finally:
            p = pstats.Stats("prof.txt")
            p.strip_dirs().sort_stats("cumulative").print_stats(30)
            return ret
    return profiled_func

def do_code_coverage(func):
    def code_func(*args,**kwargs):
        cov = coverage.coverage()
        str_int = time.time()
        cov.start()
        ret = func(*args, **kwargs)
        cov.data_files.filename='.coverage.'+func.__name__+'%f'%str_int
        cov.stop()
        cov.save()
        return ret
    return code_func

def set_log(func):
    def setlog(*args,**kwargs):
        ret=func(*args,**kwargs)
        logger.info("_set_log_")
        return ret
    return setlog
