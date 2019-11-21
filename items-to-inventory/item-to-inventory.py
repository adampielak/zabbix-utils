#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
automatic-template-selection.py
helps sync item value into inventory fields
"""


from pyzabbix import ZabbixAPI
import logging
import getopt
import os, sys, re

log_level = "WARNING" # CRITICAL, ERROR, WARNING, INFO, DEBUG
logshowerror = False
skipmodules=["pyzabbix", "urllib3"]

# Variables
SWVERSION = 1.0
ZBXURI = ""
ZBXUSER = ""
ZBXPASS = ""
ZBXITEMINVENTORY = {"Device Name": "name", "Device Model": "model"} # dict {item name: inventory name}
ZBXGROUPS = ["Printers"] # array of group names

class ZabbixAPI(ZabbixAPI):
    logging.getLogger(__name__)
    def __init__(self, *args, **kwargs):
        try:
            return super(ZabbixAPI, self).__init__(*args, **kwargs)
        except Exception as e:
            logging.critical(str(e))
            raise
    
    def all_hosts(self):
        try:
            output = []
            for g in ZBXGROUPS:
                groupid = self.hostgroup.get(output="groupid", filter={"name": g})[0]['groupid']
                hosts = self.host.get(output = "extend", groupids = groupid, filter = {"status": 0})
                for host in hosts:
                    output.append(host)
            return output    
        except Exception as e:
            logging.critical(str(e))
            pass
        
    def device_items_to_inventory(self, hostname):
        try:
            h = self.host.get(output=["hostid"], filter={"host": hostname})
            logging.info(
                f"working on {hostname}: ID is {h[0]['hostid']}"
            )
        except Exception as e:
            logging.critical(f"{hostname} error: {str(e)}", exc_info = logshowerror)
            pass
        try:
            for k,v in ZBXITEMINVENTORY.items():
                logging.debug(
                    f"looking for item '{k}'"    
                )
                item = self.item.get(output=["lastvalue"], hostids=h[0]["hostid"], filter={"name": k, "status": 0, "state": 0})
                logging.debug(
                    f"{k} value is {item[0]['lastvalue']}"
                )
                logging.info(
                    f"filling {item[0]['lastvalue']} into inventory {v}"
                )
                self.host.update(hostid=h[0]['hostid'], inventory={v: item[0]['lastvalue']})
        except Exception as e:
            logging.critical(f"{hostname} error: {str(e)}", exc_info = logshowerror)
            pass
        
    

def main():
    logging.basicConfig(format='%(asctime)s:%(process)d:[%(levelname)s](%(name)s):%(message)s', level=log_level)
    for module in skipmodules:
        logging.getLogger(module).setLevel(logging.ERROR)
    try:
        zapi = ZabbixAPI(ZBXURI)
        zapi.login(ZBXUSER,ZBXPASS)
        logging.info("Connected to Zabbix API %s Version %s" % (ZBXURI,zapi.api_version()))
        for host in zapi.all_hosts():
            zapi.device_items_to_inventory(hostname=host['host'])
    except Exception as e:
        logging.critical(str(e), exc_info = logshowerror)
        pass
    

if __name__ == "__main__":
    main()
