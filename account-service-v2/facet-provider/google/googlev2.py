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

google_projectName = config.get('google', 'projectname')
google_serviceAccountName = config.get('google', 'serviceaccountname')
google_projectId = config.get('google', 'projectid')
google_bucket = config.get('google', 'bucket')
google_serviceKey = config.get('googlebilling', 'servicekey')
google_dataset = config.get('googlebilling', 'dataset')

class GoogleTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

    @assignOrder(250)
    def postAccountGoogle(self):
        try:
            passed = False
            randID = 'TestGoogleAc'
            randID += str(x)
            print (randID)
            # print metadata[0]
            projectName=utils.decodeCredential(google_projectName)
            serviceAccountName=utils.decodeCredential(google_serviceAccountName)
            projectId=utils.decodeCredential(google_projectId)
            bucket=utils.decodeCredential(google_bucket)
            serviceKey=utils.decodeCredential(google_serviceKey)
            dataset=utils.decodeCredential(google_dataset)

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": randID,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "google",
                        "serviceProviderType": "google",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "projectName": projectName,
                        "serviceAccountName": serviceAccountName,
                        "projectId": projectId,
                        "bucket": bucket
                    },
                    "credentials": [
                        {
                            "credentialName": "fsdgsdf",
                            "purpose": [
                                "costIngestion"
                            ],
                            "status": "Active",
                            "passwordFields": {
                                "serviceKey": serviceKey,
                                "Data Set": dataset,
                                "Bucket": bucket
                            },
                            "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ]
                                }
                            ]
                        }
                    ],
                    "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationgoogle"
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
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(251)
    def putAccountGoogle(self):
        try:
            passed = False
            randID = 'MyAmazon'
            randID += str(x)
            print (randID)

            projectName=utils.decodeCredential(google_projectName)
            serviceAccountName=utils.decodeCredential(google_serviceAccountName)
            projectId=utils.decodeCredential(google_projectId)
            bucket=utils.decodeCredential(google_bucket)
            serviceKey=utils.decodeCredential(google_serviceKey)
            dataset=utils.decodeCredential(google_dataset)

            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationgoogle"
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
                        "serviceProviderCode": "google",
                        "serviceProviderType": "google",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "projectName": projectName,
                        "serviceAccountName": serviceAccountName,
                        "projectId": projectId,
                        "bucket": bucket
                    },
                    "credentials": [
                        {
                            "credentialName": "fsdgsdf",
                            "purpose": [
                                "costIngestion"
                            ],

                            "passwordFields": {
                                "serviceKey": serviceKey,
                                "Data Set": dataset,
                                "Bucket": bucket
                            },
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
                    "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationgoogle"
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
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(252)
    def getAccountByProviderCodeGoogle(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCode("google")
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

    @assignOrder(253)
    def deleteAccountGoogle(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationgoogle"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(406)
    def CORE2250_postAccountGoogleMinimalInfo(self):
        try:
            passed = False
            randID = 'TestGoogleAcMinimal'
            randID += str(x)
            print (randID)
            # print metadata[0]

            projectName=utils.decodeCredential(google_projectName)
            serviceAccountName=utils.decodeCredential(google_serviceAccountName)
            projectId=utils.decodeCredential(google_projectId)
            bucket=utils.decodeCredential(google_bucket)

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": randID,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "google",
                        "serviceProviderType": "google",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "projectName": projectName,
                        "serviceAccountName": serviceAccountName,
                        "projectId": projectId,
                        "bucket": bucket
                    },
                    "credentials": [

                    ],
                    "accountId": "f16b0f4a-a76e-499e-google-testautomationgoogle1"
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
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(408)
    def CORE2250_getAccountByIdsMinimalInfo(self):
        try:
            passed = False
            id='f16b0f4a-a76e-499e-google-testautomationgoogle1'
            resp, body = self.api_client.get_AccountByIds(id)
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


    @assignOrder(409)
    def CORE2250_putAccountGoogleMinimalInfo(self):
        try:
            passed = False
            randID = 'MyAmazon'
            randID += str(x)
            print (randID)

            projectName=utils.decodeCredential(google_projectName)
            serviceAccountName=utils.decodeCredential(google_serviceAccountName)
            projectId=utils.decodeCredential(google_projectId)
            bucket=utils.decodeCredential(google_bucket)
            serviceKey=utils.decodeCredential(google_serviceKey)
            dataset=utils.decodeCredential(google_dataset)

            id1 = "f16b0f4a-a76e-499e-google-testautomationgoogle1"
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
                        "serviceProviderCode": "google",
                        "serviceProviderType": "google",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "projectName": projectName,
                        "serviceAccountName": serviceAccountName,
                        "projectId": projectId,
                        "bucket": bucket
                    },
                    "credentials": [
                        {
                            "credentialName": "fsdgsdf",
                            "purpose": [
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
                            "passwordFields": {
                                "serviceKey": serviceKey,
                                "Data Set": dataset,
                                "Bucket": bucket
                            },

                        }
                    ],
                    "accountId": "f16b0f4a-a76e-499e-google-testautomationgoogle1"
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
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(410)
    def CORE2250_deleteAccountgoogleMinimalInfo(self):
        try:
            passed = False
            id = 'f16b0f4a-a76e-499e-google-testautomationgoogle1'
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


        ####################### V2 account Google Asset ########################

    @assignOrder(571)
    def postAccountGoogleAsset(self):
        try:
            passed = False
            randID = 'TestGoogleAssetAc'
            randID += str(x)
            print (randID)
            # print metadata[0]

            projectName=utils.decodeCredential(google_projectName)
            serviceAccountName=utils.decodeCredential(google_serviceAccountName)
            projectId=utils.decodeCredential(google_projectId)
            bucket=utils.decodeCredential(google_bucket)
            serviceKey=utils.decodeCredential(google_serviceKey)
            dataset=utils.decodeCredential(google_dataset)

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":randID,
                     "serviceProviderType":"google",
                     "isActive":"Active",
                     "accountType":"subaccount",
                     "userType":"asset",
                     "serviceProviderCode":"google",
                     "credential_count":1
                  },
                  "advancedInfo":{
                     "projectName": projectName,
                     "serviceAccountName": serviceAccountName,
                     "projectId": projectId
                  },
                  "credentials":[
                     {
                        "credentialName":"lkasdlkfjlk",
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
                        "passwordFields":{
                           "serviceKey":serviceKey,
                           "projectName":projectName,
                           "projectId":projectId,
                           "serviceAccountName":serviceAccountName
                        }
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationgoogleasset"
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
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(572)
    def putAccountGoogleAsset(self):
        try:
            passed = False
            randID = 'MyGoogleAssetAc'
            randID += str(x)
            print (randID)
            projectName=utils.decodeCredential(google_projectName)
            serviceAccountName=utils.decodeCredential(google_serviceAccountName)
            projectId=utils.decodeCredential(google_projectId)
            bucket=utils.decodeCredential(google_bucket)
            serviceKey=utils.decodeCredential(google_serviceKey)
            dataset=utils.decodeCredential(google_dataset)


            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationgoogleasset"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":data["basicInfo"]["accountName"],
                     "serviceProviderType":"google",
                     "isActive":"Active",
                     "accountType":"subaccount",
                     "userType":"asset",
                     "serviceProviderCode":"google",
                     "credential_count":1
                  },
                  "advancedInfo":{
                    "projectName": projectName,
                    "serviceAccountName": serviceAccountName,
                    "projectId": projectId
                  },
                  "credentials":[
                     {
                        "credentialName":"lkasdlkfjlk",
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
                        "passwordFields":{
                           "serviceKey":serviceKey,
                           "projectName":projectName,
                           "projectId":projectId,
                           "serviceAccountName":serviceAccountName
                        }
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationgoogleasset"
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
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(573)
    def getAccountByProviderCodeGoogleAsset(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeAsset("google")
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

    @assignOrder(574)
    def deleteAccountGoogleAsset(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationgoogleasset"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False
