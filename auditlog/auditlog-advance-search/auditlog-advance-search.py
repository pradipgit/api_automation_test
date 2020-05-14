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
import logging
import pprint
import configparser
import json
import random
import requests
import datetime
from collections import OrderedDict

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

class AuditlogAdvanceSearch(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)



########################CORE-2273#################

    @assignOrder(415)
    def CORE2273_populateAdvancedSearchScreenComponents(self):
        passed = False
        resp, body = self.api_client.populateAdvancedSearchScreen('components')
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['message'],'{\"message\": \"Successfully fetched the drop down values\", \"translateCode\": \"CO_SUCCESSFUL_FETCH_DROPDOWN_VALS\", \"translateParameters\": []}'))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(416)
    def CORE2273_populateAdvancedSearchScreenSubComponents(self):
        passed = False
        resp, body = self.api_client.populateAdvancedSearchScreen('subComponents')
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['message'],'{\"message\": \"Successfully fetched the drop down values\", \"translateCode\": \"CO_SUCCESSFUL_FETCH_DROPDOWN_VALS\", \"translateParameters\": []}'))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(417)
    def CORE2273_populateAdvancedSearchScreenUsers(self):
        passed = False
        resp, body = self.api_client.populateAdvancedSearchScreen('users')
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['message'],'{\"message\": \"Successfully fetched the drop down values\", \"translateCode\": \"CO_SUCCESSFUL_FETCH_DROPDOWN_VALS\", \"translateParameters\": []}'))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(418)
    def CORE2273_populateAdvancedSearchScreenTeams(self):
        passed = False
        resp, body = self.api_client.populateAdvancedSearchScreen('teams')
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['message'],'{\"message\": \"Successfully fetched the drop down values\", \"translateCode\": \"CO_SUCCESSFUL_FETCH_DROPDOWN_VALS\", \"translateParameters\": []}'))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(419)
    def CORE2273_populateAdvancedSearchScreenMessageTypes(self):
        passed = False
        resp, body = self.api_client.populateAdvancedSearchScreen('messageTypes')
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['message'],'{\"message\": \"Successfully fetched the drop down values\", \"translateCode\": \"CO_SUCCESSFUL_FETCH_DROPDOWN_VALS\", \"translateParameters\": []}'))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(420)
    def CORE2273_populateAdvancedSearchScreenWrongData(self):
        passed = False
        resp, body = self.api_client.populateAdvancedSearchScreen('messageWrong')
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 404)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

