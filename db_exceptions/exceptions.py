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

#数据库异常
class MongodbException(Exception):
    """
    raise this exception when meet a mongodb exception, such as  pymongo.errors.OperationFailure
    """
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return "MongodbException:%s"%(self.msg)

#可忽视的异常
class IgnoredException(Exception):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return "IgnoredException:%s"%(self.msg)

#商家测试帐号引起的异常,继承于可忽视异常
class TaobaoTestException(IgnoredException):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return "TaobaoTestException:%s"%(self.msg)

#fetch_access_token时解析出错引起的异常
class ResolveTokenException(IgnoredException):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return "ResolveTokenException:%s"%(self.msg)

