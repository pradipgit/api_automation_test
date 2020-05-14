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
azurecredRef_asset="azure-cref-asset-001"
azurecredRef_billing="azure-cref-billing-001"
# azure
azure_subscriptionID = config.get('azure', 'subscriptionID')
azure_offerID = config.get('azure', 'offerID')
azure_tenantID = config.get('azure', 'tenantID')


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

            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)

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
                            "crefId": azurecredRef_billing,
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
            ##print body
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


    @assignOrder(211)
    def putAccountAzure(self):
        try:
            passed = False
            accountNumber= "1234567890aa",
            randID = 'TestAzureNew'
            randID += str(x)
            print (randID)

            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)

            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationazure"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)
            # pragma: whitelist secret
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
                            "crefId": azurecredRef_billing,
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
            else :
                status['CAM-APITest'] = False
                return False
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
            else:
                status['CAM-APITest'] = False
                return False
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
                resp = self.api_client.createAzureBilling_CredRefs()
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp = self.api_client.createAzureBilling_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createAzureBilling_CredRefs()
            print (resp)
            return False

    @assignOrder(401)
    def CORE2250_postAccountAzureMinimalInfo(self):
        passed = False
        randID = 'TestAZureAcMinimal'
        randID += str(x)
        print (randID)

        subscriptionID=utils.decodeCredential(azure_subscriptionID)
        offerID=utils.decodeCredential(azure_offerID)
        tenantID=utils.decodeCredential(azure_tenantID)

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

######### Azure V2 Asset #############

    @assignOrder(555)
    def postAccountAzureAsset(self):
        passed = False
        randID = 'TestAZureAssetAc'
        randID += str(x)
        print (randID)

        subscriptionID=utils.decodeCredential(azure_subscriptionID)
        offerID=utils.decodeCredential(azure_offerID)
        tenantID=utils.decodeCredential(azure_tenantID)

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
                    "crefId": azurecredRef_asset,
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
        else:
            status['CAM-APITest'] = False
            return False

    @assignOrder(556)
    def putAccountAzureAsset(self):
        passed = False
        randID = 'TestAzureNew'
        randID += str(x)
        print (randID)

        subscriptionID=utils.decodeCredential(azure_subscriptionID)
        offerID=utils.decodeCredential(azure_offerID)
        tenantID=utils.decodeCredential(azure_tenantID)

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
                    "crefId": azurecredRef_asset,
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
        else :
            status['CAM-APITest'] = False
            return False

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
                resp = self.api_client.createAzure_CredRefs()
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp = self.api_client.createAzure_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createAzure_CredRefs()
            print (resp)
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
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False
