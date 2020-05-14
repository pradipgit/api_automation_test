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
import sys

import random

global status
status = {}
logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()
config.read('settings.conf')
config.read('testdata.conf')
now = datetime.datetime.now()
# user_name = config.get('params', 'username')
global headersUser1
global user_name
x = random.randint(0, 50000)
global id_cred,metadata,audit_log_download_id
id_cred={}
metadata={}
audit_log_download_id={}

class AccountAdvanceSearch(object):
    def __init__(self,client):
        global headersUser1
        global user_name

        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

        if(sys.argv[1]=='automation-core-b'):
            user_name = config.get('params', 'username_mt')
        else:
            user_name = config.get('params', 'username')


    ############### CORE-1914 & CORE-1732 ##############

    @assignOrder(315)
    def CORE1914_1732_advanceSearchByValidStartDateAndEndDate(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByStartDateAndEndDate('2017-01-01T01:00:00.000Z','2017-01-01T01:00:00.000Z')
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


    @assignOrder(316)
    def CORE1914_1732_advanceSearchByValidStartDateAndInvalidEndDate(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByStartDateAndEndDate('2017-01-01T01:00:00.000Z', 3234)
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


    @assignOrder(317)
    def CORE1914_1732_advanceSearchByInValidStartDateAndValidEndDate(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByStartDateAndEndDate(3234, '2017-01-01T01:00:00.000Z')
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


    @assignOrder(318)
    def CORE1914_1732_advanceSearchByInValidStartDateAndInvalidEndDate(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByStartDateAndEndDate(3234, 4545)
            print (resp)
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


    @assignOrder(319)
    def CORE1914_1732_advanceSearchByActionTypeTest(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByActionType('Create service provider')
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


    @assignOrder(320)
    def CORE1914_1732_advanceSearchByComponentTest(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByComponent('cb-credential-service')
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


    @assignOrder(321)
    def CORE1914_1732_advanceSearchBySubComponentTest(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchBySubComponent('account-service')
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


    @assignOrder(322)
    def CORE1914_1732_advanceSearchByUserTest(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByUser(user_name)
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


    @assignOrder(333)
    def CORE1914_1732_advanceSearchByUserTeamTest(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByUserTeam('MYTEAM-Consume')
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


    @assignOrder(334)
    def CORE1914_1732_advanceSearchByAllCategoryTest_WithoutTeam(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByAllCategory('ASSET_ACCOUNT_CREATE','', '',
                                                                    'ASSET_ACCOUNT_CREATE','',user_name,'','Account Management')
            print (resp)
            logger.info("API response:" + str(resp))
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['total_rows'])
            totalRowsCount = data['total_rows']
            if (totalRowsCount == 0):
                status['CAM-APITest'] = False
                return False
            else:
                passed = True
                status['CAM-APITest'] = passed
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(335)
    def CORE1914_1732_advanceSearchByAllCategoryNegativeTest(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByAllCategory('serviceProviderName33243324', '2017-01-01T01:00:00.000Z',
                                                                    '2017-01-01T01:00:00.000Z',
                                                                    'Create service provider33', 'account-service',
                                                                    'cloud.brokertest@gmail.com33', 'MYTEAM-Consum3333e32',
                                                                    'cb-credential-service')
            print (resp)
            logger.info("API response:" + str(resp))
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['total_rows'])
            totalRowsCount = data['total_rows']
            if (totalRowsCount == 0):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(336)
    def CORE1914_1732_advanceSearchByAllCategoryTestWithTeam(self):
        try:
            passed = False
            resp, body = self.api_client.advanceSearchByAllCategory('ASSET_ACCOUNT_CREATE', '', '',
                                                                    'ASSET_ACCOUNT_CREATE', '',
                                                                    user_name, 'CORE-X', 'Account Management')
            print (resp)
            logger.info("API response:" + str(resp))
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['total_rows'])
            totalRowsCount = data['total_rows']
            if (totalRowsCount == 0):
                status['CAM-APITest'] = False
                return False
            else:
                passed = True
                status['CAM-APITest'] = passed
                return passed
        except:
            status['CAM-APITest'] = False
            return False
