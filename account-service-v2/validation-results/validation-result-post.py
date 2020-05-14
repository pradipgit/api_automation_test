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
from os import path
import os

import random

global status
status = {}
logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
now = datetime.datetime.now()
x = random.randint(0, 50000)
ROOT_DIR = os.path.abspath(os.curdir)
blueprint_folder = path.join(ROOT_DIR + "/testdata", "validationresults")
file_to_open = path.join(blueprint_folder, "testdata.json")


class ValidationResult(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)
        with open(file_to_open, "r+") as jsonFile:
            self.testdatajson = json.load(jsonFile)
            jsonFile.close()


    @assignOrder(2)
    def create_validation_result_success(self):
        '''
        Success case for create validation result
        '''
        response = self.testdatajson["post_validation_result_success"]
        passed = True
        randID = 'TestValidateResult'
        randID += str(x)
        print (randID)

        body = self.testdatajson["post_validationresults_payload"]

        resp, body = self.api_client.create_validation_result_validation(body)
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200) and assertEqual(body["status"], response)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(1)
    def update_validation_result_failure(self):
        '''
        Failure case for update validation result
        '''
        passed = False
        response = self.testdatajson["get_by_id_fail"]
        valResId = "9f7b800f-0b6b-4e32-8fda-6384678bdca5-TestId-To-Check"
        randID = 'TestValidateResult'
        randID += str(x)
        print (randID)

        body = self.testdatajson["put_validationresults_payload"]

        resp, body = self.api_client.update_validation_result_validation(body, valResId)
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 404) and assertEqual(body, response)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(3)
    def update_validation_result_success(self):
        '''
        Success case for update validation result
        '''
        response = self.testdatajson["update_validation_result_success"]
        passed = True
        randID = 'TestValidateResult'
        randID += str(x)
        print (randID)

        body = self.testdatajson["put_validationresults_payload"]
        body_for_post = self.testdatajson["post_validationresults_payload"]
        resp, body_temp = self.api_client.create_validation_result_validation(body_for_post)
        id = body_temp["validationID"]
        print (id)

        resp, body = self.api_client.update_validation_result_validation(body, id)
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200) and assertEqual(body, response)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(4)
    def patch_validation_result_success(self):
        '''
        Success case for update validation result
        '''
        response = self.testdatajson["patch_validation_result_success"]
        passed = True
        randID = 'TestValidateResult'
        randID += str(x)
        print (randID)

        body = self.testdatajson["patch_validationresults_payload"]
        body_for_post1 = self.testdatajson["post_validationresults_payload"]
        resp, body_res = self.api_client.create_validation_result_validation(body_for_post1)
        id = body_res["validationID"]
        print (id)
        resp, body = self.api_client.patch_validation_result_validation(body, id)
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200) and assertEqual(body, response)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(4)
    def patch_validation_result_fail(self):
        '''
        Success case for update validation result
        '''
        response = self.testdatajson["get_by_id_fail"]
        passed = True
        valResId = "9f7b800f-0b6b-4e32-8fda-6384678bdca5-TestId-To-Check"
        randID = 'TestValidateResult'
        randID += str(x)
        print (randID)

        body = self.testdatajson["patch_validationresults_payload"]

        resp, body = self.api_client.patch_validation_result_validation(body, valResId)
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 404) and assertEqual(body, response))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed
