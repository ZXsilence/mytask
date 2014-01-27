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



class ApiSourceError(Exception):
    """
    raise this exception when taobao_client excute error  
    """
    def __init__(self, code=None,sub_code=None,msg=None, sub_msg = None):
        self.msg = msg 
        self.sub_msg = sub_msg
        self.code = code
        self.sub_code = sub_code
    
    def __str__(self):
        return "ApiSourceError:code:%s,sub_code:%s,msg:%s,sub_msg:%s"%(self.code,self.sub_code,self.msg,self.sub_msg)


