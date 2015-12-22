#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xieguanfu
@contact: xieguanfu@maimiaotech.com
@date: 2015-10-27 17:09
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import gevent
import inspect
from gevent import monkey

def multi_execute(func,args = [],kwargs = []):
    monkey.patch_all()
    if not args and not kwargs:
        jobs = [gevent.spawn(func,parm_dict) for parm_dict in args]
    if args and not kwargs:
        func_args = inspect.getargspec(func)[0]
        if not (isinstance(args[0],list) or isinstance(args[0],tuple)) or (len(func_args) <= 2 and len(args[0]) <=1):
            jobs = [gevent.spawn(func,parm_dict) for parm_dict in args]
        else:
            jobs = [gevent.spawn(func,*parm_dict) for parm_dict in args]
    elif not args and kwargs:
        jobs = [gevent.spawn(func,**parm_dict) for parm_dict in kwargs]
    elif len(args) == len(kwargs):
        func_args_tuple = inspect.getargspec(func)
        func_args = func_args_tuple[0]
        func_kwargs = func_args_tuple[3]
        args_size = len(func_args) - (0 if func_kwargs else  len(func_kwargs))
        if not (isinstance(args[0],list) or isinstance(args[0],set)) or (args_size <= 2 and len(args[0]) <=1):
            jobs = [gevent.spawn(func,args[i],**kwargs[i]) for i in xrange(len(args))]
        else:
            jobs = [gevent.spawn(func,*args[i],**kwargs[i]) for i in xrange(len(args))]
    else:
        raise Exception('invalid func:%s args:%s kwargs:%s' % (func.__name__,args,kwargs))
    gevent.joinall(jobs)
    data = []
    #for obj in jobs:
    #    if obj.successful():
    #        data.append(job.value)
    #    else:
    #         data.append()
    data = [job.value for job in jobs]
    print data
    return data

def multi_execute_with_pool(func,params,concurrent_size = 30):
    from gevent.pool import Pool
    pool = Pool(concurrent_size)
    #jobs = [gevent.spawn(func,parm_dict,parm_dict) for parm_dict in params]
    dd = pool.map(func,params)
    #data = gevent.joinall(jobs)
    print dd

class Af(object):
    def test1(self,i):
        print i
        return i

    def test2(self,i,b):
        print i,b
        return i,b

    def test3(self,i,name = None,age =5):
        return 'index:%s,name :%s,age:%s' %(i,name,age)

    def test4(self,name = None,age =5):
        return 'name :%s,age:%s' %(name,age)

    def test5(self,i,b,name = None,age =5):
        return 'index:%s,name :%s,age:%s' %(i,name,age)

if __name__ == '__main__':
    obj = Af()
    multi_execute(obj.test1,args = [1,2,3])
    multi_execute(obj.test2,args = [(1,2),(3,5)])
    multi_execute(obj.test3,args = [1,2,3],kwargs=[{'name':'aa','age':56},{'age':80},{'name':'cc'}])
    multi_execute(obj.test5,args = [[2,2],[3,3],[4,4]],kwargs=[{'name':'aa','age':56},{'age':80},{'name':'cc'}])
    multi_execute(obj.test4,kwargs=[{'name':'aa','age':56},{'age':80},{'name':'cc'}])


