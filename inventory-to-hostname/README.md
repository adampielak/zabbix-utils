
## What

**inventory-to-hostname**: **zabbix-inv2hostname** - systemd thread-based Python script used to update {HOST.NAME} (Visible Name) with {INVENTORY.NAME} if {HOST.NAME} == {HOST.HOST}.


## How
##### **Installation**
```sh
$ ./install.sh         Configures, installs and runs via systemd zabbix-inv2hostname.py
```

##### **Dependancies**
* Python 2.7 min.
* pyzabbix libs (installed via pip by install script).


##### **Logging**

logging is managed directly on systemd and could be checked by:

```sh
$ journalctl -f -u zabbix-inv2hostname
```

## Where
- **zabbix-inv2hostname.py** Python script copied into /usr/local/sbin/
- **zabbix-inv2hostname.conf** text configuration copied and configured in /etc/zabbix/
- **zabbix-inv2hostname.service** Systemd configuration copied into /etc/systemd/system

## Who
Author: Sergio Cricca - scricca@tomware.it

## When
March 2018
