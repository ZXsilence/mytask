#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-21 10:11
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import logging
logger2 = logging.getLogger("api_virtual")

class ReplaceBase(object):
    def __init__(self,api_name,nick,fkey,ivalue,*args):
        self.api_name = api_name
        self.nick = nick
        self.fkey = fkey
        self.ivalue = ivalue
        #动态赋值变量
        if isinstance(args[0],dict):
            for k,v in args[0].iteritems():
                if k in ("adgroup_id","campaign_id"):
                    v = int(v)
                #if type(v)==unicode:
                #    v = str(v)
                setattr(self,k,v)
