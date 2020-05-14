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

class AccountSort(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)



################### CORE-1909 ############################


    @assignOrder(336)
    def CORE1909_sortByActionDateDescending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('desc','initiatedDate')
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

    @assignOrder(337)
    def CORE1909_sortByActionDateAscending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('asc','initiatedDate')
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

    @assignOrder(338)
    def CORE1909_sortByActionTypeDescending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('desc','messageType')
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

    @assignOrder(339)
    def CORE1909_sortByActionTypeAscending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('asc','messageType')
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

    @assignOrder(340)
    def CORE1909_sortByComponentDescending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('desc', 'component')
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

    @assignOrder(341)
    def CORE1909_sortByComponentAscending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('asc', 'component')
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

    @assignOrder(342)
    def CORE1909_sortBySubComponentDescending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('desc', 'subcomponent')
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

    @assignOrder(343)
    def CORE1909_sortBySubComponentAscending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('asc', 'subcomponent')
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

    @assignOrder(344)
    def CORE1909_sortByUserDescending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('desc', 'userId')
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

    @assignOrder(345)
    def CORE1909_sortByUserAscending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('asc', 'userId')
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

    @assignOrder(346)
    def CORE1909_sortByUserTeamDescending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('desc', 'teamId')
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

    @assignOrder(347)
    def CORE1909_sortByUserTeamAscending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('asc', 'teamId')
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

    @assignOrder(348)
    def CORE1909_sortByWrongUserTeamAscending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('asc', 'UserTeamXYZ')
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

    @assignOrder(349)
    def CORE1909_sortByWrongSortTypeDescending(self):
        try:
            passed = False
            resp, body = self.api_client.sortByAction('xyz', 'UserXYZ')
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
