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
from TriggerPoint import TriggerPointGenerator



if __name__ =="__main__":
    attributeList = []
    attributeList.append({'attribute_value':u'欧博恒','attribute_value_id':'v123', 'attribute_key':u'品牌', 'attribute_key_id':'k123'})
    attributeList.append({'attribute_value':u'2012新款','attribute_value_id':'v123', 'attribute_key':u'品牌', 'attribute_key_id':'k123'})
    attributeList.append({'attribute_value':u'全场包邮','attribute_value_id':'v123', 'attribute_key':u'品牌', 'attribute_key_id':'k123'})
    attributeList.append({'attribute_value':u'中袖','attribute_value_id':'v123', 'attribute_key':u'品牌', 'attribute_key_id':'k123'})
    attributeList.append({'attribute_value':u'修身型','attribute_value_id':'v123', 'attribute_key':u'品牌', 'attribute_key_id':'k123'})
    tpGenerator = TriggerPointGenerator();
    attributeList = tpGenerator.attribute_trigger_point(attributeList)
    print "list:", attributeList
