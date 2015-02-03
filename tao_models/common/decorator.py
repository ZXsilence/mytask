#encoding=utf8
"""doc string for module"""
__author__ = 'lym liyangmin@maimiaotech.com'

import os
import commands
import sys
import re
import logging
import traceback
import inspect
import time
from threading import Thread

from time import  sleep
from datetime import datetime
import simplejson as json
import copy

from TaobaoSdk.Exceptions import ErrorResponseException
from pymongo.errors import AutoReconnect, OperationFailure, PyMongoError
from db_exceptions.exceptions import  MongodbException
from TaobaoSdk.Exceptions.SDKRetryException import SDKRetryException

from tao_models.common.exceptions import   DataOutdateException
from tao_models.common.exceptions import  *
from api_server.common.exceptions import ApiSourceError
from busi_service.service.task_service import TaskService
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
def tao_api_exception(MAX_RETRY_TIMES = 6):
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

                    '''
                        异常处理分两块：
                        1、保留自定义业务异常处理，兼容上层的代码
                        2、异常的重试处理,不扔出自定义的业务异常
                    '''

                    if e.code == 1000.1:
                        raise ApiSourceError(e.code,e.sub_code,e.msg,e.sub_msg)
                    if e.code == 1000.2:
                        raise SDKRetryException(code=e.code,sub_code=e.sub_code\
                                ,msg=e.msg,sub_msg=e.sub_msg)
                     
                    #扔出自定义异常
                    if hasattr(e,'params') and e.params:
                        api_method = e.params['method']
                        if api_method == 'taobao.simba.adgroup.update' and e.sub_msg \
                                and u'审核下线的推广组不能手工上下线' in e.sub_msg:
                            raise AdgroupAudictFailedException
                        elif api_method == 'taobao.simba.campaign.budget.get' and e.sub_msg \
                                and u'未找到指定客户' in e.sub_msg:
                            raise CampaignIdNotBelongToUserException
                        elif api_method == 'taobao.simba.campaign.budget.update' and e.sub_msg \
                                and u'限额不得小于' in e.sub_msg:
                            raise CampaignBudgetLessThanCostException
                        elif api_method == 'taobao.simba.campaign.platform.update' and e.sub_msg \
                                and u'用户无资格投放定向推广' in e.sub_msg:
                            raise NonsearchNotAllowedException
                        elif api_method == 'taobao.simba.creative.update' and e.sub_msg \
                                and u'图片不是推广组的图片' in e.sub_msg:
                            raise ImgNotBelongToAdgroupException
                        elif api_method == 'taobao.simba.nonsearch.adgroupplaces.add' and e.sub_msg \
                                and u'当前推广计划不支持该操作' in e.sub_msg:
                            raise NonsearchNotOpenException
                        elif api_method == 'taobao.simba.nonsearch.adgroupplaces.delete' and e.sub_msg \
                                and u'当前推广计划不支持该操作' in e.sub_msg:
                            raise NonsearchNotOpenException
                        elif api_method == 'taobao.simba.nonsearch.adgroupplaces.get' and e.sub_msg \
                                and u'当前推广计划不支持该操作' in e.sub_msg:
                            raise NonsearchNotOpenException

                    #异常状态的重试处理,不扔出自定义的业务异常
                    if (code == 530 or code == 46) and e.sub_code.startswith('isp'): 
                        if retry_times == MAX_RETRY_TIMES:
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        continue
                    #ShopGet.get_shop偶尔会出现用户对应店铺不存在的错误，重试可以解决
                    elif code == 560 and e.sub_msg == '用户对应的店铺不存在':
                        if retry_times == MAX_RETRY_TIMES:
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        continue
                    #存在“未找到指定商品”的问题，经测试部分接口可以重试解决
                    elif code == 15 and e.sub_msg and ('未找到指定商品' in e.sub_msg or 'syncAgent获得宝贝信息接口异常' in e.sub_msg):
                        sleep(5)
                        if retry_times == MAX_RETRY_TIMES:
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        continue
                    #掌中宝接口存在时间戳参数无效的情况，进行重试
                    elif code == 31 and e.msg and 'Invalid timestamp' in e.msg:
                        if retry_times == MAX_RETRY_TIMES:
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        continue
                    elif code == 520 and e.sub_msg and '3分钟后再查询' in e.sub_msg:
                        if retry_times == MAX_RETRY_TIMES:
                            logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        sleep(180)
                        continue
                    elif code == TaoOpenErrorCode.APP_CALL_LIMIT :
                        wait_seconds = int(e.sub_msg.split(' ')[5])
                        if retry_times == MAX_RETRY_TIMES:
                            if wait_seconds > 60:
                                logger.warning("app call limit [%d] seconds"%wait_seconds)
                                raise AppCallLimitedAllDayException("app call limit [%d] seconds"%wait_seconds)
                            else:
                                logger.warning('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                                raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        if wait_seconds > 60:
                            logger.warning("app call limit [%d] seconds"%wait_seconds)
                            raise AppCallLimitedAllDayException("app call limit [%d] seconds"%wait_seconds)
                        else: 
                            if wait_seconds >= 2:
                                logger.debug("app call limit [%d] seconds, need sleep"%wait_seconds)
                            sleep(wait_seconds)
                        continue
                    #isp为开头的错误，只有三种无法重试
                    elif code == TaoOpenErrorCode.REMOTE_ERROR_700 or (e.sub_code and e.sub_code.startswith('isp')):
                        if e.sub_code and u'isp.null-pointer-exception' in e.sub_code:
                            raise #重试无法解决此类异常
                        if e.sub_code and u'isp.top-parse-error' in e.sub_code:
                            raise #重试无法解决此类异常
                        if e.sub_code and u'isp.top-mapping-parse-error' in e.sub_code:
                            raise #重试无法解决此类异常
                        sleep(3)
                        if retry_times == MAX_RETRY_TIMES:
                            if e.sub_code and 'isp.internal-error' in e.sub_code:
                                logger.warning('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            else:
                                logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                            raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                        continue
                    elif code == TaoOpenErrorCode.REMOTE_SERVICE_ERROR:
                        if e.sub_code and e.sub_code == 'isv.invalid-permission':
                            if retry_times == MAX_RETRY_TIMES:
                                logger.error('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                                raise TaoApiMaxRetryException("retry %i times ,but still failed. reason:%s"%(MAX_RETRY_TIMES,e))
                            continue
                        if e.sub_code and e.sub_code.startswith('isv'):
                            #错误码为15，且以isv开头的子错误码，属于业务异常，直接抛出，无需重试
                            raise
                        elif e.sub_code and e.sub_code == "6001":
                            #user not exist
                            raise
                        else:
                            #其他类型异常，可重试
                            sleep(1)
                            if retry_times == MAX_RETRY_TIMES:
                                #isp.internal-error 错误不打印error
                                if e.sub_code and 'isp.internal-error' in e.sub_code:
                                    logger.info('retry failed, total  retry_times:%s, reason:%s'%(retry_times, e))
                                else:
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

                    elif code == 12 and e.sub_msg and '该子帐号无此操作权限' in e.sub_msg and '请通过主帐号设置开通相应权限' in e.sub_msg:
                        raise InvalidAccessTokenException('subuser has no permission')

                    elif code == TaoOpenErrorCode.INVALID_SESSION_KEY:
                        raise InvalidAccessTokenException("access session expired or invalid")
                    elif code == 53 and e.sub_code and 'isv.w2-security-authorize-invalid' in e.sub_code:
                        raise W2securityException('w2-security-authorize-invalid') 
                    else:
                        raise  e
                else:
                    if retry_times:
                        logger.info("retry success, total_retry time:%i"%retry_times)
                    return res
        return __wrapped_func

    return _wrapper_func


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

def get_sys_info(pid):
    res = commands.getstatusoutput('ps aux|grep '+str(pid))[1].split('\n')[0]  
    p = re.compile(r'\s+')  
    l = p.split(res)  
    #'user':l[0],'pid':l[1],'cpu':l[2],'mem':l[3],'vsa':l[4],'rss':l[5],'start_time':l[6]
    curr_mem = float(l[5])/1000.0
    curr_time = time.time()*1000
    return (curr_time,curr_mem)

def analyze(func):
    def __wrappe_func(*args, **kwargs):
        pid = os.getpid()
        start_info = get_sys_info(pid)
        a = func(*args, **kwargs)
        end_info = get_sys_info(pid)
        logger.info('Analyze PID:%s function:%s start_mem:%sMB end_mem:%sMB cost_time:%sms'\
                %(pid,func.__name__,round(start_info[1]),round(end_info[1]),round((end_info[0]-start_info[0]),0)))
        return a
    return __wrappe_func

def task_manage(arg):
    def _wrapper_func(func):
        def __wrappe_func(*args, **kwargs):
            task_name = arg
            params = args[0]
            status = 'doing'
            start_time = datetime.now()
            #减少数据存储量
            save_params = copy.deepcopy(params)
            del save_params['nick']
            del save_params['soft_code']
            #del save_params['sid']
            task_id = save_params.get('task_id',0)
            #如果参数中带有task_id，表示是老任务重试，而非新任务
            if task_id:
                TaskService.upset_task(task_id,{'status':'doing','start_time':start_time})
            else:
                task_id = TaskService.insert_task(task_name,params['nick'],status,params['soft_code'],save_params,start_time)
            try:
                a = func(*args, **kwargs)
            except Exception,e:
                end_time = datetime.now()
                TaskService.upset_task(task_id,{'status':'failed','exception':str(e),'end_time':end_time})
                logger.exception('task error!')
            else:
                end_time = datetime.now()
                TaskService.upset_task(task_id,{'status':'done','result':a,'end_time':end_time})
        return __wrappe_func
    return _wrapper_func


def script_manage(arg):
    def _wrapper_func(func):
        def __wrappe_func(*args, **kwargs):
            task_name = arg
            status = 'doing'
            start_time = datetime.now()
            task_id = TaskService.insert_script_task(task_name,status,start_time)
            try:
                a = func(*args, **kwargs)
            except Exception,e:
                end_time = datetime.now()
                TaskService.upset_script_task(task_id,{'status':'failed','exception':str(e),'end_time':end_time})
                logger.exception('task error!')
                logger.info('%s'%task_name)
            else:
                end_time = datetime.now()
                TaskService.upset_script_task(task_id,{'status':'done','result':a,'end_time':end_time})
        return __wrappe_func
    return _wrapper_func


def server_timeout_check(func):
    def __wrappe_func(*args, **kwargs):
        name = args[0]
        timeout = args[1]
        contact = args[2]
        host = args[3]
        t = Thread(target=func,args=(name,timeout,contact,host))
        t.start()
        t.join(timeout)
        if t.is_alive():
            t._Thread__stop()
            message = '【系统监控】%s响应较慢，超过限额值%s秒(主机:%s)'%(name,timeout,host)
            logger.error(message)
        else:
            message = '【系统监控】%s响应未超时(主机:%s)'%(name,host)
            logger.info(message)
    return __wrappe_func


