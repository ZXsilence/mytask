#encoding=utf8
__author__ = 'lym liyangmin@maimiaotech.com'


import sys
import os
import logging
import logging.config
from datetime import  datetime


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))

from tao_models.conf import settings 
if __name__ == '__main__':
    coll = (settings.api_conn)['api_record']['api_record']
    coll.ensure_index('source')
    coll.ensure_index('date')
    coll.ensure_index('method')
    coll.ensure_index('total_times')
    coll.ensure_index('success_times')
    coll.ensure_index('fail_times')

