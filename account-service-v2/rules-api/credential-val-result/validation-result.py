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
import jsonschema
import simplejson as json
from jsonschema import exceptions as json_exe
import random
from os import path
import os

global status
config = configparser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
now = datetime.datetime.now()
x = random.randint(0, 50000)
status = {}
data = {}
valresid = "1234"
ROOT_DIR = os.path.abspath(os.curdir)
blueprint_folder = path.join(ROOT_DIR + "/testdata", "validation-result")
file_to_open = path.join(blueprint_folder, "credValResult.json")

logger = logging.getLogger("Validation result store Run")
class ValidationResultTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)
        with open(file_to_open, "r+") as jsonFile:
            self.data = json.load(jsonFile)
            jsonFile.close()

    @assignOrder(1)
    def test_store_cred_res_success(self):
        try:
            passed = False
            response = {
                'status': {
                    'translateParameters': [],
                    'message': 'Storing of credential validation results success',
                    'translateCode': 'CO200_CRED_VALIDATION_RESULTS_STORED',
                    'statusCode': 200
                    },
                    "credId": "1234",
                    "valresId": valresid
                }
            resp, body = self.api_client.storeCredValResult(self.data["cred_val_Result_success"], valresid)
            logger.info("API response:" + str(resp))
            response["credId"] = body["credId"]
            credId = body["credId"]
            valresID = assertEqual(body["valresId"], valresid)
            passOfResponseCode = assertEqual(resp, 200)
            passOfResponse = assertEqual(body, response)
            if (passOfResponseCode and passOfResponse and valresID):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(2)
    def test_update_cred_Res_success1(self):
        try:
            passed = False
            response = {
                "status":{
                    'translateParameters': [],
                    'message': 'Updating of credential validation results success',
                    'translateCode': 'CO200_CRED_VALIDATIONRESULTS_UPDATED',
                    'statusCode': 200
                    },
                    "credId": "1234",
                    "valResId": valresid
                }
            resp, body = self.api_client.storeCredValResult(self.data["cred_val_Result_success"], valresid)
            print (resp)
            print (body)
            credId = body["credId"]
            valresID1 = assertEqual(body["valresId"], valresid)
            resp1, body1 = self.api_client.updateCredValResult(self.data["cred_val_Result_success"], valresid, credId)
            print (resp1)
            print (body1)
            logger.info("API response:" + str(resp1))
            response["credId"] = body1["credId"]
            valresID2 = assertEqual(body1["valResId"], valresid)
            passOfResponseCode = assertEqual(resp1, 200)
            passOfResponse = assertEqual(body1, response)
            if (passOfResponseCode and passOfResponse and valresID1 and valresID2):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(3)
    def test_update_cred_Res_success2(self):
        try:
            passed = False
            response =  {
                'status': {
                    'translateParameters': [],
                    'message': 'Storing of credential validation results success',
                    'translateCode': 'CO200_CRED_VALIDATION_RESULTS_STORED',
                    'statusCode': 200
                    },
                    "credId": "123",
                    "valresId": valresid
                }
            resp, body = self.api_client.updateCredValResult(self.data["cred_val_Result_success"], valresid, 'e7c8')
            print (resp)
            print (body)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            response["credId"] = body["credId"]
            valresID = assertEqual(body["valresId"], valresid)
            passOfResponse = assertEqual(body, response)
            if (passOfResponseCode and passOfResponse and valresID):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False
