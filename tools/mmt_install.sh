#!/bin/bash
#===============================================================================
#
#          FILE:  mmt_install.sh
# 
#         USAGE:  ./mmt_install.sh 
# 
#   DESCRIPTION:  
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  xuyaoqiang (xuyaoqiang), xuyaoqiang@MaimiaoTech.com
#       COMPANY:  MaimiaoTech
#       VERSION:  1.0
#       CREATED:  08/14/2013 11:47:04 PM CST
#      REVISION:  ---
#===============================================================================

#!/bin/bash 

# install the basic lib

yum install -y 
automake libtool flex bison pkgconfig gcc gcc-c++ boost-devel libevent-devel zlib-devel python-devel ruby-devel openssl-devel make kernel-devel m4 ncurses-devel xmlto pytz eventlet net-snmp net-snmp-devel net-snmp-utils 

#install mysql

yum install -y  mysql mysql-server mysql-devel
chgrp -R mysql  /var/lib/mysql
chmod -R 700 /var/lib/mysql

# install python lib 
yum install -y  MySQL-python  python-devel ython-setuptools mod_wsgi


easy_install pip
easy_install south
pip install Mako
pip install django-mako==0.1.5pre
pip install pymongo==2.5
pip install validictory
pip install simplejson

#install django 

easy_install django==1.5.1
#install mongodb 
echo "[10gen]" > /etc/yum.repos.d/10gen.repo 
echo "name=10gen Repository" >> /etc/yum.repos.d/10gen.repo
echo "baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64 " >> /etc/yum.repos.d/10gen.repo
echo "gpgcheck=0" >> /etc/yum.repos.d/10gen.repo

yum install -y mongo-10gen-server
yum install -y mongo-10gen

#install apache 
yum install -y httpd

#set jiankongbao

net-snmp-config --create-snmpv3-user -ro -A jiankongbaomaimiaotech -a MD5 jiankongbao

# install git
yum install -y git

#install screen 
yum install -y screen

#install erlang

wget -O /etc/yum.repos.d/epel-erlang.repo http://repos.fedorapeople.org/repos/peter/erlang/epel-erlang.repo
yum install -y erlang

# install rabbitmq
#rpm --import http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
yum install -y rabbitmq-server-3.1.4-1.noarch.rpm

#instal celery
easy_install celery==3.0.13

#install denyhosts
yum install -y denyhosts

echo "sshd:122.224.126.18" >> /etc/hosts.allow 
echo "sshd:223.5.20.242" >> /etc/hosts.allow 
echo "sshd:223.5.20.243" >> /etc/hosts.allow 
echo "sshd:223.5.20.244" >> /etc/hosts.allow 
echo "sshd:223.5.20.245" >> /etc/hosts.allow 
echo "sshd:223.5.20.246" >> /etc/hosts.allow 
echo "sshd:223.5.20.248" >> /etc/hosts.allow 

#disable selinux
sed -i 's/SELINUX=enforcing/SELINUX=disable/g' /et/selinux/config
setenforce 0

#append ld path 
echo "/home/ops/Algorithm/BidwordExtend/lib" >> /etc/ld.so.conf 
echo "/usr/lib64/" >> /etc/ld.so.conf 
echo "/usr/local/lib/" >> /etc/ld.so.conf 

ldconfig

#change the ulimit 
echo "*    soft    nofile    32768" >> /et/security/limits.conf
echo "*    hard    nofile    65535" >> /et/security/limits.conf

#set the init start 
chkconfig --add sshd 
chkconfig --add iptables
chkconfig --add denyhosts
chkconfig --add snmpd 



#install nagios client nrpe

chattr -i /etc/passwd 
chattr -i /etc/group 
chattr -i /etc/shadow 
chattr -i /etc/gshadow 

useradd nagios
wget http://sourceforge.net/projects/nagiosplug/files/nagiosplug/1.4.16/nagios-plugins-1.4.16.tar.gz/download
wget http://nchc.dl.sourceforge.net/project/nagios/nrpe-2.x/nrpe-2.14/nrpe-2.14.tar.gz

tar -xzvf nagios-plugins-1.4.16.tar.gz  && cd nagios-plugins-1.4.16
./configure  --with-nagios-user=nagios --with-nagios-group=nagios 
make && make install 
chown -R nagios.nagios /usr/local/nagios/

#install nrpe 
cd $HOME

tar -xzvf nrpe-2.14.tar.gz  && cd nrpe-2.14
./configure --enable-command-args
make all 
make  install-plugin
make install-daemon
make install-daemon-config
sed -i 's/dont_blame_nrpe=0/dont_blame_nrpe=1/g' /usr/loca/nagios/etc/nrpe.cfg

chattr +i /etc/passwd 
chattr +i /etc/group 
chattr +i /etc/shadow 
chattr +i /etc/gshadow 
#reboot the serv
reboot

#

