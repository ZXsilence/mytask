#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import unittest
import logging
sys.path.append('../tools/')
import send_tools
from send_tools import SendTools
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
tools = SendTools(phone, email, secret, logger)

class SendToolsTestCase(unittest.TestCase):

    def test_send_email_with_text(self):
        tools.send_email_with_text(email, 'text', 'subject')

    def test_send_sms(self):
        tools.send_sms(phone, u'测试短信')

if __name__ == '__main__':
    import doctest
    doctest.testmod(send_tools)
    unittest.main()
