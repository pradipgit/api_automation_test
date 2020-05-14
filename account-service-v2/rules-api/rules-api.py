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
import requests
#import responses
import datetime
import uuid
from os import path
import os

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
blueprint_folder = path.join(ROOT_DIR + "/testdata", "rules-api")
file_to_open = path.join(blueprint_folder, "testdata.json")



class RulesAPI(object):
    '''
    Test suit for Rule CRUD API
    '''
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)
        with open(file_to_open, "r+") as jsonFile:
            self.testdatajson = json.load(jsonFile)
            jsonFile.close()

    @assignOrder(1)
    def add_rule_success(self):
        '''
        Success case for adding new Rule
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)
        body = self.testdatajson["new_rule"]
        self.api_client.delete_rule_by_id(body['ruleId'])
        #print body
        resp, body = self.api_client.add_rule(body)
        print (resp)
        #print body
        ruleId = body['document']['ruleId']
        del body["document"]['vault_id']
        resp_comp = (resp, body)
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.delete_rule_by_id(ruleId)
        passOfResponseCode = (assertEqual(resp_comp[0], 200) & assertEqual(resp_comp[1], self.testdatajson["new_rule_res"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(2)
    def add_rule_failure(self):
        '''
        Failure case for adding new Rule
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)
        body = self.testdatajson["invalid_rule_payload"]

        #print body
        resp, body = self.api_client.add_rule(body)
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 400) & assertEqual(body, self.testdatajson["invalid_rule_resp"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(3)
    def get_rule_success(self):
        '''
        Success case for get Rule
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)
        body = self.testdatajson["new_rule"]

        #print body
        resp, body = self.api_client.add_rule(body)
        ruleId = body['document']['ruleId']
        resp, body = self.api_client.get_rule_by_id(ruleId)
        print (resp)
        #print body
        del body[0]['vault_id']
        res = self.testdatajson["get_rule_res"]
        res[0]['updatedTime']= body[0]['updatedTime']
        resp_comp = (resp, body)
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.delete_rule_by_id(ruleId)
        passOfResponseCode = (assertEqual(resp_comp[0], 200) & assertEqual(resp_comp[1], res))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(4)
    def get_rule_failure(self):
        '''
        Failure case for get Rule
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)

        resp, body = self.api_client.get_rule_by_id("ruleId")
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, self.testdatajson["invalid_get_rule"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(5)
    def delete_rule_success(self):
        '''
        Success case for deleting new Rule
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)
        body = self.testdatajson["new_rule"]

        #print body
        resp, body = self.api_client.add_rule(body)
        ruleId = body['document']['ruleId']
        resp, body = self.api_client.delete_rule_by_id(ruleId)
        print (resp)
        #print body
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body, self.testdatajson["delete_rule_success"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(6)
    def delete_rule_failure(self):
        '''
        Fail case for deleting new Rule
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)
        body = self.testdatajson["new_rule"]

        #print body
        resp, body = self.api_client.delete_rule_by_id("ruleId")
        print (resp)
        #print body
        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, self.testdatajson["delete_rule_fail"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(7)
    def get_all_rules_success(self):
        '''
        Success case for get all Rules
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)

        resp, body = self.api_client.get_all_rules()
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200) & isinstance(body['Rules'], list)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(8)
    def patch_rule_status_success(self):
        '''
        Success case for patch Rule status
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)
        body = self.testdatajson["new_rule"]

        #print body
        resp, body = self.api_client.add_rule(body)
        ruleId = body['document']['ruleId']

        body = self.testdatajson["rule_status_disable"]
        resp, body = self.api_client.patch_rule_status(body, ruleId)
        print (resp)
        #print body
        res = (resp, body)
        resp, body = self.api_client.delete_rule_by_id(ruleId)

        passOfResponseCode = (assertEqual(res[0], 200) & assertEqual(res[1], self.testdatajson["rule_patch_res"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(9)
    def patch_rule_status_success(self):
        '''
        Success case for patch Rule status with already enable
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)
        body = self.testdatajson["new_rule"]

        #print body
        resp, body = self.api_client.add_rule(body)
        ruleId = body['document']['ruleId']

        body = self.testdatajson["rule_status_enable"]
        resp, body = self.api_client.patch_rule_status(body, ruleId)
        print (resp)
        #print body
        res = (resp, body)
        resp, body = self.api_client.delete_rule_by_id(ruleId)

        passOfResponseCode = (assertEqual(res[0], 200) & assertEqual(res[1], self.testdatajson["rule_patch_res1"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(10)
    def patch_rule_status_failure(self):
        '''
        Failure case for patch Rule status with wrong Rule Id
        '''
        passed = False
        randID = 'TestRuleAPI'
        randID += str(x)
        print (randID)

        body = self.testdatajson["rule_status_enable"]
        resp, body = self.api_client.patch_rule_status(body, "ruleId")
        print (resp)
        #print body

        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, self.testdatajson["rule_patch_fail"]))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed
