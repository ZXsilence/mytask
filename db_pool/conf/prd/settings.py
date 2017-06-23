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
                 'crm','dbtest','keywords',\
                 'longtail','mobileapp','mysql','performance',\
                 'qianniu','shop_info','syb_comm_info',\
                 'syb_web','busi','syb_webpage' ,'sys_info','taoci'\
                 ,'xiangqing','xuanciw','syb_layer','rpt_cache','busi_back','workflow','yzb','advert','auto_celery','yzb_busi','yzb_creatives'
                 ]
        }

#rds2实例连接池配置
RDS2 = {
         'pool_addr':{
                 'HOST':'10.242.173.131',
                 'PORT':4041,
                 'USER':'maimiao_ops2',
                 'PASSWD':'maimiaoadmin2014' 
                 }
             ,
         'db_list':[
              'access_records','dbtest','operation_log','sample_analysis','user_item','ysf','yzb_operation_log','yzb_monitor'
             ]
        }

#rds3实例连接池配置
RDS3 = {
         'pool_addr':{
                 'HOST':'10.242.173.131',
                 'PORT':4042,
                 'USER':'maimiao_ops3',
                 'PASSWD':'maimiaoadmin2014' 
                 }
             ,
         'db_list':[
              'queryall','queryqueue','item_query_rpt','keywords_deleted','keywords_deleted_new','items'
             ]
        }

#rds4实例连接池配置
RDS4 = {
         'pool_addr':{
                 'HOST':'10.242.173.131',
                 'PORT':4043,
                 'USER':'maimiao_ops4',
                 'PASSWD':'maimiaoadmin2014' 
                 }
             ,
         'db_list':[
              'rpt_all','rpt_all_new','yzb_rpt_all'
             ]
        }

