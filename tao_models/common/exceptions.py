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



class TaoApiMaxRetryException(Exception):
    """
    raise this exception when retry time meet the max retry time
    """
    def __init__(self, msg = None):
        self.msg = msg

    def __str__(self):
        return "TaoApiMaxRetryException:%s"%(self.msg)


class InvalidAccessTokenException(Exception):
    """
    raise this exception when invalid access token or access token expires
    """
    def __init__(self, msg = None):
        self.msg = msg

    def __str__(self):
        return "InvalidAccessTokenException:%s"%(self.msg)



class TBDataNotReadyException(Exception):
    """
    raise when TBDataNotReady at moment
    """
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return "TBDataNotReadyException:%s"%(self.msg)


class JsonDecodeException(Exception):
    """
    raise this exception when api output is not json schema
    """
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return "JsonDecodeException:%s "%(self.msg)

class DataOutdateException(Exception):
     """
     raise this exception when data in XCW database does not keep update with taobao platform

     example:
     in XCW database:    but in taobao platform.....
     """

     def __init__(self, msg=None):
         self.msg = msg

     def __str__(self):
         return "DataOutdateException:%s"%(self.msg)

