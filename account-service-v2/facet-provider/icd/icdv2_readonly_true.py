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
icdcredRef="icd-cref-001"

icd_url = config.get('icd', 'url')

class IcdTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)


    @assignOrder(254)
    def postAccountICD(self):
        try:
            passed = False
            randID = 'TestICDAc'
            randID += str(x)
            print (randID)

            url=utils.decodeCredential(icd_url)

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":randID,
                     "serviceProviderType":"icd",
                     "isActive":"Active",
                     "accountType":"master",
                     "userType":"billing",
                     "serviceProviderCode":"icd",
                     "credential_count":1
                  },
                  "advancedInfo":{
                     "url":url
                  },
                  "credentials":[
                     {
                        "credentialName":"jaslkdjflkj",
                        "purpose":[
                           "costIngestion"
                        ],
                         "context": [
                             {
                                 "team": [
                                     "CORE-X"
                                 ]
                             }
                         ],
                        "status": "Active",
                        "crefId": icdcredRef
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationicd"
               }
            };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            #print body
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


    @assignOrder(255)
    def putAccountICD(self):
        try:
            passed = False
            randID = 'MyAmazon'
            randID += str(x)
            print (randID)
            url=utils.decodeCredential(icd_url)
            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationicd"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":data["basicInfo"]["accountName"],
                     "serviceProviderType":"icd",
                     "isActive":"Active",
                     "accountType":"master",
                     "userType":"billing",
                     "serviceProviderCode":"icd",
                     "credential_count":1
                  },
                  "advancedInfo":{
                     "url":url
                  },
                  "credentials":[
                     {
                        "credentialName":"jaslkdjflkj",
                        "purpose":[
                           "costIngestion"
                        ],
                        "status":"Active",
                         "context": [
                             {
                                 "team": [
                                     "CORE-X"
                                 ]
                             }
                         ],
                        "crefId": icdcredRef
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationicd"
               }
            };
            resp, body = self.api_client.update_account(body, id1)
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


    @assignOrder(256)
    def getAccountByProviderCodeICD(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCode("icd")
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

    @assignOrder(257)
    def deleteAccountICD(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationicd"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp = self.api_client.createICD_CredRefs()
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp = self.api_client.createICD_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createICD_CredRefs()
            print (resp)
            return False

############ ICD system account ###########

    @assignOrder(529)
    def postAccountICDSystem(self):
        try:
            passed = False
            randID = 'TestICDSystemAc'
            randID += str(x)
            print (randID)
            url=utils.decodeCredential(icd_url)
            # print metadata[0]

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":randID,
                     "serviceProviderType":"icd",
                     "isActive":"Active",
                     "accountType":"master",
                     "userType":"system",
                     "serviceProviderCode":"icd",
                     "credential_count":1
                  },
                  "advancedInfo":{
                     "url":url
                  },
                  "credentials":[
                     {
                        "credentialName":"fasdf",
                        "purpose":[
                           "systemIntegration"
                        ],
                        "status":"Active",
                         "context": [
                             {
                                 "team": [
                                     "CORE-X"
                                 ]
                             }
                         ],
                        "crefId": icdcredRef
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationicdsystem"
               }
            };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            #print body
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


    @assignOrder(530)
    def putAccountICDSystem(self):
        try:
            passed = False
            randID = 'MyICDSystem'
            randID += str(x)
            print (randID)
            url=utils.decodeCredential(icd_url)
            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationicdsystem"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":data["basicInfo"]["accountName"],
                     "serviceProviderType":"icd",
                     "isActive":"Active",
                     "accountType":"master",
                     "userType":"system",
                     "serviceProviderCode":"icd",
                     "credential_count":1
                  },
                  "advancedInfo":{
                     "url":url
                  },
                  "credentials":[
                     {
                        "credentialName":"fasdf",
                        "purpose":[
                           "systemIntegration"
                        ],
                        "status":"Active",
                         "context": [
                             {
                                 "team": [
                                     "CORE-X"
                                 ]
                             }
                         ],
                        "crefId": icdcredRef
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationicdsystem"
               }
            };
            resp, body = self.api_client.update_account(body, id1)
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


    @assignOrder(531)
    def getAccountByProviderCodeICDSystem(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeSystem("icd")
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

    @assignOrder(532)
    def deleteAccountICDSystem(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationicdsystem"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp = self.api_client.createICD_CredRefs()
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp = self.api_client.createICD_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createICD_CredRefs()
            print (resp)
            return False

####################### V2 Asset account ICD ########################

    @assignOrder(575)
    def postAccountICDAsset(self):
        try:
            passed = False
            randID = 'TestICDAssetAc'
            randID += str(x)
            print (randID)
            url=utils.decodeCredential(icd_url)
            # print metadata[0]

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":randID,
                     "serviceProviderType":"icd",
                     "isActive":"Active",
                     "accountType":"subaccount",
                     "userType":"asset",
                     "serviceProviderCode":"icd",
                     "credential_count":1
                  },
                  "advancedInfo":{
                     "url":url
                  },
                  "credentials":[
                     {
                        "credentialName":"lkajdslkj",
                        "purpose":[
                           "provisioning"
                        ],
                        "status":"Active",
                         "context": [
                             {
                                 "team": [
                                     "CORE-X"
                                 ]
                             }
                         ],
                        "crefId": icdcredRef
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationicdasset"
               }
            };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            #print body
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


    @assignOrder(576)
    def putAccountICDAsset(self):
        try:
            passed = False
            randID = 'MyICDAssetAc'
            randID += str(x)
            print (randID)
            url=utils.decodeCredential(icd_url)
            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationicdasset"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":data["basicInfo"]["accountName"],
                     "serviceProviderType":"icd",
                     "isActive":"Active",
                     "accountType":"subaccount",
                     "userType":"asset",
                     "serviceProviderCode":"icd",
                     "credential_count":1
                  },
                  "advancedInfo":{
                     "url":url
                  },
                  "credentials":[
                     {
                        "credentialName":"lkajdslkj",
                        "purpose":[
                           "provisioning"
                        ],
                        "status":"Active",
                         "context": [
                             {
                                 "team": [
                                     "CORE-X"
                                 ]
                             }
                         ],
                        "crefId": icdcredRef
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationicdasset"
               }
            };
            resp, body = self.api_client.update_account(body, id1)
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


    @assignOrder(577)
    def getAccountByProviderCodeICDAsset(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeAsset("icd")
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

    @assignOrder(578)
    def deleteAccountICDAsset(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationicdasset"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp = self.api_client.createICD_CredRefs()
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp = self.api_client.createICD_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createICD_CredRefs()
            print (resp)
            return False

    @assignOrder(579)
    def postSystemAccount_TestDataCreation(self):
        try:
            passed = False
            url=utils.decodeCredential(icd_url)
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": "testDataAccountforICDNewAccount",
                        "serviceProviderType": "icd",
                        "isActive": "Active",
                        "accountType": "master",
                        "userType": "system",
                        "serviceProviderCode": "icd",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "url": url
                    },
                    "credentials": [
                        {
                            "credentialName": "Credential1",
                            "purpose": [
                                "systemIntegration"
                            ],
                            "status": "Active",
                             "context": [
                             {
                                 "team": [
                                     "CORE-X"
                                 ]
                             }
                         ],
                            "crefId": icdcredRef
                        }
                    ]
                }
            };

            ##print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            passOfResponseCode = resp
            if ((passOfResponseCode == 200) | (passOfResponseCode == 409)):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False
