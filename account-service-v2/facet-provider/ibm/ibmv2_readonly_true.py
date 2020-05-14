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
x = random.randint(0, 70000)
global id_cred,metadata,audit_log_download_id
id_cred={}
metadata={}
audit_log_download_id={}
ibmcredRef="ibm-cref-001"

class IbmTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(200000,555555)

    @assignOrder(1)
    def postAccountIBM(self):
        try:
            passed = False
            randID = 'IBMAccountTest'
            randID += str(x)
            print (randID)
            # print metadata[0]

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": randID,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "softlayer",
                        "serviceProviderType": "ibm",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "accountNumber": "456435"
                    },
                    "credentials": [
                        {
                            "credentialName": "credpp",
                            "purpose": [
                                "costIngestion"
                            ],
                            "crefId": ibmcredRef,
                            "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ]
                                }
                            ]
                            ,
                            "status": "Active"
                        }
                    ],
                    "accountId": "f16b0f4a-a76e-499e-b5f7-IBMAccountTest"
                }
            };

            ##print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            ##print body
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(2)
    def putAccountIBM(self):
        try:
            passed = False
            randID = 'TestIBMNew'
            randID += str(x)
            print (randID)
            id1 = "f16b0f4a-a76e-499e-b5f7-IBMAccountTest"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": data["basicInfo"]["accountName"],
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "softlayer",
                        "serviceProviderType": "ibm",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "accountNumber": "345324523"
                    },
                    "credentials": [
                        {
                            "credentialName": "credpp",
                            "purpose": [
                                "costIngestion"
                            ],
                            "crefId": ibmcredRef,
                            "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ]
                                }
                            ],
                            "status": "Active",
                        }
                    ],
                    "accountId": "f16b0f4a-a76e-499e-b5f7-IBMAccountTest"
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
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(3)
    def getAccountByProviderCodeIBM(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCode("softlayer")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False



    @assignOrder(4)
    def CORE2250_postAccountIBMCloudMinimalInfo(self):
        try:
            passed = False
            randID = 'TestIBMAcMinimal'
            randID += str(x)
            print (randID)
            # print metadata[0]

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": randID,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "softlayer",
                        "serviceProviderType": "ibm",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "accountNumber": "345324523"
                    },
                    "credentials": [

                    ],
                    "accountId": "f16b0f4a-a76e-499e-IBMCloud-testautomationIBMCloud"
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
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(5)
    def deleteBillingAccountIBM(self):
            try:
                passed = False
                id = "f16b0f4a-a76e-499e-b5f7-IBMAccountTest"
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                logger.info("API response:" + str(resp))
                passOfResponseCode = assertEqual(resp, 204)
                if (passOfResponseCode):
                    passed = True
                    status['CAM-APITest'] = passed
                    resp = self.api_client.createIBMCloud_CredRefs()
                    print (resp)
                    return passed
                else :
                    status['CAM-APITest'] = False
                    resp = self.api_client.createIBMCloud_CredRefs()
                    print (resp)
                    return False
            except:
                status['CAM-APITest'] = False
                resp = self.api_client.createIBMCloud_CredRefs()
                print (resp)
                return False


############## IBM Cloud Asset #######################

    @assignOrder(6)
    def postAccountIBMAsset(self):
        try:
            passed = False
            randID = 'TestIBMAssetAc'
            randID += str(x)
            print (randID)
            # print metadata[0]

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":randID,
                     "serviceProviderType":"ibm",
                     "isActive":"Active",
                     "accountType":"subaccount",
                     "userType":"asset",
                     "serviceProviderCode":"softlayer",
                     "credential_count":1
                  },
                  "advancedInfo":{
                     "accountNumber":"klajdsflkj"
                  },
                  "credentials":[
                     {
                        "credentialName":"kjahdslkj",
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
                        "crefId": ibmcredRef
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationibmasset"
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
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(7)
    def putAccountIBMAsset(self):
        try:
            passed = False
            randID = 'TestIBMAssetAc'
            randID += str(x)
            print (randID)
            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationibmasset"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":data["basicInfo"]["accountName"],
                     "serviceProviderType":"ibm",
                     "isActive":"Active",
                     "accountType":"subaccount",
                     "userType":"asset",
                     "serviceProviderCode":"softlayer",
                     "credential_count":1
                  },
                  "advancedInfo":{
                     "accountNumber":"klajdsflkj"
                  },
                  "credentials":[
                     {
                        "credentialName":"kjahdslkj",
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
                        "crefId": ibmcredRef
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationibmasset"
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
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(8)
    def getAccountByProviderCodeIBMAsset(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeAsset("softlayer")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(9)
    def deleteAccountIBM(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationibmasset"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                resp = self.api_client.createIBMCloud_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createIBMCloud_CredRefs()
            print (resp)
            return False

    @assignOrder(10)
    def deleteAccountIBMCloudMinimalInfo(self):
        try:
            passed = False
            id = 'f16b0f4a-a76e-499e-IBMCloud-testautomationIBMCloud'
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False
