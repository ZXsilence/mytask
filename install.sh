#!/bin/sh
currDir=$(cd "$(dirname "$0")"; pwd)
proPath="${currDir}"/../
if [ $1_ == "dev_" ]
then
    ln -s "${proPath}/comm_lib/tao_models/conf/dev/settings.py" "${proPath}/comm_lib/tao_models/conf/"
    ln -s "${proPath}/comm_lib/tao_models/conf/dev/set_env.py" "${proPath}/comm_lib/tao_models/conf/"

    ln -s "${proPath}/comm_lib/api_server/conf/dev/set_env.py" "${proPath}/comm_lib/api_server/conf/"
    ln -s "${proPath}/comm_lib/api_server/conf/dev/settings.py" "${proPath}/comm_lib/api_server/conf/"
    ln -s "${proPath}/comm_lib/db_pool/conf/dev/settings.py" "${proPath}/comm_lib/db_pool/conf/"

elif [ $1_ == "prd_" ]
then
    ln -s "${proPath}/comm_lib/tao_models/conf/prd/settings.py" "${proPath}/comm_lib/tao_models/conf/"
    ln -s "${proPath}/comm_lib/tao_models/conf/prd/set_env.py" "${proPath}/comm_lib/tao_models/conf/"

    ln -s "${proPath}/comm_lib/api_server/conf/prd/set_env.py" "${proPath}/comm_lib/api_server/conf/"
    ln -s "${proPath}/comm_lib/api_server/conf/prd/settings.py" "${proPath}/comm_lib/api_server/conf/"
    ln -s "${proPath}/comm_lib/db_pool/conf/prd/settings.py" "${proPath}/comm_lib/db_pool/conf/"

elif [ $1_ == "clean_" ]
then
    find $proPath -name "*.pyc" | xargs rm -f

    rm -f "${proPath}/comm_lib/tao_models/conf/settings.py"
    rm -f "${proPath}/comm_lib/tao_models/conf/set_env.py"

    rm -f "${proPath}/comm_lib/api_server/conf/settings.py"
    rm -f "${proPath}/comm_lib/api_server/conf/set_env.py"
    rm -f "${proPath}/comm_lib/db_pool/conf/set_env.py"

elif [ "_" == "_" ]
then
    echo "Usage: sh install.sh clean    清除当前环境中的配置及中间文件"
    echo "       sh install.sh prd      安装线上环境"
    echo "       sh install.sh dev      安装开发环境"
fi
