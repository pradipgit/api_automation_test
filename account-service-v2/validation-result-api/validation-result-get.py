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
#import simplejson as json
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
file_to_open = path.join(blueprint_folder, "valResultGet.json")

logger = logging.getLogger("Validation result store Run")
class ValidationResultGetTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)
        with open(file_to_open, "r+") as jsonFile:
            self.testdatajson = json.load(jsonFile)
            jsonFile.close()

    @assignOrder(1)
    def test_get_val_res_by_id_success(self):
        '''
        Success case for get validation result by id
        '''
        passed = False
        randID = 'TestValidationResultGetAPI-'
        randID += str(x)
        print (randID)

        test_body = self.testdatajson["new_validation_result"]

        resp1, body1 = self.api_client.add_validation_result(test_body)

        valResId = body1['validationID']

        resp, body = self.api_client.get_validation_result_by_id(valResId)

        resp_comp = (resp, body)
        logger.info("API response:" + str(resp))

        passOfResponseCode = (assertEqual(resp_comp[0], 200) & assertEqual(resp_comp[1]['message']['valResId'], valResId))

        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(2)
    def test_get_val_res_by_id_failure(self):
        '''
        Failure case for get validation result by id
        '''
        passed = False
        randID = 'TestValidationResultGetAPI-'
        randID += str(x)
        print (randID)

        resp, body = self.api_client.get_validation_result_by_id("wrongId")
        print (resp)
        #print body

        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, self.testdatajson["invalid_get_val_res_by_id"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(3)
    def test_get_val_res_by_credid_success(self):
        '''
        Success case for get validation result by credid
        '''
        passed = False
        randID = 'TestValidationResultGetAPI-'
        randID += str(x)
        print (randID)
        valResId = "2d104102-da97-469f-830c-5512e22aaa04"
        test_body = self.testdatajson["cred_val_Result_success"]

        resp1, body1 = self.api_client.storeCredValResult(test_body, valResId)

        credId = body1["credId"]

        resp, body = self.api_client.get_validation_result_by_credid(valResId, credId)

        resp_comp = (resp, body)
        logger.info("API response:" + str(resp))

        passOfResponseCode = (assertEqual(resp_comp[0], 200) & assertEqual(resp_comp[1]['message']['valcredentialID'], credId))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(4)
    def test_get_val_res_by_credid_failure(self):
        '''
        Failure case for get validation result by credid
        '''
        passed = False
        randID = 'TestValidationResultGetAPI-'
        randID += str(x)
        print (randID)

        resp, body = self.api_client.get_validation_result_by_credid("wrongId", "credId")
        print (resp)
        #print body

        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, self.testdatajson["invalid_get_val_res_by_credid"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(5)
    def test_get_val_count_by_id_success(self):
        '''
        Success case for get validation count by id
        '''
        passed = False
        randID = 'TestValidationResultGetValidationCountAPI-'
        randID += str(x)
        print (randID)

        test_body = self.testdatajson["new_validation_result"]

        resp1, body1 = self.api_client.add_validation_result(test_body)

        valResId = body1['validationID']

        resp, body = self.api_client.get_val_count_by_id(valResId)

        resp_comp = (resp, body)

        logger.info("API response:" + str(resp))

        passOfResponseCode = (assertEqual(resp_comp[0], 200) & assertEqual(resp_comp[1]['message'], self.testdatajson["get_val_count_by_id"]))

        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(6)
    def test_get_val_count_by_id_failure(self):
        '''
        Failure case for get validation count by id
        '''
        passed = False
        randID = 'TestValidationResultGetValidationCountAPI-'
        randID += str(x)
        print (randID)

        resp, body = self.api_client.get_val_count_by_id("wrongId")
        print (resp)
        #print body

        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, self.testdatajson["invalid_get_val_count_by_id"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(7)
    def test_get_val_count_by_credid_success(self):
        '''
        Success case for get validation result by credid
        '''
        passed = False
        randID = 'TestValidationResultGetAPI-'
        randID += str(x)
        print (randID)
        valResId = "2d104102-da97-469f-830c-5512e22aaa04"
        test_body = self.testdatajson["cred_val_Result_success"]

        resp1, body1 = self.api_client.storeCredValResult(test_body, valResId)

        credId = body1["credId"]

        resp, body = self.api_client.get_val_count_by_credid(valResId, credId)

        resp_comp = (resp, body)
        logger.info("API response:" + str(resp))

        passOfResponseCode = (assertEqual(resp_comp[0], 200) & assertEqual(resp_comp[1]['message'], self.testdatajson["get_validation_count_by_credid"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(8)
    def test_get_val_count_by_credid_failure(self):
        '''
        Failure case for get validation count by credid
        '''
        passed = False
        randID = 'TestValidationResultGetAPI-'
        randID += str(x)
        print (randID)

        resp, body = self.api_client.get_val_count_by_credid("wrongId", "credId")
        print (resp)
        #print body

        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, self.testdatajson["invalid_get_val_count_by_credid"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed
