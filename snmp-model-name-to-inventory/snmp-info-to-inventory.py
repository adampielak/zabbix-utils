#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
automatic-template-selection.py
"""
from pyzabbix import ZabbixAPI
import logging
import getopt
import os, sys, re

SWVERSION = 0.1
log_level = "DEBUG" # CRITICAL, ERROR, WARNING, INFO, DEBUG
skipmodules=["pyzabbix", "urllib3"]

ZBXURI = ""
ZBXUSER = ""
ZBXPASS = ""
ZBXITEMINVENTORY = {"Device Name": "name", "Device Model": "model"}

class ZabbixAPI(ZabbixAPI):
    logging.getLogger(__name__)
    def __init__(self, *args, **kwargs):
        try:
            return super(ZabbixAPI, self).__init__(*args, **kwargs)
        except Exception as e:
            logging.critical(str(e))
            raise
        
    def device_items_to_inventory(self, hostname):
        try:
            h = self.host.get(output=["hostid"], filter={"host": hostname})
            logging.info(
                f"working on {hostname}: ID is {h[0]['hostid']}"
            )
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
            logging.critical(str(e), exc_info=True)
            pass
        
    
def helpArgs():
    print (
        "\n"
        f"{os.path.basename(__file__)} - snmp device info to inventory v{SWVERSION}\n"
        "Arguments:\n"
        "\t-s|--source <hostname to manage>\n"
        f"eg: {os.path.basename(__file__)} -s 'Linux Host'"
    )
    

def main(argv):
    logging.basicConfig(format='%(asctime)s:%(process)d:[%(levelname)s](%(name)s):%(message)s', level=log_level)
    for module in skipmodules:
        logging.getLogger(module).setLevel(logging.ERROR)


    try:
        opts, args = getopt.getopt(argv,"hs:f:",["help","source="])
    except getopt.GetoptError:
        helpArgs()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            helpArgs()
            sys.exit()
        elif opt in ("-s","--source"):
            hostname = arg

    zapi = ZabbixAPI(ZBXURI)
    zapi.login(ZBXUSER,ZBXPASS)
    logging.info("Connected to Zabbix API %s Version %s" % (ZBXURI,zapi.api_version()))
    zapi.device_items_to_inventory(hostname=hostname)

if __name__ == "__main__":
    main(sys.argv[1:])
