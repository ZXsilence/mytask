#!/usr/bin/env python
#encoding=utf8
import os
import sys
import datetime
import sys
if not '/module/path' in sys.path:
    sys.path.append('/module/path')

from Boss4Python import Boss4Python 

if __name__ == "__main__":
	boss = Boss4Python()
	boss.init("/home/data/BOSS/conf/boss.conf")
	for i in range(1,10000):
		word = u"你好中国mp3"
		tokens = boss.process(word.encode('utf8')) 
		for item in tokens :
			items = item.split("\1")
			print items
		print "==========="
