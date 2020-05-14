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

class AuditLogArchivePolicy(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)



######################## CORE-2268 #################
    @assignOrder(1)
    def CORE2268_deleteArchivePolicy(self):
        try:
            passed = False
            resp, body = self.api_client.deleteArchivePolicy()
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
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

    @assignOrder(2)
    def CORE2268_postArchivePlicy(self):
        try:
            passed = False
            now = datetime.datetime.utcnow()
            startAt= 'Y:Q:1M:' + str(now.weekday()) + 'W' + '-00:00:01'
            print(startAt)
            body = {
                "policy_type": "auditlog_archival_policy",
                "format": "ZIP",
                "periodicity": "WEEKLY",
                "startAt": startAt,
                "recordsPerArchive": 100000,
                "retentionPolicy": {
                    "hotRetentionPeriod": 30,
                    "hotRetentionCount": 500000
                },
                "archiveEndpoint": {
                    "type": "object_storage",
                    "credentials": "SYS_AUDIT_ARCHIVAL_ADMIN"
                }
            };
            resp, body = self.api_client.postArchivePolicy(body)
            print (resp)
            logger.info("API response:" + str(resp))
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

    @assignOrder(3)
    def CORE2268_getArchivePolicy(self):
        try:
            passed = False
            resp, body = self.api_client.getArchivePolicy()
            print (resp)
            logger.info("API response:" + str(resp))
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

    @assignOrder(4)
    def CORE2268_putArchivePlicy(self):
        try:
            passed = False
            now = datetime.datetime.utcnow()
            startAt = 'Y:Q:1M:' + str(now.weekday()) + 'W' + '-00:00:01'
            print(startAt)
            body = {
                "policy_type": "auditlog_archival_policy",
                "format": "ZIP",
                "periodicity": "WEEKLY",
                "startAt": startAt,
                "recordsPerArchive": 150000,
                "retentionPolicy":
                {
                    "hotRetentionPeriod": 30,
                    "hotRetentionCount": 500000
                },
                "archiveEndpoint": {
                    "type": "object_storage",
                    "credentials": "SYS_AUDIT_ARCHIVAL_ADMIN"
                }
                };
            resp, body = self.api_client.putArchivePolicy(body)
            print (resp)
            logger.info("API response:" + str(resp))
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
