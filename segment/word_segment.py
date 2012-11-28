#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Chen Ke
@contact: chenke@MaimiaoTech.com
@date: 2012-06-26 10:28
@version: 0.0.0
@license: Copyright MaimiaoTech.com
@copyright: Copyright MaimiaoTech.com

"""
import os
import sys
import string
import mimetypes
import cStringIO as StringIO
import platform
import copy

curr_path = os.path.dirname(__file__)
sys.path.append(os.path.join(curr_path,'./gen-py/'))
sys.path.append(os.path.join(curr_path,'./boss/'))

from settings_segment import BOSS_CONF_FILE, OS_NAME, BOSS_THRIFT

if OS_NAME in platform.platform():
    from Boss4Python import Boss4Python 
else:
    from maimiaotech import Segment
    from maimiaotech.ttypes import *
    from thrift import Thrift
    from thrift.transport import TSocket
    from thrift.transport import TTransport
    from thrift.protocol import TBinaryProtocol


class WordSegment(object):

    def __init__(self): 
        if OS_NAME in  platform.platform():
            self.boss = Boss4Python()
            self.boss.init(BOSS_CONF_FILE)
        else:
            self.transport = TSocket.TSocket(BOSS_THRIFT['host'], BOSS_THRIFT['port'])
            self.transport = TTransport.TBufferedTransport(self.transport)
            self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
            self.client = Segment.Client(self.protocol)
            self.transport.open()

    def __del__(self):
        try:
            if not OS_NAME in platform.platform():
                self.transport.close()
        except Exception, data:
            pass

    def do_segment(self, words):
        if isinstance(words,unicode):
            words = words.encode('utf-8')
        word_list= []
        if OS_NAME in  platform.platform():
        # seg using boss4python
            result = self.boss.process(words) 
            for word in result:
                word_list.append(word)

        else:
        # seg via thrift
            term_list = self.client.seg_process(words)
            for term in term_list:
                word_element = str(term.key)+'\1'+str(term.nType)+'\1'+str(term.nWeight)
                word_list.append(word_element)

        return word_list 


if __name__ == '__main__':
    word = u'新款秋装2012'
    segmentor = WordSegment()
    word_list = segmentor.do_segment(word)

    for word in word_list:
        print word
        print type(word)
