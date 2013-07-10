#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import unittest
import logging
sys.path.append('../tools/')
import send_tools
from send_tools import SendTools
import log_monitor
from log_monitor import LogMonitor, SpeedLimiter
import time
from datetime import datetime
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

phone = '18658837169'
email = 'luoyan@maimiaotech.com'
secret = '62717038'
class LogMonitorTestCase(unittest.TestCase):

    def test_speed_limit(self):
        limiter = SpeedLimiter(5)
        self.assertEquals(limiter.need_limit(10), False)
        self.assertEquals(limiter.get_call_limits(), 1)
        self.assertEquals(cmp("", limiter.info()), 0)

        self.assertEquals(limiter.need_limit(10), False)
        self.assertEquals(limiter.get_call_limits(), 1)
        self.assertEquals(cmp("", limiter.info()), 0)
        
        self.assertEquals(limiter.need_limit(10), True)
        self.assertEquals(limiter.get_call_limits(), 1)

        self.assertEquals(limiter.need_limit(14), True)
        self.assertEquals(limiter.get_call_limits(), 1)
        
        self.assertEquals(limiter.need_limit(15), False)
        self.assertEquals(limiter.get_call_limits(), 4)
        self.assertEquals(cmp("4 messages in 5 seconds", limiter.info()), 0)
        
        self.assertEquals(limiter.need_limit(15), False)
        self.assertEquals(limiter.get_call_limits(), 4)
        self.assertEquals(cmp("", limiter.info()), 0)
        
        self.assertEquals(limiter.need_limit(15), True)
        self.assertEquals(limiter.get_call_limits(), 4)
#        self.assertEquals(cmp("", limiter.info()), 0)
    def test_parse_line(self):
        now_timestamp = float(datetime.now().strftime("%s"))
        log_timestamp = time.mktime(time.strptime("2013-07-04 10:42:12", "%Y-%m-%d %H:%M:%S"))
        before_second = now_timestamp - log_timestamp + 1000
        monitor = LogMonitor(sys.stdin, before_second, phone, email, secret, 10, "testcase")
        success, time_content, level, message = monitor.parse_line('2013-07-03 16:38:04,261 INFO mylogger.<module>:12    message info')
        self.assertEquals(success, True)
        self.assertEquals(time_content, '2013-07-03 16:38:04')
        self.assertEquals(level, 'INFO')
        self.assertEquals(message, ' mylogger.<module>:12    message info')

        success, time_content, level, message = monitor.parse_line('[2013-07-03 14:03:11,909: DEBUG/MainProcess] request SimbaRptAdgroupbaseGetRequest')
        self.assertEquals(success, True)
        self.assertEquals(time_content, '2013-07-03 14:03:11')
        self.assertEquals(level, 'DEBUG')
        self.assertEquals(message, '/MainProcess] request SimbaRptAdgroupbaseGetRequest')

    def test_send_message(self):
        now_timestamp = float(datetime.now().strftime("%s"))
        log_timestamp = time.mktime(time.strptime("2013-07-04 10:42:12", "%Y-%m-%d %H:%M:%S"))
        before_second = now_timestamp - log_timestamp + 1000
        monitor = LogMonitor(sys.stdin, before_second, phone, email, secret, 10, "testcase")

        subject, text, send_sms, send_email = monitor.send_message("2013-07-04 10:42:12,045 INFO mylogger.<module>:12    message info")
        self.assertEquals(subject, None)
        self.assertEquals(text, None)
        self.assertEquals(send_sms, False)
        self.assertEquals(send_email, False)

        subject, text, send_sms, send_email = monitor.send_message("2013-07-04 10:42:12,045 ERROR mylogger.<module>:13    message error")
        self.assertEquals(subject, "ERROR log at 2013-07-04 10:42:12 in testcase ")
        self.assertEquals(text, " mylogger.<module>:13    message error")
        self.assertEquals(send_sms, True)
        self.assertEquals(send_email, True)

        subject, text, send_sms, send_email = monitor.send_message("2013-07-04 10:42:12,045 WARNING mylogger.<module>:14    message warning")
        self.assertEquals(subject, "WARNING log at 2013-07-04 10:42:12 in testcase ")
        self.assertEquals(text, " mylogger.<module>:14    message warning")
        self.assertEquals(send_sms, False)
        self.assertEquals(send_email, True)

        subject, text, send_sms, send_email = monitor.send_message("2013-07-04 10:42:12,045 ERROR mylogger.<module>:15    message exception")
        self.assertEquals(subject, "ERROR log at 2013-07-04 10:42:12 in testcase ")
        self.assertEquals(text, " mylogger.<module>:15    message exception")
        self.assertEquals(send_sms, True)
        self.assertEquals(send_email, True)

        subject, text, send_sms, send_email = monitor.send_message("2013-07-04 10:42:12,045 ERROR mylogger.<module>:15    message exception")
        self.assertEquals(subject, None)
        self.assertEquals(text, None)
        self.assertEquals(send_sms, False)
        self.assertEquals(send_email, False)

        subject, text, send_sms, send_email = monitor.send_message("2013-07-04 10:42:12,045 ERROR mylogger.<module>:15    message exception")
        self.assertEquals(subject, None)
        self.assertEquals(text, None)
        self.assertEquals(send_sms, False)
        self.assertEquals(send_email, False)

        subject, text, send_sms, send_email = monitor.send_message("2013-07-04 10:44:22,045 WARNING mylogger.<module>:14    message warning")
        self.assertEquals(subject, "WARNING log at 2013-07-04 10:44:22 in testcase ")
        self.assertEquals(text, " mylogger.<module>:14    message warning")
        self.assertEquals(send_sms, False)
        self.assertEquals(send_email, True)

        subject, text, send_sms, send_email = monitor.send_message("2013-07-04 10:44:22,045 WARNING mylogger.<module>:14    message warning2")
        self.assertEquals(subject, "WARNING log at 2013-07-04 10:44:22 in testcase ")
        self.assertEquals(text, " mylogger.<module>:14    message warning2")
        self.assertEquals(send_sms, False)
        self.assertEquals(send_email, True)

        subject, text, send_sms, send_email = monitor.send_message("2013-07-04 10:44:12,045 ERROR mylogger.<module>:15    message exception")
        self.assertEquals(subject, "ERROR log at 2013-07-04 10:44:12 in testcase 4 messages in 10 seconds")
        self.assertEquals(text, " mylogger.<module>:15    message exception")
        self.assertEquals(send_sms, True)
        self.assertEquals(send_email, True)

        subject, text, send_sms, send_email = monitor.send_message("Nonecontent")
        self.assertEquals(subject, None)
        self.assertEquals(text, None)
        self.assertEquals(send_sms, False)
        self.assertEquals(send_email, False)

if __name__ == '__main__':
    import doctest
    doctest.testmod(log_monitor)
    unittest.main()
