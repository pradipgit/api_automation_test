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
import responses
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
accountId = 'f16b0f4a-a76e-499e-b5f7-autoawsintegration'
ROOT_DIR = os.path.abspath(os.curdir)
blueprint_folder = path.join(ROOT_DIR + "/testdata", "rules-api")
file_to_open = path.join(blueprint_folder, "testdata.json")



class RuleValidation(object):
    '''
    Test suit for Rule validation for Account and Credential
    '''
    def __init__(self,client, appurl):
        self.api_client = client
        self.appurl = appurl
        self.invoice_id = random.randint(100000,999999)
        with open(file_to_open, "r+") as jsonFile:
            self.testdatajson = json.load(jsonFile)
            jsonFile.close()

    @assignOrder(1)
    def validate_account_rule_failure(self):
        '''
        Failure case for account rule validation
        '''
        passed = False
        randID = 'TestRuleValidate'
        randID += str(x)
        print (randID)
        body = self.testdatajson["account_failure"]

        # #print body
        resp, body = self.api_client.validate_account_rule(body)
        print (resp)
        # #print body
        resp_comp = self.testdatajson["internal_err_acc"]
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, resp_comp))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(2)
    def validate_account_rule_invalid_body(self):
        '''
        Invalid request- failure cases
        '''
        passed = False
        randID = 'TestRuleValidate'
        randID += str(x)
        print (randID)
        body = {}

        #print body
        resp, body = self.api_client.validate_account_rule(body)
        print (resp)
        #print body
        resp_data = self.testdatajson["acc_invalid_req_res"]
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 400) & assertEqual(body, resp_data))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(3)
    def validate_cred_rule_invalid_req(self):
        '''
        Failure case for credential rule validation
        '''
        passed = False
        randID = 'TestRuleValidate'
        randID += str(x)
        print (randID)

        body = self.testdatajson["acc_cred_invalid_body"]

        #print body
        resp, body = self.api_client.validate_credential_rule(body)
        print (resp)
        #print body
        resp_data = self.testdatajson["invalid_req_res"]
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 400) & assertEqual(body, resp_data))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(4)
    def validate_cred_rule_failure(self):
        '''
        Invalid request- failure cases
        '''
        passed = False
        randID = 'TestRuleValidate'
        randID += str(x)
        print (randID)

        body = self.testdatajson["cred_failure_res"]

        #print body
        resp, body = self.api_client.validate_credential_rule(body)
        print (resp)
        #print body
        resp_comp = self.testdatajson["internal_err_acc"]
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, resp_comp))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(5)
    def revalidate_cred_rule_invalid_req(self):
        '''
        Failure case for credential & account rule Revalidation
        '''
        passed = False
        randID = 'TestRuleValidate'
        randID += str(x)
        print (randID)

        body = self.testdatajson["acc_cred_invalid_body"]

        #print body
        resp, body = self.api_client.revalidate_credential_rule(body)
        print (resp)
        #print body
        resp_data = self.testdatajson["invalid_req_res"]
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 400) & assertEqual(body, resp_data))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(6)
    def revalidate_cred_rule_failure(self):
        '''
        Invalid request- failure cases
        '''
        passed = False
        randID = 'TestRuleValidate'
        randID += str(x)
        print (randID)

        body = self.testdatajson["cred_failure_res"]

        #print body
        resp, body = self.api_client.revalidate_credential_rule(body)
        print (resp)
        #print body
        resp_comp = self.testdatajson["internal_err"]
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 404) & assertEqual(body, resp_comp))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(7)
    @responses.activate
    def validate_account_rule_success(self):
        '''
        Success case for account rule validation
        '''
        passed = False
        randID = 'TestRuleValidate'
        randID += str(x)
        print (randID)
        account_validation_response =self.testdatajson["account_validation_response"]
        responses.add(responses.POST, self.appurl + 'cb-credential-service/api/v2.0/rules/accountvalidator',
            json=account_validation_response, status=200)

        body = self.testdatajson["account_failure"]

        #print body
        resp, body = self.api_client.validate_account_rule(body)
        data = json.dumps(body)
        data = json.loads(data)
        acc_res = self.testdatajson["acc_val_res"]
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(data, acc_res))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(8)
    @responses.activate
    def validate_cred_rule_success(self):
        '''
        Success case for credential rule validation
        '''
        passed = False
        randID = 'TestRuleValidate'
        randID += str(x)
        print (randID)
        account_validation_response =self.testdatajson["account_validation_response"]
        responses.add(responses.POST, self.appurl + 'cb-credential-service/api/v2.0/rules/credentialvalidator',
            json=account_validation_response, status=200)

        body = self.testdatajson["account_failure"]

        #print body
        resp, body = self.api_client.validate_credential_rule(body)
        data = json.dumps(body)
        data = json.loads(data)
        acc_res = self.testdatajson["acc_val_res"]
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(data, acc_res))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(9)
    @responses.activate
    def revalidate_cred_rule_success(self):
        '''
        Success case for credential rule Revalidation
        '''
        passed = False
        randID = 'TestRuleValidate'
        randID += str(x)
        print (randID)
        account_validation_response =self.testdatajson["account_validation_response"]
        responses.add(responses.POST, self.appurl + 'cb-credential-service/api/v2.0/rules/credentialrevalidator',
            json=account_validation_response, status=200)

        body = self.testdatajson["account_failure"]

        #print body
        resp, body = self.api_client.revalidate_credential_rule(body)
        data = json.dumps(body)
        data = json.loads(data)
        acc_res = self.testdatajson["acc_val_res"]
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(data, acc_res))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed
