import time
import subprocess
import utils
from utils import assignOrder
from utils import assertEqual
from utils import assertContains
from utils import randomString
import threading
import queue
import random
from collections import OrderedDict
import logging
import pprint
import configparser
import json
import random
import requests
import datetime

import random

global status
status = {}
logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
now = datetime.datetime.now()
# db=config.get('params','db')
# invalidUrl =config.get('params', 'invalidUrl')
x = random.randint(0, 50000)
global id_cred,metadata,audit_log_download_id
id_cred={}
metadata={}
audit_log_download_id={}

class AuditLogUI(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)



################ CORE-2762 ################

    @assignOrder(1)
    def CORE2762_auditArchiveSearchText(self):
        try:
            passed = False
            resp, body = self.api_client.auditArchiveSearchText('archive')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200 )
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(2)
    def CORE2762_auditArchiveSearchTextNoValue(self):
        try:
            passed = False
            resp, body = self.api_client.auditArchiveSearchText('archivexyz')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(3)
    def CORE2762_auditArchiveLimitPage(self):
        try:
            passed = False
            resp, body = self.api_client.auditArchiveLimitPage(5,1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(4)
    def CORE2762_auditArchiveLimitPageWrong(self):
        try:
            passed = False
            resp, body = self.api_client.auditArchiveLimitPage(-5, 1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(5)
    def CORE2762_auditArchiveJobType(self):
        try:
            passed = False
            resp, body = self.api_client.auditArchiveJobType('manual')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(6)
    def CORE2762_auditArchiveStatus(self):
        try:
            passed = False
            resp, body = self.api_client.auditArchiveStatus('Completed')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(7)
    def CORE2762_auditArchiveSortBy(self):
        try:
            passed = False
            resp, body = self.api_client.auditArchiveSortBy('archiveInitiatedDate','desc')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(8)
    def CORE2763_initiateArchive_Jobs(self):
        try:
            passed = False
            body = {
                "startDate": "2018-11-05T10:00:00Z",
                "endDate": "2018-11-05T10:00:00Z",
                "archiveMethod": "manual"
            };
            resp, body = self.api_client.postAuditLogArchive(body)
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data["message"])
            response = data["message"]
            if 'Archival Failed' in response:
                status['CAM-APITest'] = False
                return False
            else:
                passed = True
                status['CAM-APITest'] = passed
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(9)
    def postAuditConfigforIP(self):
        try:
            passed = False
            body = {
                "configurationkey": "audit_logs_user_ip",
                "configurationvalue": True
            };
            resp, body = self.api_client.postAuditConfigValues(body)
            print(resp)
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(10)
    def getAuditCadfFormat(self):
        try:
            passed = False
            resp, body = self.api_client.getAuditCadf()
            print(resp)
            passOfResponseCode = assertEqual(resp, 200)

            data = json.dumps(body)
            data = json.loads(data)

            tenantID = data['result'][0]['tenantId']
            print(tenantID)

            id = data['result'][0]['id']
            print(id)

            action = data['result'][0]['action']
            print(action)

            outcome = data['result'][0]['outcome']
            print(outcome)

            initiatorName = data['result'][0]['initiator']['name']
            print(initiatorName)

            host_useragent = data['result'][0]['initiator']['host']['user-agent']
            print(host_useragent)

            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(11)
    def getAuditSystemIP_DeleteOperation(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByActionType_Limit('HTTP_REQUEST_DELETE')
            print(resp)

            data = json.dumps(body)
            data = json.loads(data)
            sourceIpAddress = data['result'][0]['sourceIpAddress'][0]
            print(sourceIpAddress)
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and sourceIpAddress is not None and '.' in sourceIpAddress):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(12)
    def getAuditSystemIP_POSTOperation(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByActionType_Limit('HTTP_REQUEST_POST')
            print(resp)

            data = json.dumps(body)
            data = json.loads(data)
            sourceIpAddress = data['result'][0]['sourceIpAddress'][0]
            print(sourceIpAddress)
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and sourceIpAddress is not None and '.' in sourceIpAddress):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False



