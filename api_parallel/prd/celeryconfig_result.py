#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2014-03-26 11:11
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
from celery.schedules import crontab
BROKER_URL = 'amqp://guest:guest@mm_yun10_in:30005//'
CELERYD_POOL_RESTARTS = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_ACKS_LATE = True
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_RESULT_BACKEND = 'mongodb://mm_yun11:31000;mm_yun10:31000/' 
#CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost:5672//'
CELERY_TASK_RESULT_EXPIRES = 43200 
CELERY_ROUTES = {
        'get_rpt_adgroupkeywordbase_list':{'queue':'api_parallel'},
        'get_rpt_adgroupkeywordeffect_list':{'queue':'api_parallel'},
        'get_rpt_adgroupbase_list':{'queue':'api_parallel'},
        'get_rpt_adgroupeffect_list':{'queue':'api_parallel'},
        'get_item_list_by_page':{'queue':'api_parallel'},
        'get_item_list_by_num_iids':{'queue':'api_parallel'},
        'get_keywords_split_qscore':{'queue':'api_parallel'},
}
CELERYBEAT_SCHEDULE = {
        'clean_db': {
                    'task': 'celery.backend_cleanup',
                    'schedule': crontab(hour=0, minute=0, day_of_month='*/2'),
                },
}
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False






