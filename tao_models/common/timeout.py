#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumc
@contact: liumingchao@maimiaotech.com
@date: 2014-08-07 17:52
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
from threading import Thread
import time

class TimeoutException(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        print self.msg

ThreadStop = Thread._Thread__stop

def TimeOut(limit_time):
    def decorator(function):
        def decorator2(*args,**kwargs):
            class TimeLimited(Thread):
                def __init__(self,_error = None):
                    Thread.__init__(self)
                    self._error = _error
                def run(self):
                    try:
                        self.result = function(*args,**kwargs)
                    except Exception ,e:
                        self._error = e

                def _stop(self):
                    if self.isAlive():
                        ThreadStop(self)
            t= TimeLimited() 
            t.start()
            t.join(limit_time)
            if t._error:
                raise t._error
            if t.isAlive() :
                t._stop()
                raise TimeoutException("time out for %s" %(repr(function)))
            if not t._error :
                return t.result
        return decorator2
    return decorator


if __name__ == "__main__":
    @TimeOut(2)
    def fn(s_time):
        print 'sleep %s sesc' %s_time
        time.sleep(s_time)
        print 'finish sleep'
        return "finished"
    print fn(4)
