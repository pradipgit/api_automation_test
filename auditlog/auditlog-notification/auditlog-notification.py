import time
import subprocess
import utils
from utils import assignOrder
from utils import assertEqual
from utils import assertContains
from utils import randomString
import threading
import Queue
import random
from collections import OrderedDict
import logging
import pprint
import ConfigParser
import json
import random
import requests
import datetime

import random

global status
status = {}
logger = logging.getLogger("Test Run")
config = ConfigParser.ConfigParser()
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

class AuditLogNotification(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)



    ################ CORE-2280 ##############

    @assignOrder(470)
    def CORE2280_postAuditLogNotificationPurgeSuccess(self):
        passed = False
        body = {
            "template": "purge_success",
            "error_message": "purge success"
        };
        resp, body = self.api_client.postAuditLogNotification(body)
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(471)
    def CORE2280_postAuditLogNotificationPurgeFailure(self):
        passed = False
        body = {
            "template": "purge_failure",
            "error_message": "purge fail"
        };
        resp, body = self.api_client.postAuditLogNotification(body)
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(472)
    def CORE2280_postAuditLogNotificationArchiveSuccess(self):
        passed = False
        body = {
            "template": "archive_success",
            "error_message": "archive success"
        };
        resp, body = self.api_client.postAuditLogNotification(body)
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(473)
    def CORE2280_postAuditLogNotificationArchiveFalure(self):
        passed = False
        body = {
            "template": "archive_failure",
            "error_message": "archive failure"
        };
        resp, body = self.api_client.postAuditLogNotification(body)
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed
