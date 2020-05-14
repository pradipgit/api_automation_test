import time
import subprocess
import utils
from utils import assignOrder
from utils import assertEqual
from utils import assertContains
from utils import randomString
import threading
import queue
import configparser
import random
from collections import OrderedDict
import logging
import pprint
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

class AccountFilter(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)



    @assignOrder(350)
    def CORE1909_filterByStartDateGreaterThanEndDate(self):
        try:
            passed = False
            resp, body = self.api_client.filterByStartDataAndEndDate('061318T1245', '041318T1245')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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

    @assignOrder(351)
    def CORE1909_filterByValidStartDataAndValidEndDate(self):
        try:
            passed = False
            resp, body = self.api_client.filterByStartDataAndEndDate('2017-01-01T01:00:00.000Z', '2017-01-01T01:00:00.000Z')
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

    @assignOrder(352)
    def CORE1909_filterByValidStartDataAndInValidEndDate(self):
        try:
            passed = False
            resp, body = self.api_client.filterByStartDataAndEndDate('2017-01-01T01:00:00.000Z', '061318')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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

    @assignOrder(353)
    def CORE1909_filterByInValidStartDataAndValidEndDate(self):
        try:
            passed = False
            resp, body = self.api_client.filterByStartDataAndEndDate('18T1158', '2017-01-01T01:00:00.000Z')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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

    @assignOrder(354)
    def CORE1909_filterByInValidStartDataAndInValidEndDate(self):
        try:
            passed = False
            resp, body = self.api_client.filterByStartDataAndEndDate('18T1158', '06131245')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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

    @assignOrder(355)
    def CORE1909_filterByAllTestDescending(self):
        try:
            passed = False
            resp, body = self.api_client.filterByAll('2017-01-01T01:00:00.000Z', '2017-01-01T01:00:00.000Z',10,1,'desc','messageType')
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

    @assignOrder(356)
    def CORE1909_filterByAllTestAscending(self):
        try:
            passed = False
            resp, body = self.api_client.filterByAll('2017-01-01T01:00:00.000Z', '2017-01-01T01:00:00.000Z',10,1,'asc','userId')
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

    @assignOrder(357)
    def CORE1909_filterByAllTestAscendingWrongData(self):
        try :
            passed = False
            resp, body = self.api_client.filterByAll('051318', '2017-01-01T01:00:00.000Z', 10, 1, 'asc', 'UserXYZ')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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
        
