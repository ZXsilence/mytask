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

class InsufficientSecurityException(Exception):
    """
    raise this exception when R1 security authorize invalid
    """
    def __init__(self, msg = None):
        self.msg = msg
    
    def __str__(self):
        return "InsufficientSecurityException:%s" % (self.msg)

class AppCallLimitedAllDayException(Exception):
    """
    raise this exception when app call limit all day 
    """
    def __init__(self, msg = None):
        self.msg = msg
    
    def __str__(self):
        return "AppCallLimitedAllDayException:%s" % (self.msg)

class ItemForbiddenException(Exception):
    """
    raise this exception when item is not respect to taobao's rules 
    """
    def __init__(self, msg = None, sub_msg = None):
        self.msg = msg
        self.sub_msg = sub_msg
    
    def __str__(self):
        return "ItemForbiddenException:msg [%s] sub_msg [%s]" % (self.msg, self.sub_msg)


class CampaignBudgetLessThanCostException(Exception):
    """
    raise this exception when taobao_client excute error  
    """
    def __init__(self, msg = None, sub_msg = None):
        self.msg = msg
        self.sub_msg = sub_msg
    
    def __str__(self):
        return "CampaignBudgetLessThanCostException:msg [%s] sub_msg [%s]" % (self.msg, self.sub_msg)

class NonsearchNotAllowedException(Exception):
    """
    raise this exception when taobao_client excute error  
    """
    def __init__(self, msg = None, sub_msg = None):
        self.msg = msg
        self.sub_msg = sub_msg
    
    def __str__(self):
        return "NonsearchNotAllowedException:msg [%s] sub_msg [%s]" % (self.msg, self.sub_msg)

class ImgNotBelongToAdgroupException(Exception):
    """
    raise this exception when taobao_client excute error  
    """
    def __init__(self, msg = None, sub_msg = None):
        self.msg = msg
        self.sub_msg = sub_msg
    
    def __str__(self):
        return "ImgNotBelongToAdgroupException:msg [%s] sub_msg [%s]" % (self.msg, self.sub_msg)


class CampaignIdNotBelongToUserException(Exception):
    """
    raise this exception when taobao_client excute error  
    """
    def __init__(self, msg = None, sub_msg = None):
        self.msg = msg
        self.sub_msg = sub_msg
    
    def __str__(self):
        return "CampaignIdNotBelongToUserException:msg [%s] sub_msg [%s]" % (self.msg, self.sub_msg)




