#!/bin/sh
currDir=$(cd "$(dirname "$0")"; pwd)
proPath="${currDir}"/../

#网营机房 ip 与网卡
#192.168.20.194  00:1E:67:64:AF:61   mm_194
#115.231.102.195 00:1E:67:59:8F:73   mm_195
#192.168.20.196  00:1E:67:24:E0:B1   mm_196
#115.231.102.197 00:1E:67:1A:0D:81   mm_197
#192.168.20.200  00:1E:67:A4:D7:E4   mm_be1_in
#内网不通需改为外网设置
#00:16:3e:00:52:60 baidu3
#00:16:3e:00:01:f9 baidu4
function  isWy(){
    info=`ifconfig`
    if [[ "$info" =~ "00:1E:67:64:AF:61" || "$info" =~ "00:1E:67:59:8F:73" || "$info" =~ "00:1E:67:24:E0:B1" || "$info" =~ "00:1E:67:1A:0D:81" || "$info" =~ "00:1E:67:A4:D7:E4" ]];then
        echo 'wy'
    elif [[ "$info" =~ "00:16:3e:00:52:60" || "$info" =~ "00:16:3e:00:01:f9" ]];then
        echo 'aliyun'
    else
        echo 'jst' 
    fi  
}
isWyIp=`isWy`
echo "软链设置类型:$isWyIp"

if [ $1_ == "dev_" ]
then
    ln -s "${proPath}/comm_lib/tao_models/conf/dev/settings.py" "${proPath}/comm_lib/tao_models/conf/"
    ln -s "${proPath}/comm_lib/tao_models/conf/dev/set_env.py" "${proPath}/comm_lib/tao_models/conf/"

    ln -s "${proPath}/comm_lib/api_server/conf/dev/set_env.py" "${proPath}/comm_lib/api_server/conf/"
    ln -s "${proPath}/comm_lib/api_server/conf/dev/settings.py" "${proPath}/comm_lib/api_server/conf/"
    ln -s "${proPath}/comm_lib/api_server/conf/dev/db_settings.py" "${proPath}/comm_lib/api_server/conf/"
    ln -s "${proPath}/comm_lib/db_pool/conf/dev/settings.py" "${proPath}/comm_lib/db_pool/conf/"

    ln -s "${proPath}/comm_lib/service_server/conf/dev/set_env.py" "${proPath}/comm_lib/service_server/conf/"
    ln -s "${proPath}/comm_lib/service_server/conf/dev/settings.py" "${proPath}/comm_lib/service_server/conf/"
    ln -s "${proPath}/comm_lib/api_parallel/dev/celeryconfig_result.py" "${proPath}/comm_lib/api_parallel/"

elif [ $1_ == "prd_" ]
then
    ln -s "${proPath}/comm_lib/tao_models/conf/prd/settings.py" "${proPath}/comm_lib/tao_models/conf/"
    ln -s "${proPath}/comm_lib/tao_models/conf/prd/set_env.py" "${proPath}/comm_lib/tao_models/conf/"

    ln -s "${proPath}/comm_lib/service_server/conf/prd/set_env.py" "${proPath}/comm_lib/service_server/conf/"
    ln -s "${proPath}/comm_lib/service_server/conf/prd/settings.py" "${proPath}/comm_lib/service_server/conf/"
    ln -s "${proPath}/comm_lib/api_parallel/prd/celeryconfig_result.py" "${proPath}/comm_lib/api_parallel/"

    ln -s "${proPath}/comm_lib/api_server/conf/prd/set_env.py" "${proPath}/comm_lib/api_server/conf/"
    ln -s "${proPath}/comm_lib/api_server/conf/prd/db_settings.py" "${proPath}/comm_lib/api_server/conf/"
    if [ 'wy' == $isWyIp ];then
        ln -s "${proPath}/comm_lib/api_server/conf/prd/wy_settings.py" "${proPath}/comm_lib/api_server/conf/settings.py"
        ln -s "${proPath}/comm_lib/db_pool/conf/prd/wy_settings.py" "${proPath}/comm_lib/db_pool/conf/settings.py"
    elif [ 'aliyun' == $isWyIp ];then
        ln -s "${proPath}/comm_lib/api_server/conf/prd/settings.py" "${proPath}/comm_lib/api_server/conf/"
        ln -s "${proPath}/comm_lib/db_pool/conf/prd/settings.py" "${proPath}/comm_lib/db_pool/conf/"
    else
        ln -s "${proPath}/comm_lib/api_server/conf/prd/settings.py" "${proPath}/comm_lib/api_server/conf/"
        ln -s "${proPath}/comm_lib/db_pool/conf/prd/settings.py" "${proPath}/comm_lib/db_pool/conf/"
    fi

elif [ $1_ == "clean_" ]
then
    find $proPath -name "*.pyc" | xargs rm -f

    rm -f "${proPath}/comm_lib/tao_models/conf/settings.py"
    rm -f "${proPath}/comm_lib/tao_models/conf/set_env.py"

    rm -f "${proPath}/comm_lib/api_server/conf/settings.py"
    rm -f "${proPath}/comm_lib/api_server/conf/db_settings.py"
    rm -f "${proPath}/comm_lib/api_server/conf/set_env.py"
    rm -f "${proPath}/comm_lib/db_pool/conf/set_env.py"
    rm -f "${proPath}/comm_lib/db_pool/conf/settings.py"
    rm -f "${proPath}/comm_lib/api_parallel/celeryconfig_result.py"

    rm -f "${proPath}/comm_lib/service_server/conf/settings.py"
    rm -f "${proPath}/comm_lib/service_server/conf/set_env.py"

elif [ "_" == "_" ]
then
    echo "Usage: sh install.sh clean    清除当前环境中的配置及中间文件"
    echo "       sh install.sh prd      安装线上环境"
    echo "       sh install.sh dev      安装开发环境"
fi
