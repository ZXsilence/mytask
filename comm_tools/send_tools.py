#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zhoujiebin
@contact: zhoujiebing@maimiaotech.com
@date: 2012-12-10 17:13
@version: 0.0.0
@license: Copyright maimiaotech.com
@copyright: Copyright maimiaotech.com

"""
import sys
import json
import time
import logging
import smtplib, mimetypes
import urllib, urllib2
if __name__ == '__main__':
    sys.path.append('../')

from email.Header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

SEND_COMMAND = 'MT_REQUEST' 
SPID = '5208'
SP_PASSWORD = 'Ad8@@yt011'
DC = '15'
SEND_MSG_URL = 'http://esms.etonenet.com/sms/mt'

#新账号
REG = '101100-WEB-HUAX-307114'
PASSWORD = 'KNXPCLNW'
BALANCE_URL = 'http://www.stongnet.com/sdkhttp/getbalance.aspx'
SEND_MESSAGE_URL = 'http://www.stongnet.com/sdkhttp/sendsms.aspx'
MSG_REPORT = 'http://www.stongnet.com/sdkhttp/getmtreport.aspx'
DIRECTOR = {
            'PHONE':'15068116152',
            'EMAIL':'monitor@maimiaotech.com',
            'SECRET':'Mm@ops2015)'
            }

def send_email_with_text(addressee, text, subject,cc = None, reply_to=None):
    """发送文本email"""

    msg = MIMEMultipart()
    msg.attach(MIMEText(text, _charset='utf-8'))
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = DIRECTOR['EMAIL']
    to_list = [ str(adr).strip() for adr in addressee.split(';')] if type(addressee) in [str,type(u'')] else addressee
    msg['To'] = ';'.join(to_list) 
    cc_list = []
    if cc:
        cc_list = [ str(adr).strip() for adr in cc.split(';')] if type(cc) in [str,type(u'')] else cc 
        msg['Cc'] = ';'.join(cc_list)
    if reply_to:
        msg.add_header('reply-to',reply_to)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.mxhichina.com', 25) 
        smtp.login(msg['From'], DIRECTOR['SECRET'])
        smtp.sendmail(msg['From'], list(set(to_list+cc_list)), msg.as_string())
    except Exception,e:
        print e

def send_email_with_html(addressee, html, subject,cc = None,reply_to=None):
    """发送html email"""

    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = DIRECTOR['EMAIL']
    to_list = [ str(adr).strip() for adr in addressee.split(';')] if type(addressee) in [str,type(u'')] else addressee
    msg['To'] = ';'.join(to_list) 
    cc_list = []
    if cc:
        cc_list = [ str(adr).strip() for adr in cc.split(';')] if type(cc) in [str,type(u'')] else cc 
        msg['Cc'] = ';'.join(cc_list)
    if reply_to:
        msg.add_header('reply-to',reply_to)
    html_att = MIMEText(html, 'html', 'utf-8')
    msg.attach(html_att)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.mxhichina.com', 25) 
        smtp.login(msg['From'], DIRECTOR['SECRET'])
        smtp.sendmail(msg['From'], list(set(to_list + cc_list)), msg.as_string())
    except Exception,e:
        print e

def send_email_with_file(addressee, text, subject, file_list):
    """发送file email"""

    msg = MIMEMultipart()
    msg.attach(MIMEText(text, _charset='utf-8'))
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = DIRECTOR['EMAIL']
    msg['To'] = addressee

    for file_name in file_list:
        ctype, encoding = mimetypes.guess_type(file_name)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        
        attachment = MIMEImage((lambda f: (f.read(), f.close())) \
                (open(file_name, 'rb'))[0], _subtype =subtype)
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(attachment)

    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.mxhichina.com', 25) 
        smtp.login(msg['From'], DIRECTOR['SECRET']) 
        smtp.sendmail(msg['From'], addressee, msg.as_string())
    except Exception,e:
        print e

def _toHex(str,charset):
    if type(str) == type('type'):
        str = str.decode('utf-8')
    s = str.encode(charset)
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    return reduce(lambda x,y:x+y, lst)

def _parse_sms_response(message):
    dict = {}
    response_list = message.split('&')
    for info in response_list:
        key_value = info.split('=')
        dict[key_value[0]] = key_value[1]   
    return dict

def send_sms_old(cellphone, text, retry_times=3):
    """发送短信"""

    retry_times -= 1
    if retry_times < 0:
        logging.error('send message to %s unsuccessfully'%(cellphone,))
        print 'send message to %s unsuccessfully'%(cellphone,)
        return
    dict = {}
    dict['command'] = SEND_COMMAND
    dict['spid'] = SPID
    dict['sppassword'] = SP_PASSWORD
    dict['da'] = '86'+cellphone
    dict['dc'] = DC 
    dict['sm']  = _toHex(text,'gbk')
    url_params = urllib.urlencode(dict)
    try:
        response = urllib2.urlopen(SEND_MSG_URL,url_params)
        dict = _parse_sms_response(response.read())
        if dict.get('mterrcode',None) != '000':
            logging.error('send message to %s unsuccessfully:response error'%(cellphone,))
            logging.error('error dict: %s' % (str(dict)))
            print 'send message to %s unsuccessfully:response error'%(cellphone,)
            print 'error dict: %s' % (str(dict))
            send_sms_old(cellphone,text,retry_times)
    except urllib2.HTTPError,e:
        logging.error('send message to %s unsuccessfully:url connect error'%(cellphone,))
        print 'send message to %s unsuccessfully:url connect error'%(cellphone,)
        send_sms_old(cellphone,text,retry_times)
    except Exception,e:
        logging.error('send message to %s unsuccessfully:server error'%(cellphone,))
        print 'send message to %s unsuccessfully:server error'%(cellphone,)
        send_sms_old(cellphone,text,retry_times)

def get_balance():
    url_params = urllib.urlencode({'reg':REG,'pwd':PASSWORD})
    response = urllib2.urlopen(BALANCE_URL,url_params)
    data = _parse_sms_response(response.read())
    balance = 0
    if data['result'] == '0':
        balance = int(data['balance'])
    return balance

def get_msg_report():
    url_params = urllib.urlencode({'reg':REG,'pwd':PASSWORD})
    response = urllib2.urlopen(MSG_REPORT,url_params)
    report = {}
    data = _parse_sms_response(response.read())
    if data['result'] == '0':
        report.update(data)
    return report

def send_sms(cellphone, text, retry_times=3):
    """发送短信"""

    retry_times -= 1
    if retry_times < 0:
        logging.error('send message to %s unsuccessfully'%(cellphone,))
        print 'send message to %s unsuccessfully'%(cellphone,)
        return
    if type(text) == type(u''):
        text = text.encode('utf-8')
    if '【麦苗】' not in text:
        text += '【麦苗】'
    text = filter_words(text)
    if type(cellphone) == type([]):
        cellphone = ','.join(cellphone)
    dict = {}
    dict['reg'] = REG 
    dict['pwd'] = PASSWORD
    dict['phone'] = cellphone
    dict['content']  = text
    dict['sourceadd']  = None
    url_params = urllib.urlencode(dict)
    print text
    try:
        response = urllib2.urlopen(SEND_MESSAGE_URL,url_params)
        dict = _parse_sms_response(response.read())
        if dict.get('result',None) != '0':
            logging.error('send message to %s unsuccessfully:response error,msg:%s'%(cellphone,dict))
            print 'send message to %s unsuccessfully:response error,msg:%s'%(cellphone,dict)
            send_email_with_html('xieguanfu@maimiaotech.com', text, '短信发送失败')
    except urllib2.HTTPError,e:
        logging.error('send message to %s unsuccessfully:url connect error'%(cellphone,))
        print 'send message to %s unsuccessfully:url connect error'%(cellphone,)
        #send_sms(cellphone,text,retry_times)
    except Exception,e:
        logging.error('send message to %s unsuccessfully:server error'%(cellphone,))
        print 'send message to %s unsuccessfully:server error'%(cellphone,)
        #send_sms(cellphone,text,retry_times)

def filter_words(msg):
    words = [('**','--'),('服务','服&务'),('双11','双&11'),('黄色','黄&色'),('双十一','双&十&一'),('转化','转&化'),\
             ('傻逼','傻&逼'),('脑残','脑&残'),('二货','二&货'),('骚扰','骚&扰')]
    for word in words:
        msg = msg.replace(word[0],word[1])
    return msg

if __name__ == '__main__':
    #send_email_with_html('115965829@qq.com;xieguanfu@maimiaotech.com', '新邮件切换', '新邮件地址')
    #send_email_with_html(['115965829@qq.com','xieguanfu@maimiaotech.com'], '你收到邮件了吗', 'subject')
    #send_email_with_html('dongxuanliang@maimiaotech.com','网络延迟','标题',['dongxl123@163.com'],'245684715@qq.com')
    print get_msg_report()
    print get_balance()
    
    #send_sms('18612251466','省油宝会员激活验证码:988280。请勿告知他人并确认申请是您本人操作。')
    #send_sms('15068116152','麦苗提醒:尊敬的水冰月0426，您好！您的省油宝软件将于3天后到期，过期后软件推广设置将被清空，请尽快续费以免影响推广。【麦苗】 ')
    #send_sms('13732249864','麦苗提醒:尊敬的水冰月0426，您好！您的省油宝软件将于3天后到期，过期后软件推广设置将被清空，请尽快续费以免影响推广。【麦苗】 ')
    #send_sms(DIRECTOR['PHONE'], u'省油宝新评价:小--漫,评分:1,用了两个多月 再来评价的！说句真心话，没有一点用！ 烧出去的关键词比系统自动添加的还差！每天开出去200多块左')
    #send_sms(DIRECTOR['PHONE'], '尊敬的客户你好！您的省油宝长期未登陆导致不能正常优化,请您及时登陆省油宝,方便我们进行优化!')
