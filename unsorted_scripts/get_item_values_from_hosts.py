#!/usr/bin/python

from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys, string, glob, getopt, logging, threading, time
from collections import OrderedDict
import json
import openpyxl
import pandas


def helpArgs():
    print ("Arguments:\n\t\t-u|--username <zabbix username>\n\t\t-p|--password <zabbix password>\n\t\t-l|--link <zabbix server link>\n\t\t-f|--filter <item name>")

def getHostList(zApi):
    return zApi.host.get(output = "extend")

def getItemFromHosts(zApi, f):
    output = []
    for h in getHostList(zApi):
        for i in zApi.item.get(output = ['name', 'lastvalue'], hostids=h['hostid'], search = {"name" : f}):
        i['Hostname']=h['name']
            #items[i['name']] = i['lastvalue']
            output.append({'Hostname': h['name'], i['name']: i['lastvalue']})
        #print(output)
    pandas.read_json(json.dumps(output)).to_excel("output.xls", index=False,  engine="openpyxl")
    print(output)
        
            
    
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hu:p:l:f:t:a:",["help","username=","password=","link=","filter="])
    except getopt.GetoptError:
        helpArgs()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            helpArgs()
            sys.exit()
        elif opt in ("-u","--username"):
            zbxUsername = arg
        elif opt in ("-p","--password"):
            zbxPassword = arg
        elif opt in ("-l","--link"):
            zbxLink = arg.lower()
        elif opt in ("-f","--filter"):
            zbxFilter = arg

    zapi = ZabbixAPI(zbxLink)
    zapi.login(zbxUsername,zbxPassword)
    getItemFromHosts(zapi, zbxFilter)



if __name__ == "__main__":
    main(sys.argv[1:])
