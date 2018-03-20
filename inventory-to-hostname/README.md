Author: Sergio Cricca - scricca@tomware.it - 2018

Zabbix inventory-name to hostname


** Usage: **

./install.sh         Configures, installs and runs via systemd zabbix-inv2hostname.py

** depends on: **
Python 2.7 min.
pyzabbix libs (installed via pip by install script).


** how to check logs: **

logging is managed directly on systemd.
use ""journalctl -f -u zabbix-inv2hostname"" 
