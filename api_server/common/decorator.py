#encoding=utf8
"""doc string for module"""
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import logging
import traceback
import inspect

import time
from time import  sleep
from datetime import datetime
import simplejson as json

from MySQLdb import OperationalError

from pymongo.errors import AutoReconnect, OperationFailure, PyMongoError
from db_exceptions.exceptions import  MongodbException
from TaobaoSdk.Exceptions.SDKRetryException import SDKRetryException
import simplejson as json
from thrift.transport.TTransport import TTransportException   

logger = logging.getLogger(__name__)

def mongo_exception(func):
    """
    decorator to catch and deal with mongodb exception in a uniform way.

    example:
    if AutoReconnect exception occurs, we will catch it and retry the last mongodb operation.

    NOTICE:
    this  decorator can be only used for **transaction**, if not, data maybe in a mess.

    """

    def wrapped_func(*args, **kwargs):
        retry_times = 0
        while True:
            try:
                return func(*args, **kwargs)
            except AutoReconnect, e:
                retry_times+=1
                if retry_times > 5:
                    logging.exception("got an exception when operate on mongodb")
                    raise MongodbException(msg=('adgroup_mongo_exception:%s'%str(e)))
                sleep(2)

            except  OperationFailure, e:
                logging.exception("got an exception when operate on mongodb")
                raise MongodbException(msg=('adgroup_mongo_exception:%s'%str(e)))

            except PyMongoError,e:
                logging.exception("got an exception when operate on mongodb")
                raise MongodbException(msg=('adgroup_mongo_exception:%s'%str(e)))
    return wrapped_func

def sdk_exception(MAX_RETRY_TIMES = 20):
    def _wrapper_func(func,*args,**kwargs):

        def __wrapped_func(*args, **kwargs):
            retry_times = 0
            res = None
            while True:
                try:
                    res =  func(*args, **kwargs)
                except (ImportError,ValueError),e:
                    if retry_times == MAX_RETRY_TIMES:
                        logger.error('SDK ERROR,retry %s times,but still failed'%MAX_RETRY_TIMES)
                        raise SDKRetryException
                    retry_times += 1
                    continue
                except TTransportException,e:
                    if retry_times != MAX_RETRY_TIMES:
                        retry_times += 1
                        sleep(3)
                        continue
                    logger.exception('sdk error:%s'%e)
                    raise e
                except Exception,e:
                    if retry_times != MAX_RETRY_TIMES and ("Connection reset by peer" in str(e) or " Connection timed out" in str(e)):
                        retry_times += 1
                        sleep(1)
                        continue
                    logger.exception('sdk error:%s'%e)
                    raise e
                else:
                    if retry_times:
                        logger.info("retry success, total_retry time:%i"%retry_times)
                    return res
        return __wrapped_func

    return _wrapper_func



def mysql_exception(func):
    """
    """

    def wrapped_func(*args, **kwargs):
        retry_times = 0
        start = time.time()
        while True:
            try:

                ret = func(*args, **kwargs)
                logging.debug("%s cost [%s]s, " % (func.__name__, time.time() - start))
                return ret
            except OperationalError, e:
                code = e.args[0]
                retry_times += 1
                if int(code) in [1213,2013,1040,2003,1213]:
                    if retry_times > 20:
                        logging.exception("got an exception when operate on mysql. func:[%s] args:[%s],  **kwargs [%s]" % (func.__name__,str(args),  str(kwargs)))
                        raise e
                else:
                    raise e
                sleep(3)
            except Exception, e:
                    logging.exception("got an exception when operate on mysql. func:[%s] args:[%s],  **kwargs [%s]" % (func.__name__,str(args),  str(kwargs)))
                    raise e

    return wrapped_func



