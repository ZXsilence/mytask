#encoding=utf8
"""doc string for module"""
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import logging
import traceback
import inspect

from time import  sleep
from datetime import datetime
import simplejson as json

from TaobaoSdk.Exceptions import ErrorResponseException

from tao_models.common.exceptions import   DataOutdateException
from tao_models.common.exceptions import  InvalidAccessTokenException, TaoApiMaxRetryException, InsufficientSecurityException, AppCallLimitedAllDayException

logger = logging.getLogger(__name__)
mail_logger = logging.getLogger('django.request')


class TaoOpenErrorCode(object):
    """
    error code from taobao open platform

    link: http://open.taobao.com/doc/detail.htm?id=114
    """
    APP_CALL_LIMIT = 7
    SERVICE_TEMP_UNAVAILABLE = 10
    INVALID_SESSION_KEY = 27
    REMOTE_SERVICE_ERROR = 15
    REMOTE_ERROR_600 = 600
    INSUFFICIENT_SECURITY = 53
    REMOTE_ERROR_700 = 700

def tao_api_exception(MAX_RETRY_TIMES = 20):
    def _wrapper_func(func):
        """
        decorator to catch and handle taobao open api exception in a uniform way.

        http://open.taobao.com/doc/detail.htm?id=114
        """
        # 经过调研，目前需要出现的最大重试次数为25次,一百个并发的时候
        # 目前最大重试次数默认为20次

        def __wrapped_func(*args, **kwargs):
            retry_times = 0
            res = None
            while True:
                try:
                    res =  func(*args, **kwargs)
                except ErrorResponseException,e:
                    retry_times += 1
                    code =  e.code
                    if code == TaoOpenErrorCode.APP_CALL_LIMIT :
                        wait_seconds = int(e.sub_msg.split(' ')[5])
                        if wait_seconds >= 180:                              
                            raise AppCallLimitedAllDayException("app call limit [%d] seconds"%wait_seconds)
    
                        logger.error(e)
                        sleep(1)
                        if retry_times == MAX_RETRY_TIMES:
                            raise TaoApiMaxRetryException("retry %i times ,but still failed"%MAX_RETRY_TIMES)
                        continue
                    
                    elif code == TaoOpenErrorCode.REMOTE_ERROR_700:
                        if e.sub_code and u'isp.null-pointer-exception' in e.sub_code:
                            raise #重试无法解决此类异常
                        if e.sub_code and u'isp.top-parse-error' in e.sub_code:
                            raise #重试无法解决此类异常
                        if e.sub_code and u'isp.top-mapping-parse-error' in e.sub_code:
                            raise #重试无法解决此类异常
                        logger.error(e)
                        sleep(5)
                        if retry_times == MAX_RETRY_TIMES:
                            raise TaoApiMaxRetryException("retry %i times ,but still failed"%MAX_RETRY_TIMES)
                        continue

                    elif code == TaoOpenErrorCode.REMOTE_SERVICE_ERROR:
                        logger.info(e)

                        if e.sub_code and u'isv.invalid-permission' in e.sub_code:
                            raise
                        if e.sub_msg and u'推广组Id不存在' in e.sub_msg:
                            raise DataOutdateException(str(e))
                        if e.sub_msg and u'包含了不属于该客户的关键词Id' in e.sub_msg:
                            raise DataOutdateException(str(e))
                        if e.sub_msg and  u'Id不存在' in e.sub_msg:
                            raise
                        if  e.sub_code and u'用户未开通主动通知服' in e.sub_code:
                            raise 
                        sleep(5)
                        if retry_times == MAX_RETRY_TIMES:
                            mail_logger.exception(str(e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed"%MAX_RETRY_TIMES)
                        continue

                    elif code == TaoOpenErrorCode.REMOTE_ERROR_600:
                        if  e.sub_msg and  'end_modified' in e.sub_msg.encode('utf8'):
                            raise  #在这里重试不合适，到整个任务的地方去重试

                        logger.info(e)
                        sleep(5)
                        if retry_times == MAX_RETRY_TIMES:
                            raise TaoApiMaxRetryException("retry %i times ,but still failed"%MAX_RETRY_TIMES)
                        continue

                    elif code == TaoOpenErrorCode.SERVICE_TEMP_UNAVAILABLE:
                        logger.info(e)
                        sleep(5)
                        if retry_times == MAX_RETRY_TIMES:
                            raise TaoApiMaxRetryException("retry %i times ,but still failed"%MAX_RETRY_TIMES)
                        continue

                    elif code == TaoOpenErrorCode.INVALID_SESSION_KEY:
                        logging.exception('got an exception when request taobao api')
                        raise InvalidAccessTokenException("access session expired or invalid")

                    else:
                        logging.exception('got an exception when request taobao api')
                        raise  e
                else:
                    if retry_times:
                        logger.info("retry success, total_retry time:%i"%retry_times)
                    return res
        return __wrapped_func

    return _wrapper_func




