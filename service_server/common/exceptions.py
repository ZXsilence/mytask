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



class ServerEerror(Exception):
    """
    raise this exception when service server excute error  
    """
    def __init__(self, code=None,msg = None):
        self.msg = msg 
        self.code = code
    
    def __str__(self):
        return "ServerEerror:code:%smsg:%s"%(self.code,self.msg)


