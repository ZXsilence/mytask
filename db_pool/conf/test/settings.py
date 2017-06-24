#encoding=utf8
# Django settings for xuanciw project.
#rds实例1的连接池配置
RDS1 = {
         'pool_addr':{
                 'HOST':'localhost',
                 'PORT':3306,
                 'USER':'root',
                 'PASSWD':'test123' 
                 }
             ,
         'db_list':['information_schema','access_records',\
                 'adgroups','all_apps','api_record','auth',\
                 'campaign','cloud','cms','contact','crm',\
                 'items','keywords','longtail','mobileapp',\
                 'mysql','performance','qianniupc','rpt_adgroupbase',\
                 'rpt_adgroupeffect','rpt_all_31','rpt_campaignbase',\
                 'rpt_campaigneffect','rpt_custbase','shop_info',\
                 'strategy','syb_common_info','taoci','test','busi',\
                 'xiangqing','xuanciw','syb_web','keywords_deleted',\
                 'syb_layer','rpt_all','rpt_cache','operation_log',\
                 'queryall','queryqueue','item_query_rpt','busi_back',\
                 'sample_analysis','workflow','keywords_deleted_new',\
                 'user_item','yzb','advert','ysf','rpt_all_new',\
                 'yzb_busi','yzb_operation_log','yzb_creatives',\
                 'yzb_rpt_all','yzb_monitor']
        }

#rds2实例连接池配置
RDS2 = RDS1
#rds3实例连接池配置
RDS3 = RDS1 
#rds4实例连接池配置
RDS4 = RDS1 
