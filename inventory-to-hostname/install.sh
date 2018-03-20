#!/bin/bash

CONF=/etc/zabbix/zabbix-inv2hostname.conf
SBIN=/usr/local/sbin/zabbix-inv2hostname.py
SYSTEMDCONF=/etc/systemd/system/zabbix-inv2hostname.service
SERVICE=zabbix-inv2hostname

echo -n "Zabbix Server API Path (eg: http://127.0.0.1/zabbix): " && read URL
echo -n "Zabbix Server API Username: " && read USERNAME
echo -n "Zabbix Server API Password: " && read PASSWORD

pip install -q --upgrade pip
pip install -q pyzabbix

mkdir -p /etc/zabbix/

cp -f ./zabbix-inv2hostname.py $SBIN
cp -f ./zabbix-inv2hostname.conf $CONF
cp -f ./zabbix-inv2hostname.service $SYSTEMDCONF

sed -i -e "s#__USERNAME__#$USERNAME#g" -e "s#__PASSWORD__#$PASSWORD#g" -e "s#__URL__#$URL#g" $CONF 

systemctl daemon-reload
systemctl enable $SERVICE
systemctl restart $SERVICE

