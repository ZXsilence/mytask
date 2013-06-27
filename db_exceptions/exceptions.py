#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Li Yangmin
@contact: liyangmin@maimiaotech.com
@date: 2012-08-02 11:10
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""


class MongodbException(Exception):
    """
    raise this exception when meet a mongodb exception, such as  pymongo.errors.OperationFailure
    """
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return "MongodbException:%s"%(self.msg)


