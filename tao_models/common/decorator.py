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
from tao_models.conf import    settings as tao_model_settings
from tao_models.common.exceptions import  InvalidAccessTokenException, TaoApiMaxRetryException, InsufficientSecurityException, AppCallLimitedAllDayException
from api_records.services.api_records_service import inc_api_call_times, get_api_call_times, update_api_call_times, QueueName
api_call_infos = [ 
        ['syb_auto_campaign_optimize_job.py',QueueName.SYB_AUTO_CAMPAIGN_OPTIMIZE],
        ['syb_auto_creative_optimize_job.py',QueueName.SYB_AUTO_CREATIVE_OPTIMIZE],
        ['syb_key_campaign_optimize_job.py',QueueName.SYB_KEY_CAMPAIGN_OPTIMIZE]
]
api_call_requests = [
    'SimbaKeywordsvonAdd',
    'SimbaKeywordsPricevonSet',
    'SimbaKeywordsDelete'
]
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


DEBUG_MODE=False
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
                    if (DEBUG_MODE and (len(args) >= 1) and (
                                cmp(args[0].__class__.__name__, 'SimbaKeywordsvonAdd') == 0 or
                                cmp(args[0].__class__.__name__, 'SimbaKeywordsPricevonSet') == 0 or
                                cmp(args[0].__class__.__name__, 'SimbaKeywordsDelete') == 0 or
                                cmp(args[0].__class__.__name__, 'SimbaCreativeUpdate') == 0 or
                                cmp(args[0].__class__.__name__, 'SimbaCreativeAdd') == 0 
                                )

                            ):
                        logger.info(args[0].__class__.__name__ + "return None")
                        return None

                    res =  func(*args, **kwargs)
                except ErrorResponseException,e:
                    logger.info('exception: code %d *args:%s', e.code, str(args))
                    logger.info('exception:**kwargs:%s'%str(kwargs))
                    logger.info('exception:%s meet tao api exception :%s, retry_times:%s'%(func.__name__, e, retry_times))
                    retry_times += 1
                    code =  e.code
                    if code == 530 and 'isp.top-remote-connection-timeout' in e.sub_code:
                        if retry_times == MAX_RETRY_TIMES:
                            print '530 timeout重试失败！'
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        print '重试！'
                        continue
                    if code == TaoOpenErrorCode.APP_CALL_LIMIT :
                        if retry_times == MAX_RETRY_TIMES:
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))

                        wait_seconds = int(e.sub_msg.split(' ')[5])
                        if wait_seconds > 60:
                            logger.error("app call limit [%d] seconds"%wait_seconds)
                            raise AppCallLimitedAllDayException("app call limit [%d] seconds"%wait_seconds)
                        else: 
                            if wait_seconds >= 2:
                                logger.debug("app call limit [%d] seconds, need sleep"%wait_seconds)
                            sleep(wait_seconds)
                        continue
                    #isp类型错误，只有三种无法重试
                    elif code == TaoOpenErrorCode.REMOTE_ERROR_700:
                        if e.sub_code and u'isp.null-pointer-exception' in e.sub_code:
                            raise #重试无法解决此类异常
                        if e.sub_code and u'isp.top-parse-error' in e.sub_code:
                            raise #重试无法解决此类异常
                        if e.sub_code and u'isp.top-mapping-parse-error' in e.sub_code:
                            raise #重试无法解决此类异常
                        sleep(5)
                        if retry_times == MAX_RETRY_TIMES:
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        continue

                    elif code == TaoOpenErrorCode.REMOTE_SERVICE_ERROR:
                        if e.sub_code.startswith('isv'):
                            #错误码为15，且以isv开头的子错误码，属于业务异常，直接抛出，无需重试
                            raise
                        elif e.sub_code == "6001":
                            #user not exist
                            raise
                        else:
                            #其他类型异常，可重试
                            sleep(5)
                            if retry_times == MAX_RETRY_TIMES:
                                logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                                raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                            continue

                    elif code == TaoOpenErrorCode.REMOTE_ERROR_600:
                        if  e.sub_msg and  'end_modified' in e.sub_msg.encode('utf8'):
                            raise  #在这里重试不合适，到整个任务的地方去重试

                        sleep(5)
                        if retry_times == MAX_RETRY_TIMES:
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        continue

                    elif code == TaoOpenErrorCode.SERVICE_TEMP_UNAVAILABLE:
                        sleep(5)
                        if retry_times == MAX_RETRY_TIMES:
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        continue

                    elif code == TaoOpenErrorCode.INVALID_SESSION_KEY:
                        raise InvalidAccessTokenException("access session expired or invalid")

                    else:
                        raise  e
                else:
                    if retry_times:
                        logger.info("retry success, total_retry time:%i"%retry_times)
                    if (len(args) >= 1):
                        update_api_call_times(tao_model_settings.taobao_client.appKey, args[0].__name__, api_call_requests, api_call_infos)
                    return res
        return __wrapped_func

    return _wrapper_func




