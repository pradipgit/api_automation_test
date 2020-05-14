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

class AccountPurpose(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)


    @assignOrder(266)
    def createPurpose_1(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x)+"bb"
            print (randID)
            body = {
                "purposes":[
                    {
                        "name": "test1",
                        "code": "test1",
                        "description": "test Account used for working with test",
                        "appliesTo": ["test1"]
                    }

                ]
            };
            resp, body = self.api_client.create_purpose(body)
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

    @assignOrder(267)
    def createPurpose_2(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "aa"
            print (randID)
            body = {
                "purposes":[
                    {
                        "name": "test2",
                        "code": "test2",
                        "description": "test Account used for working with test",
                        "appliesTo": ["tes2"]
                    }

                ]
            };
            resp, body = self.api_client.create_purpose(body)
            print (resp)
            #print body
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(268)
    def getAllPurpose(self):
        try:
            passed = False
            resp, body = self.api_client.getAll_purpose()
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

    @assignOrder(269)
    def getPurposeByCode(self):
        try:
            passed = False
            resp, body = self.api_client.getAll_purpose()
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['code'])
            resp, body = self.api_client.getByCode_purpose(data[0]['code'])
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


    @assignOrder(270)
    def updatePurposeByCode(self):
        try:
            passed = False
            code = config.get('param', 'random_code_purpose')
            body =  {
                        "name": "test1",
                        "code": "test1",
                        "description": "test Account used for working with test1",
                        "appliesTo": ["test1"]
                    };
            resp, body = self.api_client.updatePurpose_ByCode(body, code)
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


    @assignOrder(271)
    def updatePurposeById(self):
        passed = False
        code = config.get('param', 'random_code_purpose')
        resp, body = self.api_client.getByCode_purpose(code)
        data = json.dumps(body)
        data = json.loads(data)
        print (data[0]['_id'])
        print (data[0]['code'])
        body =  {
                    "name": "test1",
                    "code": "test1",
                    "description": "test Account used for working with test1",
                    "appliesTo": ["test1"]
                };
        resp, body = self.api_client.updatePurpose_ById(body, data[0]['_id'])
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(272)
    def deletePurposeByCode(self):
        passed = False
        code = config.get('param', 'random_code_purpose')
        resp, body = self.api_client.deletePurpose_ByCode(code)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 204)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(273)
    def deletePurposeById(self):
        passed = False
        code = config.get('param', 'random_code_purpose2')
        resp, body = self.api_client.getByCode_purpose(code)
        data = json.dumps(body)
        data = json.loads(data)
        print (data[0]['_id'])
        resp, body = self.api_client.deletePurpose_ById(data[0]['_id'])
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 204)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed
