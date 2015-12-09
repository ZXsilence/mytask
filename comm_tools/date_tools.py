#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: dongxuanliang
@contact: dongxuanliang@maimiaotech.com
@date: 2015-03-02 13:14
@version: 2015
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import datetime as dt
import calendar

def get_week_date(base_date,weekday,week_delta):
    """获取周几的日期，base_date：基准时间点，weekday：calendar.Monday..SUNDAY,week_delta:-1代表上周，1代表下周"""
    base_weekday = base_date.weekday()
    return base_date + dt.timedelta(days = weekday-base_weekday+7*week_delta)

def add_months(dt,months):
    """时间+-月份"""
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day,calendar.monthrange(year,month)[1])
    return dt.replace(year=year, month=month, day=day)
