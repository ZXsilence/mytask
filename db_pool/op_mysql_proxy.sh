#!/bin/bash
function useage(){
    echo 'useage:'
    echo '               sh op_mysql_proxy.sh check         查看mysql proxy进程总数'     
    echo '               sh op_mysql_proxy.sh stop          停止mysql proxy服务'     
    echo '               sh op_mysql_proxy.sh start         启动mysql proxy服务'     
    echo '               sh op_mysql_proxy.sh restart       重启mysql porxy服务'     
}

function stop_proxy(){
    pids=`ps -ef|grep "mysql-proxy"|grep -v 'grep'|awk '{print $2}'`
    if [ "$pids" == '' ] ; then
        echo -e "\033[33mthere is no mysql-proxy processes to stop\033[0m"
        return
    fi
    kill -9 `ps -ef|grep -v grep|grep "mysql-proxy"|awk '{print $2}'`
    pids=`ps -ef|grep "mysql-proxy"|grep -v 'grep'|awk '{print $2}'`
    if [ "$pids" != '' ] ; then
        echo -e "\033[31mstop mysql-proxy failed\033[0m"
    else
        echo -e "\033[32mstop mysql-proxy successfully\033[0m"
    fi
}

function start_proxy(){
    ip=`ifconfig eth0 |grep "inet addr:"|awk -F : '{print $2}'|awk '{print $1}'`
    old_host='10.242.173.131'
    filename='../db_pool/conf/prd/settings.py'
    sed -i "s/$old_host/$ip/" $filename 1>/dev/null 2>&1
    pids=`ps -ef|grep "mysql-proxy"|grep -v grep|awk '{print $2}'`
    if [ "$pids" != '' ] ; then
        echo -e "\033[33mthere is already mysql-proxy running\033[0m"
        return
    fi
    mysql-proxy --proxy-address=$ip:4040 --proxy-backend-addresses=jconn2thvf8ua.mysql.rds.aliyuncs.com:3306 --daemon --admin-address=127.0.0.1:5050 --admin-username=maimiao_ops --admin-password=maimiaoadmin2014 --admin-lua-script=/usr/share/mysql-proxy/ro-pooling.lua --log-file=/alidata1/logs/mysql_proxy_rds1.log --log-level=info
    mysql-proxy --proxy-address=$ip:4041 --proxy-backend-addresses=jconncd2y38wt.mysql.rds.aliyuncs.com:3306 --daemon --admin-address=127.0.0.1:5051 --admin-username=maimiao_ops --admin-password=maimiaoadmin2014 --admin-lua-script=/usr/share/mysql-proxy/ro-pooling.lua --log-file=/alidata1/logs/mysql_proxy_rds2.log --log-level=info
    mysql-proxy --proxy-address=$ip:4042 --proxy-backend-addresses=jconnuq7wnycm.mysql.rds.aliyuncs.com:3306 --daemon --admin-address=127.0.0.1:5052 --admin-username=maimiao_ops --admin-password=maimiaoadmin2014 --admin-lua-script=/usr/share/mysql-proxy/ro-pooling.lua --log-file=/alidata1/logs/mysql_proxy_rds3.log --log-level=info
    mysql-proxy --proxy-address=$ip:4043 --proxy-backend-addresses=jconn75wjq2eq.mysql.rds.aliyuncs.com:3306 --daemon --admin-address=127.0.0.1:5053 --admin-username=maimiao_ops --admin-password=maimiaoadmin2014 --admin-lua-script=/usr/share/mysql-proxy/ro-pooling.lua --log-file=/alidata1/logs/mysql_proxy_rds4.log --log-level=info
    sleep 5 
    pids=`ps -ef|grep "mysql-proxy"|grep -v grep|awk '{print $2}'`
    if [ "$pids" == '' ] ; then
        echo -e "\033[31mstart mysql proxy failed\033[0m"
    else
        echo -e "\033[32mstart mysql proxy successfully\033[0m"
    fi
}

function restart_proxy(){
    stop_proxy
    start_proxy
}

if [ $# == 0 ] ; then
    useage
elif [ $1_ == 'check_' ] ; then
    ps -ef|grep "mysql-proxy"|grep -v grep|awk '{print $2}'|wc -l
elif [ $1_ == 'stop_' ] ; then
    stop_proxy 
elif [ $1_ == 'start_' ] ; then
    start_proxy
elif [ $1_ == 'restart_' ] ; then
    restart_proxy
else
    useage
fi


