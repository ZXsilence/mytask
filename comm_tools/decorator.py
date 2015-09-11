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

def do_cprofile(func):
    def profiled_func(*args,**kwargs):
        prof = cProfile.Profile()
        try:
            prof.runcall(func, *args, **kwargs)
            prof.dump_stats("prof.txt")
        finally:
            p = pstats.Stats("prof.txt")
            p.strip_dirs().sort_stats("cumulative").print_stats(30)
    return profiled_func
