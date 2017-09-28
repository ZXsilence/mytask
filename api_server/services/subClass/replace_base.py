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
    def __init__(self,api_name,nick,fkey,ivalue,campaign_id=None,adgroup_id=None):
        self.api_name = api_name
        self.nick = nick
        self.fkey = fkey
        self.ivalue = ivalue
        self.campaign_id = campaign_id
        self.adgroup_id = adgroup_id
