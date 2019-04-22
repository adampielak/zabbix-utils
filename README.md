# ZABBIX-UTILS
zabbix scripts and utilities repository.

### OS/Zabbix version disclaimer:
I'm actively testing this utilities mainly on **CentOS 7.***/**Ubuntu 18.04** and **Zabbix > 3.2** versions.

## Tools:

- **inventory-to-hostname**: **zabbix-inv2hostname** - systemd thread-based Python script used to update {HOST.NAME} (Visible Name) with {INVENTORY.NAME} if {HOST.NAME} == {HOST.HOST}.
