#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-08-08 15:35
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
class ApiVirtualResponseException(Exception):
    def __init__(self,msg=None):
        self.msg = msg

    def __str__(self):
        return "%s" % self.msg


