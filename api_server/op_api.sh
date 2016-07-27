#!/bin/bash
function useage(){
    echo 'useage:'
    echo '               sh op_api.sh check         查看api server进程总数'     
    echo '               sh op_api.sh stop          停止api server服务'     
    echo '               sh op_api.sh start slb     启动api server服务 slb为可选'     
    echo '               sh op_api.sh restart slb   重启api server服务 slb为可选'     
    echo '               sh op_api.sh rebuild slb   代码更新并重启api server服务 slb为可选'     
}

function stop_api(){
    pids=`ps -ef|grep "$USER"|grep ApiCenterServer|grep -v 'grep'|awk '{print $2}'`
    if [ "$pids" == '' ] ; then
        echo -e "\033[33mthere is no api server processes to stop\033[0m"
        return
    fi
    kill -9 `ps -ef|grep $USER|grep -v grep|grep ApiCenterServer|awk '{print $2}'`
    sleep 5
    pids=`ps -ef|grep "$USER"|grep ApiCenterServer|grep -v 'grep'|awk '{print $2}'`
    if [ "$pids" != '' ] ; then
        echo -e "\033[31mstop api server failed\033[0m"
    else
        echo -e "\033[32mstop api server successfully\033[0m"
    fi
}

function start_api(){
    pids=`ps -ef|grep $USER|grep ApiCenterServer|grep -v grep|awk '{print $2}'`
    if [ "$pids" != '' ] ; then
        echo -e "\033[33mthere is already api server running\033[0m"
        return
    fi
    cd ~/comm_lib/api_server/thrift/
    nohup python ApiCenterServer.py 1>> /dev/null 2>&1 &
    sleep 5 
    pids=`ps -ef|grep $USER|grep ApiCenterServer|grep -v grep|awk '{print $2}'`
    if [ "$pids" == '' ] ; then
        echo -e "\033[31mstart api server failed\033[0m"
    else
        echo -e "\033[32mstart api server successfully\033[0m"
    fi
}

function restart_api(){
    stop_api
    start_api
}

function rebuild_api(){
    # cd ~ && sh update.sh
    restart_api
}

function config_slb(){
    ip=`ifconfig eth0 |grep "inet addr:"|awk -F : '{print $2}'|awk '{print $1}'`
    old_host='10.242.173.131'
    filename='../api_server/conf/prd/settings.py'
    sed -i "s/$old_host/$ip/" $filename 1>/dev/null 2>&1
}

if [ $# == 0 ] ; then
    useage
elif [ $1_ == 'check_' ] ; then
    ps -ef|grep $USER |grep ApiCenterServer|grep -v grep|awk '{print $2}'|wc -l
elif [ $1_ == 'stop_' ] ; then
    stop_api
elif [ $# == 1 -a $1_ == 'start_' ] ; then
    start_api
elif [ $# == 1 -a $1_ == 'restart_' ] ; then
    restart_api
elif [ $# == 1 -a $1_ == 'rebuild_' ] ; then
    rebuild_api
elif [ $# == 2 -a $2 == 'slb' -a $1 == 'start_' ] ; then
    config_slb
    start_api
elif [ $# == 2 -a $2 == 'slb' -a $1 == 'restart_' ] ; then
    config_slb
    restart_api
elif [ $# == 2 -a $2 == 'slb' -a $1 == 'rebuild_' ] ; then
    config_slb
    rebuild_api
else
    useage
fi


