
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

now = datetime.datetime.now()

class AuditLogArchive(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)


    @assignOrder(2)
    def getAuditLogArchive(self):
        try:
            passed = False
            resp, body = self.api_client.getAuditLogArchive()
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
    def verifyStatusofAuditLogArchive(self):
        try:
            passed = False
            print ("Current year: %d" % now.year)
            year = now.year
            print ("Current month: %d" % now.month)
            month = now.month
            print ("Current day: %d" % now.day)
            day = now.day

            if month < 10:
                month1 = "0" + str(month)
            else:
                month1 =str(month)

            if day < 10:
                day1 = "0" + str(day)
            else:
                day1 =str(day)

            finalDate = str(year) + "-" + str(month1) + "-" + str(day1) + "T18:29:59Z"
            print (finalDate)
            body = {
                "archiveUntil": finalDate,
                "mode": "manual",
                "filename": "DemoArchive"
            };
            resp, body = self.api_client.postAuditLogArchive(body)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['job_id'])
            resp, body = self.api_client.getAuditLogArchiveByID(data['job_id'])
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data["archiveStatus"])
            fileStatus=data["archiveStatus"]
            print (data["archiveStageStatus"])
            overAllStatus=data["archiveStageStatus"]

            if fileStatus=='ARCHIVE_PURGED' and overAllStatus == 'COMPLETED':
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False



    @assignOrder(8)
    def postAuditLogArchive_WithoutPolicy(self):
        try:
            passed = False
            resp, body = self.api_client.deleteArchivePolicy()
            print (resp)
            logger.info("API response:" + str(resp))
            print ("Current year: %d" % now.year)
            year = now.year
            print ("Current month: %d" % now.month)
            month = now.month
            print ("Current day: %d" % now.day)
            day = now.day


            if month < 10:
                month1 = "0" + str(month)
            else:
                month1 = str(month)

            if day < 10:
                day1 = "0" + str(day)
            else:
                day1 = str(day)

            finalDate = str(year) + "-" + str(month1) + "-" + str(day1) + "T10:10:00Z"


            body = {
                "archiveUntil": finalDate,
                "mode": "manual",
                "filename": "DemoArchive"
            };
            resp, body = self.api_client.postAuditLogArchive(body)
            print (resp)
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(9)
    def postArchivePlicy(self):
      try:
            passed = False
            body = {
            "policy_type": "auditlog_archival_policy",
            "format": "ZIP",
            "periodicity": "MONTHLY",
            "startAt": "Y:Q:1M:W-00:00:01",
            "recordsPerArchive": 100000,
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
            resp, body = self.api_client.postArchivePolicy(body)
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


    @assignOrder(10)
    def getAuditLogArchiveByInvalidid(self):
        try:
            passed = False
            resp, body = self.api_client.getAuditLogArchiveByID("xyz123")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    # @assignOrder(11)
    # def restartwith_InvalidId(self):
    #     try:
    #         passed = False
    #         body = {
    #             "restartJob": "xyz123"
    #         };
    #         resp, body = self.api_client.patchArchiveJobs(body)
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         passOfResponseCode = assertEqual(resp, 404)
    #         if (passOfResponseCode):
    #             passed = True
    #         status['CAM-APITest'] = passed
    #         return passed
    #     except:
    #         status['CAM-APITest'] = False
    #         return False
    #
    #

    @assignOrder(12)
    def postAuditLogArchive_WrongData(self):
        try:
            passed = False
            body = {
               "archiveUntil11" : "2019-02-01T10:10:00Z",
              "mode": "manual",
              "filename": "DemoArchive"
            };
            resp, body = self.api_client.postAuditLogArchive(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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
