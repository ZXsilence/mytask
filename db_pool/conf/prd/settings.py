#encoding=utf8
# Django settings for xuanciw project.
#rds实例1的连接池配置
RDS1 = {
         'pool_addr':{
                 'HOST':'10.242.173.131',
                 'PORT':4040,
                 'USER':'maimiao_ops',
                 'PASSWD':'maimiaoadmin2014' 
                 }
             ,
         'db_list':['adgroups','api','api_record',\
                 'auth_center','campaign','campaigns',\
                 'crm','dbtest','items','keywords',\
                 'longtail','mobileapp','mysql','performance',\
                 'qianniu','shop_info','syb_comm_info',\
                 'syb_web','syb_webpage' ,'sys_info','taoci'\
                 ,'xiangqing','xuanciw'
                 ]
        }

#rds2实例连接池配置
RDS2 = {
         'pool_addr':{
                 'HOST':'121.199.170.159',
                 'PORT':4041,
                 'USER':'maimiao_ops',
                 'PASSWD':'maimiaoadmin2014' 
                 },
             ,
         'db_list':[
              'keywords_deleted','access_records','dbtest'
             ]
        }
