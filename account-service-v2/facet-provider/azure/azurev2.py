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

# azure
azure_subscriptionID = config.get('azure', 'subscriptionID')
azure_offerID = config.get('azure', 'offerID')
azure_tenantID = config.get('azure', 'tenantID')
azure_applicationsecret = config.get('azureBilling', 'applicationsecret')
azure_domain = config.get('azure', 'domain')
azure_clientid = config.get('azure', 'clientid')
azure_secret = config.get('azure', 'secret')



class AzureTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)


    @assignOrder(210)
    def postAccountAzure(self):
        try:
            passed = False
            randID = 'TestAZureAc'
            randID += str(x)
            print (randID)
            # print metadata[0]
            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)
            applicationSecret=utils.decodeCredential(azure_applicationsecret)

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": randID,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "azure",
                        "serviceProviderType": "azure",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "subscriptionID": subscriptionID,
                        "offerID": offerID,
                        "tenantID": tenantID
                    },
                    "credentials": [
                        {
                            "credentialName": "ljlkajslkfdjlkasjdf",
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
                            "passwordFields": {
                                "applicationSecret": applicationSecret
                            },
                            "status": "Active",
                            "accountNumber": "1234567890aa",
                            "tenantID": tenantID,
                            "applicationID": offerID
                        }
                    ],
                    "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationazure"
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


    @assignOrder(211)
    def putAccountAzure(self):
        try:
            passed = False
            accountNumber= "1234567890aa",
            randID = 'MyAmazon'
            randID += str(x)
            print (randID)
            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationazure"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)

            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)
            applicationSecret=utils.decodeCredential(azure_applicationsecret)

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": data["basicInfo"]["accountName"],
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "azure",
                        "serviceProviderType": "azure",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "subscriptionID": subscriptionID,
                        "offerID": offerID,
                        "tenantID": tenantID
                    },
                    "credentials": [
                        {
                            "credentialName": "ljlkajslkfdjlkasjdf",
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
                                "applicationSecret": applicationSecret
                            },
                            "accountNumber": accountNumber,
                            "tenantID": tenantID,
                            "applicationID": offerID
                        }
                    ],
                    "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationazure"
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


    @assignOrder(212)
    def getAccountByProviderCodeAzure(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCode("azure")
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

    @assignOrder(213)
    def deleteAccountAzure(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationazure"
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

    @assignOrder(401)
    def CORE2250_postAccountAzureMinimalInfo(self):
        passed = False
        randID = 'TestAZureAcMinimal'
        randID += str(x)
        print (randID)
        # print metadata[0]

        subscriptionID=utils.decodeCredential(azure_subscriptionID)
        offerID=utils.decodeCredential(azure_offerID)
        tenantID=utils.decodeCredential(azure_tenantID)
        applicationSecret=utils.decodeCredential(azure_applicationsecret)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": randID,
                    "accountType": "master",
                    "isActive": "Active",
                    "userType": "billing",
                    "serviceProviderCode": "azure",
                    "serviceProviderType": "azure",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "subscriptionID": subscriptionID,
                    "offerID": offerID,
                    "tenantID": tenantID
                },
                "credentials": [

                ],
                "accountId": "f16b0f4a-a76e-499e-azure-testautomationAzure"
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

######### Azure V2 Asset #############

    @assignOrder(555)
    def postAccountAzureAsset(self):
        passed = False
        randID = 'TestAZureAssetAc'
        randID += str(x)
        print (randID)
        # print metadata[0]

        subscriptionID=utils.decodeCredential(azure_subscriptionID)
        offerID=utils.decodeCredential(azure_offerID)
        tenantID=utils.decodeCredential(azure_tenantID)
        applicationSecret=utils.decodeCredential(azure_applicationsecret)
        clientId=utils.decodeCredential(azure_clientid)
        secret=utils.decodeCredential(azure_secret)
        domain=utils.decodeCredential(azure_domain)


        body = {
           "account":{
              "basicInfo":{
                 "accountName":randID,
                 "serviceProviderType":"azure",
                 "isActive":"Active",
                 "accountType":"subaccount",
                 "userType":"asset" ,
                 "serviceProviderCode":"azure",
                 "credential_count":1
              },
              "advancedInfo":{
                 "subscriptionID": subscriptionID,
                 "offerID": offerID,
                 "tenantID": tenantID
              },
              "credentials":[
                 {
                    "credentialName":"asdfadsf",
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
                       "clientId":clientId,
                       "secret":secret,
                       "subscriptionID": subscriptionID,
                       "offerID": offerID,
                       "tenantID": tenantID,
                       "domain":domain
                    }
                 }
              ],
               "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationazureasset"
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

    @assignOrder(556)
    def putAccountAzureAsset(self):
        passed = False
        randID = 'MyAmazon'
        randID += str(x)
        print (randID)

        subscriptionID=utils.decodeCredential(azure_subscriptionID)
        offerID=utils.decodeCredential(azure_offerID)
        tenantID=utils.decodeCredential(azure_tenantID)
        applicationSecret=utils.decodeCredential(azure_applicationsecret)
        clientId=utils.decodeCredential(azure_clientid)
        secret=utils.decodeCredential(azure_secret)
        domain=utils.decodeCredential(azure_domain)


        id1 = "f16b0f4a-a76e-499e-b5f7-testautomationazureasset"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
           "account":{
              "basicInfo":{
                 "accountName":data["basicInfo"]["accountName"],
                 "serviceProviderType":"azure",
                 "isActive":"Active",
                 "accountType":"subaccount",
                 "userType":"asset",
                 "serviceProviderCode":"azure",
                 "credential_count":1
              },
              "advancedInfo":{
                 "subscriptionID": subscriptionID,
                 "offerID": offerID,
                 "tenantID": tenantID
              },
              "credentials":[
                 {
                    "credentialName":"asdfadsf",
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
                       "clientId":clientId,
                       "secret":secret,
                       "subscriptionID": subscriptionID,
                       "offerID": offerID,
                       "tenantID": tenantID,
                       "domain":domain
                    }
                 }
              ],
               "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationazureasset"
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

    @assignOrder(557)
    def getAccountByProviderCodeAzureAsset(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeAsset("azure")
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

    @assignOrder(558)
    def deleteAccountAzureAsset(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationazureasset"
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

    @assignOrder(559)
    def deleteAccountAzureMinimalInfo(self):
        try:
            passed = False
            id = 'f16b0f4a-a76e-499e-azure-testautomationAzure'
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
