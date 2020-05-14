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


snow_username = config.get('snowBilling', 'username')
snow_password = config.get('snowBilling', 'password')
snow_version = config.get('snowBilling', 'version')
snow_url = config.get('snowBilling', 'url')


class SnowTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

    @assignOrder(240)
    def postAccountSnow(self):
        try:
            passed = False

            version=utils.decodeCredential(snow_username)
            url=utils.decodeCredential(snow_password)
            userName=utils.decodeCredential(snow_version)
            password=utils.decodeCredential(snow_url)

            randID = 'TestSnowAc'
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
                        "serviceProviderCode": "snow",
                        "serviceProviderType": "snow"
                    },
                    "advancedInfo": {
                        "version": version,
                        "url" :url
                    },
                    "credentials": [
                        {
                            "credentialName": "kjkkkjk",
                            "purpose": [
                                "costIngestion"
                            ],

                            "passwordFields": {
                                "userName": userName,
                                "url": url,
                                "password": password
                            },
                            "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ]
                                }
                            ],
                            "status": "Active"
                        }
                    ],
                    "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationsnowNewV"
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


    @assignOrder(241)
    def putAccountSnow(self):
        try:
            passed = False

            version=utils.decodeCredential(snow_username)
            url=utils.decodeCredential(snow_password)
            userName=utils.decodeCredential(snow_version)
            password=utils.decodeCredential(snow_url)

            randID = 'MyAmazon'
            randID += str(x)
            print (randID)
            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationsnowNewV"
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
                        "serviceProviderCode": "snow",
                        "serviceProviderType": "snow",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "version": version,
                        "url" :url
                    },
                    "credentials": [
                        {
                            "credentialName": "kjkkkjk",
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
                                "userName": userName,
                                "url": url,
                                "password": password
                            }
                        }
                    ],
                    "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationsnowNewV"
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


    @assignOrder(242)
    def getAccountByProviderCodeSnow(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCode("snow")
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


    @assignOrder(243)
    def deleteAccountSnow(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationsnowNewV"
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

    @assignOrder(405)
    def CORE2250_postAccountSnowMinimalInfo(self):
        passed = False
        randID = 'TestSnowAcMinimal'
        randID += str(x)
        print (randID)
        # print metadata[0]
        version=utils.decodeCredential(snow_username)
        url=utils.decodeCredential(snow_password)
        userName=utils.decodeCredential(snow_version)
        password=utils.decodeCredential(snow_url)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": randID,
                    "accountType": "master",
                    "isActive": "Active",
                    "userType": "billing",
                    "serviceProviderCode": "snow",
                    "serviceProviderType": "snow",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "version": version,
                    "url" :url
                },
                "credentials": [

                ],
                "accountId": "f16b0f4a-a76e-499e-snow-testautomationsnow"
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

################### V2 System accounts SNOW  ########################


    @assignOrder(525)
    def postAccountSnowSystem(self):
        passed = False
        randID = 'TestSnowSystemAc'
        randID += str(x)
        print (randID)
        # print metadata[0]
        version=utils.decodeCredential(snow_username)
        url=utils.decodeCredential(snow_password)
        userName=utils.decodeCredential(snow_version)
        password=utils.decodeCredential(snow_url)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": randID,
                    "accountType": "master",
                    "isActive": "Active",
                    "userType": "system",
                    "serviceProviderCode": "snow",
                    "serviceProviderType": "snow",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "version": version,
                    "url" :url
                },
                "credentials": [
                    {
                        "credentialName": "kjkkkjk",
                        "purpose": [
                            "systemIntegration"
                        ],

                        "passwordFields": {
                            "userName": userName,
                            "url": url,
                            "password": password
                        },
                        "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ]
                                }
                            ],
                            "status": "Active"
                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationsnowsystemNewV"
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

    @assignOrder(526)
    def putAccountSnowSystem(self):
        passed = False
        randID = 'MyAmazon'
        randID += str(x)
        print (randID)
        version=utils.decodeCredential(snow_username)
        url=utils.decodeCredential(snow_password)
        userName=utils.decodeCredential(snow_version)
        password=utils.decodeCredential(snow_url)

        id1 = "f16b0f4a-a76e-499e-b5f7-testautomationsnowsystemNewV"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "accountType": "master",
                    "isActive": "Active",
                    "userType": "system",
                    "serviceProviderCode": "snow",
                    "serviceProviderType": "snow",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "version": version,
                    "url" :url
                },
                "credentials": [
                    {
                        "credentialName": "kjkkkjk",
                        "purpose": [
                            "systemIntegration"
                        ],

                        "passwordFields": {
                            "userName": userName,
                            "url": url,
                            "password": password
                        },
                        "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ]
                                }
                            ],
                            "status": "Active"
                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationsnowsystemNewV"
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

    @assignOrder(527)
    def getAccountByProviderCodeSnowSystem(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeSystem("snow")
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

    @assignOrder(528)
    def deleteAccountSnowSystem(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationsnowsystemNewV"
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

#################### V2 account SNOW ##################


    @assignOrder(567)
    def postAccountSnowAsset(self):
        passed = False
        randID = 'TestSnowAssetAc'
        randID += str(x)
        print (randID)
        # print metadata[0]

        version=utils.decodeCredential(snow_username)
        url=utils.decodeCredential(snow_password)
        userName=utils.decodeCredential(snow_version)
        password=utils.decodeCredential(snow_url)

        body = {
           "account":{
              "basicInfo":{
                 "accountName":randID,
                 "serviceProviderType":"snow",
                 "isActive":"Active",
                 "accountType":"subaccount",
                 "userType":"asset",
                 "serviceProviderCode":"snow",
                 "credential_count":1
              },
              "advancedInfo":{
                 "version": version,
                 "url" :url
              },
              "credentials":[
                 {
                    "credentialName":"lkjalksdfjlkj",
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
                       "userName": userName,
                       "password": password
                    }
                 }
              ],
               "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationsnowasset"
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


    @assignOrder(568)
    def putAccountSnowAsset(self):
        passed = False
        randID = 'MyAmazon'
        randID += str(x)
        print (randID)
        version=utils.decodeCredential(snow_username)
        url=utils.decodeCredential(snow_password)
        userName=utils.decodeCredential(snow_version)
        password=utils.decodeCredential(snow_url)

        id1 = "f16b0f4a-a76e-499e-b5f7-testautomationsnowasset"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
           "account":{
              "basicInfo":{
                 "accountName":data["basicInfo"]["accountName"],
                 "serviceProviderType":"snow",
                 "isActive":"Active",
                 "accountType":"subaccount",
                 "userType":"asset",
                 "serviceProviderCode":"snow",
                 "credential_count":1
              },
              "advancedInfo":{
                 "version": version,
                 "url" :url
              },
              "credentials":[
                 {
                    "credentialName":"lkjalksdfjlkj",
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
                      "userName": userName,
                      "password": password
                    }
                 }
              ],
               "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationsnowasset"
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

    @assignOrder(569)
    def getAccountByProviderCodeSnowAsset(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeAsset("snow")
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

    @assignOrder(570)
    def deleteAccountSnowAsset(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationsnowasset"
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

    @assignOrder(571)
    def deleteAccount_SNOW_MinimalInfo(self):
        try:
            passed = False
            id = 'f16b0f4a-a76e-499e-snow-testautomationsnow'
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
