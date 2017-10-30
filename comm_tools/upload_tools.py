#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: dongxuanliang
@contact: dongxuanliang@maimiaotech.com
@date: 2015-02-25 15:44
@version: 2015
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import os
import time
from datetime import datetime
import base64
import urllib
import re
import urllib2
import paramiko
from tao_models.picture_upload import PictureUpload
from tao_models.picture_category_get import PictureCategoryGet
from tao_models.picture_category_add import PictureCategoryAdd
from PIL import Image
CATEGORY_SYB_TOUTU = '省油宝宝贝投图'
CATEGORY_SYB_ZHUTU = '省油宝商品主图'


def upload_file(file_obj,root_path,category,proj_path,mode=None,with_scp=False):
    """
    file_obj: 文件对象
    root_paht：上传根目录
    category：文件类型
    mode：文件目录索引方式，按天索引或者按其他方式索引（目前未实现,默认不索引）
    with_scp：scp到静态资源服务器
    proj_path：项目路径
    整个文件的绝对路径为:root+category+'/'+mode_path+file_name
    远程文件的绝对路径为:**+proj_path+category+'/'+mode_path+file_name
    """
    #创建文件路径
    file_name = file_append_timestamp(file_obj.name)
    mode_path=''
    ext_path= category + '/' + mode_path
    package_path = root_path + ext_path
    if not os.path.exists(package_path):
        os.makedirs(package_path)
    abs_file_path = package_path + file_name
    #保存文件
    fw = open(abs_file_path,'wb+')
    for chunk in file_obj.chunks():
        fw.write(chunk)
    fw.close()
    relative_file_path = ext_path + file_name
    #scp到静态资源服务器
    #标识是否上传成功
    flag = True
    if with_scp:
        flag = scp_file(root_path=root_path,ext_path=ext_path,file_name=file_name,dest_path='/alidata1/static/'+proj_path)
        #删除本地无用文件
        os.remove(abs_file_path)
    return flag,relative_file_path

def file_append_timestamp(file_name):
    timestamp=int(time.time())
    buckets=file_name.split('.')
    if len(buckets)==1:
        return '%s_%s' % (file_name,timestamp)
    suffix = buckets[-1]
    pre_name = '.'.join(buckets[:-1])
    return '%s_%s.%s' % (abs(hash(pre_name)),timestamp,suffix)

def scp_file(root_path, ext_path, file_name,servers=['10.132.174.13','10.132.174.148'],port=22, username='static',password='Static_maimiao2014',dest_path='/home/static/',max_retry_times=5):
    for server in servers:
        retry_times=0
        while True:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=server, port=port, username=username, password=password)
                ssh.exec_command('mkdir -p '+dest_path + ext_path)
                sftp = ssh.open_sftp()
                if type(file_name) == list:
                    for fname in file_name:
                        sftp.put(root_path + ext_path + fname,dest_path + ext_path + fname)
                else:
                    sftp.put(root_path + ext_path + file_name,dest_path + ext_path + file_name)
                ssh.close()
            except Exception,e:
                print root_path + ext_path + file_name,dest_path + ext_path + file_name
                print e
                retry_times+=1
                if retry_times > max_retry_times:
                    return False
                time.sleep(1)
                continue
            break
    return True

def upload_activity_img_with_base64(root_path,file_obj):
    if not file_obj:
        return
    file_name = '%s.png'%(time.mktime(datetime.now().timetuple()))
    package_path = os.path.join(root_path,'feedback')
    if not os.path.exists(package_path):
        os.makedirs(package_path)
    file_path = os.path.normpath(os.path.join(package_path,'%s'%file_name))
    destination = open(file_path,'wb+')
    img_data = urllib.unquote_plus(file_obj.replace('\n',''))
    img_data = img_data[re.search(';base64',img_data).start()+8:]
    destination.write(base64.b64decode(img_data))
    destination.close()
    rsp = PictureUpload.upload_img('麦苗科技001',file_path)
    return rsp['picture']['picture_path']

def upload_customer_img_with_base64(root_path, nick, file_obj, img_target=None, has_upload_img_ability=False):
    if not file_obj:
        return None, None
    file_name = '%s.png'%(time.mktime(datetime.now().timetuple()))
    now = datetime.now()
    package_path = os.path.join(root_path,'%s/%s/%s'%(now.year,now.month,now.day))
    if not os.path.exists(package_path):
        os.makedirs(package_path)
    file_path = os.path.normpath(os.path.join(package_path,'%s'%file_name))
    destination = open(file_path,'wb+')
    img_data = urllib.unquote_plus(file_obj.replace('\n', ''))
    img_data = img_data[re.search(';base64', img_data).start()+8:]
    destination.write(base64.b64decode(img_data))
    destination.close()
    import Image, ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    image = Image.open(file_path)
    out = image.resize((image.size[0],image.size[1]),Image.ANTIALIAS)
    out.save(file_path, 'JPEG', quality=90)
    if img_target == 'is_toutu':
        category_id = _img_kongjian_add_category(nick, CATEGORY_SYB_TOUTU)
    elif img_target == 'is_zhutu':
        category_id = _img_kongjian_add_category(nick, CATEGORY_SYB_ZHUTU)
    else:
        category_id = 0
    rsp = PictureUpload.upload_img(nick,file_path, category_id)
    return rsp['picture']['picture_path'], rsp['picture']['picture_id']


def _img_kongjian_add_category(nick, category_name):
    category_list = PictureCategoryGet.get_picture_category_name(nick, category_name)
    for category in category_list:
        if category['picture_category_name'] == category_name:
            category_id = category['picture_category_id']
            break
    else:
        res = PictureCategoryAdd.add_picture_category(nick, category_name)
        category_id = res['picture_category_id']
    return category_id


def upload_customer_img_with_base64_new(root_path,nick,file_obj):
    if not file_obj:
        return
    file_name = '%s.png'%(time.mktime(datetime.now().timetuple()))
    now = datetime.now()
    package_path = os.path.join(root_path,'%s/%s/%s'%(now.year,now.month,now.day))
    if not os.path.exists(package_path):
        os.makedirs(package_path)
    file_path = os.path.normpath(os.path.join(package_path,'%s'%file_name))
    destination = open(file_path,'wb+')
    img_data = file_obj.replace('\n','')
    img_data = img_data[re.search(';base64',img_data).start()+8:]
    destination.write(base64.b64decode(img_data))
    destination.close()
    rsp = PictureUpload.upload_img(nick,file_path)
    return rsp['picture']['picture_path']

def upload_yzb_creative_img_with_base64(root_path,nick,img_data):
    if not img_data:
        return
    file_name = '%s.png'%(time.mktime(datetime.now().timetuple()))
    now = datetime.now()
    package_path = os.path.join(root_path,'%s/%s/%s'%(now.year,now.month,now.day))
    if not os.path.exists(package_path):
        os.makedirs(package_path)
    file_path = os.path.normpath(os.path.join(package_path,'%s'%file_name))
    destination = open(file_path,'wb+')
    if 'http' in img_data:
        img_data = urllib2.urlopen(img_data).read()
    else:
        img_data = img_data[re.search(';base64',img_data).start()+8:]
        img_data = base64.b64decode(img_data)
    destination.write(img_data)
    destination.close()
    image_size = "_".join(map(lambda x:str(x),Image.open(file_path).size))
    return file_path,image_size

if __name__ == '__main__':
    print file_append_timestamp('111_1')
    #scp_file('/home/dongxl/','','test2',['121.199.172.249','121.199.172.86'],22,'static','Static_maimiao2014','/home/static/assets/crm/1/',1)
