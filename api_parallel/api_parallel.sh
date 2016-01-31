#!/bin/sh
function useage()
{
    echo "       sh api_parallel.sh   check                   查看api_parallel任务进程号"
    echo "       sh api_parallel.sh   stop                    api_parallel队列停止"
    echo "       sh web_celery.sh     start                   api_parallel队列启动"
    exit 1
}

function log_print()
{
    local time=`date "+%Y-%m-%d %H:%M:%S"`
    echo -e  "\033[32m" $time" "$@ 1>&2
    echo -e "\033[0m"
}

function log_print_err()
{
    local time=`date "+%Y-%m-%d %H:%M:%S"`
    echo -e  "\033[31m" $time" "$@ 1>&2
    echo -e "\033[0m"
}

function log_info()
{
    log_print INFO $@
}

function log_error()
{
    log_print_err ERROR $@
}

function start_celery()
{
     nohup celery worker -A workers -c 10 -Q api_parallel,celery -B -E -l INFO -f /tmp/api_parallel.log  1>> /tmp/nohup_api_parallel.out 2>&1 &
}

function stop_celery()
{
    
    pids=`ps aux|grep celery|grep  api_parallel|grep -v 'grep'| grep -v 'flume'|awk '{print $2}'`
    if [ "$pids" == "" ];then
        log_print_err "no  api_parallel worker exisits"
    else
        for pid in ${pids[@]}
        do 
            kill -9 $pid
            process_num=$((process_num+1))
        done
    fi
    sleep 1
    pids=`ps aux|grep celery|grep  api_parallel|grep -v 'grep'| grep -v 'flume'|awk '{print $2}'`
    if [ "$pids" == "" ];then
        log_info "kill  api_parallel worker success kill process_num is "$process_num
    else
        log_info "kill  api_parallel worker failed"
    fi
}
function  check()
{
    pids=`ps aux|grep celery|grep  api_parallel|grep -v 'grep'| grep -v 'flume'|awk '{print $2}'`
    pids=`ps -ef|grep 'api_parallel'|grep -v 'grep'|awk '{print $2}'`
    if [ "$pids" == "" ] ; then
        echo -e "\033[33mThere is no api_parallel task \033[0m"
    else 
        echo $pids
    fi
}

function restart_celery()
{
    stop_celery
    start_celery
}

if [ $1_ == "_" ]
then
    useage
elif [ $1_ == 'check_' ]
then
    check
elif [ $1_ == 'stop_' ]
then
    stop_celery   
elif [ $1_ == 'start_' ]
then
    start_celery  
elif [ $1_ == 'restart_' ]
then
    restart_celery  
else
    useage
    exit 1
fi


