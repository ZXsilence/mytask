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



class ServerException(Exception):
    """
    raise this exception when service server excute error  
    """
    def __init__(self, code=None,msg = None,sub_code = None,sub_msg = None):
        self.msg = msg 
        self.code = code
        self.sub_msg = sub_msg 
        self.sub_code = sub_code
    
    def __str__(self):
        return "ServerException:code:%smsg:%s,sub_code:%s,sub_msg:%s"%(self.code,self.msg,self.sub_code,self.sub_msg)

class ZZAccountNotFoundException(Exception):
    """
    not found account in taobao
    """
    def __init__(self, code=None,msg = None):
        self.msg = msg 
        self.code = code
    
    def __str__(self):
        return "ZZAccountNotFoundException:code:%smsg:%s"%(self.code,self.msg)
