#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: tanglingling
@contact: tanglingling@maimiaotech.com
@date: 2017-09-26 15:46
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import logging
logger2 = logging.getLogger("api_virtual")
import time
import copy
from datetime import datetime
import datetime as dt
from exceptions import ApiVirtualResponseException
from replace_base import ReplaceBase
import operator

#导入db_model
class ReplaceSimbaRtrptBidwordGet(ReplaceBase):
    '''
    关键词实时报表
    '''


