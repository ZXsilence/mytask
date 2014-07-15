#encoding=utf8
# Django settings for xuanciw project.
#rds实例1的连接池配置
RDS1 = {
         'pool_addr':{
                 'HOST':'localhost',
                 'PORT':3306,
                 'USER':'root',
                 'PASSWD':'123456' 
                 }
             ,
         'db_list':['information_schema','access_records',\
                 'adgroups','all_apps','api_record','auth',\
                 'campaigns','cloud','cms','contact','crm',\
                 'items','keywords','longtail','mobileapp',\
                 'mysql','performance','qianniupc','rpt_adgroupbase',\
                 'rpt_adgroupeffect','rpt_all_31','rpt_campaignbase',\
                 'rpt_campaigneffect','rpt_custbase','shop_info',\
                 'strategy','syb_common_info','taoci','test',\
                 'xiangqing','xuanciw','syb_web','keywords_deleted']
        }

#rds2实例连接池配置
RDS2 = RDS1
