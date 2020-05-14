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

class AccountPagination(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)



    @assignOrder(358)
    def CORE1909_paginationWithValidLimitAndValidPage(self):
        passed = False
        resp, body = self.api_client.paginationWithLimitAndPage(10,1)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(359)
    def CORE1909_paginationWithValidLimitAndInValidPage(self):
        passed = False
        resp, body = self.api_client.paginationWithLimitAndPage(10, -1)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 400)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(360)
    def CORE1909_paginationWithInValidLimitAndValidPage(self):
        passed = False
        resp, body = self.api_client.paginationWithLimitAndPage(-10, 1)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 400)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(361)
    def CORE1909_paginationWithInValidLimitAndInValidPage(self):
        passed = False
        resp, body = self.api_client.paginationWithLimitAndPage(-10, -1)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 400)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed
