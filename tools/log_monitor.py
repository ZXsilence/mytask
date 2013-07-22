#! /usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import datetime
import sys
import json
import time
import smtplib, mimetypes
import urllib, urllib2
import time
import logging
from send_tools import SendTools
from datetime import datetime
def usage(argv0):
    print argv0 + " -f file to monitor"
def getLogger():
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter) 
    logger.addHandler(ch)
    return logger
class SpeedLimiter:
    def __init__(self, min_interval):
        self.min_interval = min_interval
        self.call_times = 0
        self.call_limits = 0
        self.last_time = 0

    def need_limit(self, timestamp = 0):
        self.call_times = self.call_times + 1
        if (timestamp == 0):
            timestamp = float(datetime.now().strftime("%s"))
        now = timestamp
        interval = now - self.last_time
        if (interval >= self.min_interval):
            self.call_limits = self.call_times
            self.call_times = 0
            self.last_time = timestamp
            return False
        elif self.call_times == 1:
            return False
        else:
            return True;

    def get_call_limits(self):
        return self.call_limits

    def info(self):
        if self.call_limits == 1:
            return ""
        elif self.call_times == 1:
            return ""
        else:
            return str(self.call_limits) + " messages in " + str(self.min_interval) + " seconds"

#2013-07-03 16:38:04,261 INFO mylogger.<module>:12    message info
#[2013-07-03 14:03:11,909: DEBUG/MainProcess] request SimbaRptAdgroupbaseGetRequest
class LogMonitor:
    def __init__(self, file, before_second, phone, email, secret, min_interval, tag_name, filter_file_name=None):
        self.file = file
        self.before_second = before_second
        self.logger = getLogger()
        self.email = email
        self.phone = phone
        self.send_tools = SendTools(phone, email, secret, self.logger)
        self.limiter_error = SpeedLimiter(min_interval)
        self.limiter_warn = SpeedLimiter(min_interval)
        self.tag_name = tag_name
        self.filter = self.get_filter(filter_file_name)

    def get_filter(self, filter_file_name):
        filter = []
        if filter_file_name :
            filter_file = open(filter_file_name)
            while True:
                filter_word = filter_file.readline()
                if not filter_word:
                    return filter
                if filter_word[0] == '#':
                    continue
                strlen = len(filter_word)
                filter_word = filter_word[:strlen-1]
                filter.append(filter_word)
            for filter_word in filter:
                print filter_word
        return filter

    def do_match_filter(self, line):
        for filter_word in self.filter:
            if line.find(filter_word) != -1:
                return True
        return False

    def parse_line(self, line):
        time_content = None
        log_timestamp = None
        level = None
        message = None
        success = False
        if len(line) < 21:
            return success, time_content, level, message
        if line[0] == '[':
            time_length = 20
            time_begin = 1
            level_begin = 26
            split_char = '/'
        else :
            time_length = 19
            time_begin = 0
            level_begin = 24
            split_char = ' '
            
        time_content = line[time_begin:time_length]
        line_array = line[level_begin:].split(split_char)
        level = line_array[0]
        message = line[(level_begin + len(level)):]
        success = True
        return success, time_content, level, message


    def send_message(self, line):

        subject = None
        text = None
        send_sms = False
        send_email = False
        try:
            
            success, time_content, level, message = self.parse_line(line)
            if not success:
                return subject, text, send_sms, send_email
#            if len(line) < 20:
#                return subject, text, send_sms, send_email

#            time_content = line[0:19]
#            log_timestamp = time.mktime(time.strptime(time_content, "%Y-%m-%d %H:%M:%S"))
            log_timestamp = time.mktime(time.strptime(time_content, "%Y-%m-%d %H:%M:%S"))
            now_timestamp = float(datetime.now().strftime("%s"))
            if now_timestamp - log_timestamp > self.before_second:
                return subject, text, send_sms, send_email

            #print "log " + str(log_timestamp) + " now " + str(now_timestamp)
#            line_array = line[24:].split()
#            level = line_array[0]
#            message = line[(24 + len(level)):]
            #print "level ["+ str(level) + "] message [" + str(message) + "]"
            if cmp(level, "ERROR") == 0:
                if not self.do_match_filter(message) and not self.limiter_error.need_limit(log_timestamp):
                    subject = level + " log at " + time_content + " in " + self.tag_name + " " + self.limiter_error.info()
                    send_email = True
                    send_sms = True
            elif cmp(level, "WARNING") == 0:
                if not self.do_match_filter(message) and not self.limiter_warn.need_limit(log_timestamp):
                    subject = level + " log at " + time_content + " in " + self.tag_name + " " + self.limiter_warn.info()
                    send_email = True

            if send_email:
                text = str(message)
                self.send_tools.send_email_with_text(self.email, text, subject)
            if send_sms:
                text = str(message)
                self.send_tools.send_sms(self.phone, "title : " + subject + " text : " + text)

            return subject, text, send_sms, send_email

        except Exception, e:
            print str(e)
            return subject, text, send_sms, send_email


    def monitor(self):
        #log_file = open(self.log_name, "r")
        while True:
            line = self.file.readline()
            try:
                if not line:
                    print "end of file"
                    break
                self.send_message(line)
            except Exception, e:
                print str(e)
                continue
                

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "f:b:t:i:F:h", ['file=', "before=", "tag=", 'interval=', 'filter=', 'help'])
    before_second = 0
    file_name = None
    tag_name = "demo"
    interval = 10
    filter_file_name = None
    for key,value in opts:
        if key in ('-f', '--file'):
            file_name = value
        elif key in ('-b', '--before'):
            before_second = int(value)
        elif key in ('-t', '--tag_name'):
            tag_name = value
        elif key in ('-i', '--interval'):
            interval = int(value)
        elif key in ('-F', '--filter'):
            filter_file_name = value
        elif key in ('-h', '--help'):
            usage(argv[0])
            sys.exit(1)
    if file_name != None:
        log_file = open(file_name, "r")
    else:
        log_file = sys.stdin
    monitor = LogMonitor(log_file, before_second, '18658837169', 'luoyan@maimiaotech.com', '62717038', interval, tag_name, filter_file_name)
    monitor.monitor()
