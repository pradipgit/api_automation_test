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
x = random.randint(0, 50000)
global id_cred,metadata,audit_log_download_id
id_cred={}
metadata={}
audit_log_download_id={}

amazon_accessKey = config.get('aws', 'accessKey')
amazon_secretKey = config.get('aws', 'secretKey')
aws_s3Bucket = config.get('aws', 's3Bucket')

class AmazonTest(object):
    def __init__(self,client):

        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

    @assignOrder(1)
    def postAccountAWS(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            body = {"account":
                    {
                        "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationaws",
                        "basicInfo": {
                            "accountName": "amazon"+randID,
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset"
                        },
                        "advancedInfo": {
                            "accountNumber": "amazon11158"
                        },
                        "credentials": [
                            {
                                "credentialName": "amazon11158",
                                "passwordFields": {
                                    "secretKey": secretKey,
                                    "accessKey": accessKey
                                },
                                "purpose": [
                                    "provisioning"
                                ],
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
                        ]

                    }
                    };


            resp, body = self.api_client.create_account(body)
            print (resp)
            #print body
            logger.info("API response:" + str(resp))
            passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['message'],'Accounts creation successful'))
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


    @assignOrder(2)
    def putAccountAWS(self):
        try:
            passed = False
            randID = 'MyAmazon'
            randID += str(x)
            print (randID)
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)
            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationaws"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)


            body= {"account":
                    {
                        "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationaws",

                        "basicInfo": {
                            "accountName": "amazon"+randID,
                            "serviceProviderId": None,
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset"

                        },
                        "advancedInfo": {
                            "accountNumber": "amazon11158"

                        },
                        "credentials": [
                            {
                                "credentialName": "amazon11158",
                                "status": "Active",
                                "passwordFields": {
                                    "secretKey": secretKey+randID,
                                    "accessKey": accessKey+randID
                                },
                                "purpose": [
                                    "provisioning"
                                ],
                                "context": [
                                    {
                                        "team": [
                                            "CORE-X"
                                        ]
                                    }
                                ]
                            }
                        ]

                    }
                    };

            resp, body = self.api_client.update_account(body, id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['translateCode'],'CO200_SUCCESSFULLY_UPDATE_ACC_AND_SUBACC'))
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(3)
    def deleteAccountAWS(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationaws"
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

    @assignOrder(4)
    def getAccountByWrongProviderCode(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCode("amazon1")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(5)
    def postAccountAWSMinimalInfo(self):
        passed = False
        randID = 'TestAWSAcMinimal'
        randID += str(x)
        print (randID)

        s3Bucket=utils.decodeCredential(aws_s3Bucket)

        body = {
               "account":{
                  "basicInfo":{
                     "accountName":randID,
                     "serviceProviderType":"amazon",
                     "isActive":"Active",
                     "accountType":"master",
                     "userType":"billing",
                     "serviceProviderCode":"amazon"
                  },
                  "advancedInfo":{
                     "accountNumber":"3245235249",
                      "s3Bucket": s3Bucket
                  },
                  "credentials":[

                  ],
                "accountId": "f16b0f4a-a76e-499e-aws-testautomationAmazon"
               }
            };

        #print body
        resp, body = self.api_client.create_account(body)
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['translateCode'],'CO200_ACC_CREATED_SUCCESSFULLY'))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


############### V2 Asset AWS accounts ######################

    @assignOrder(6)
    def postAccountAWSAsset(self):
        passed = False
        randID = 'TestAWSAssetAc'
        randID += str(x)
        print (randID)

        s3Bucket=utils.decodeCredential(aws_s3Bucket)
        accessKey=utils.decodeCredential(amazon_accessKey)
        secretKey=utils.decodeCredential(amazon_secretKey)

        body = {
           "account":{
              "basicInfo":{
                 "accountName":randID,
                 "serviceProviderType":"amazon",
                 "isActive":"Active",
                 "accountType":"subaccount",
                 "userType":"asset",
                 "serviceProviderCode":"amazon",
                 "credential_count":1
              },
              "advancedInfo":{
                 "accountNumber":"lkjaslkdj"
              },
              "credentials":[
                 {
                    "credentialName":"lkjadslkj",
                    "purpose":[
                       "provisioning"
                    ],
                    "status":"Active",
                    "context":
                        [
                            {
                            "team": [
                                "CORE-X"
                            ]
                            }
                        ],
                    "passwordFields":{
                       "accessKey":accessKey,
                       "secretKey":secretKey
                    }
                 }
              ],
               "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationawsasset"
           }
        };

        #print body
        resp, body = self.api_client.create_account(body)
        print (resp)
        #print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['translateCode'],'CO200_ACC_CREATED_SUCCESSFULLY'))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(7)
    def putAccountAWSAsset(self):
        passed = False
        randID = 'MyAmazon'
        randID += str(x)
        print (randID)

        s3Bucket=utils.decodeCredential(aws_s3Bucket)
        accessKey=utils.decodeCredential(amazon_accessKey)
        secretKey=utils.decodeCredential(amazon_secretKey)

        id1 = "f16b0f4a-a76e-499e-b5f7-testautomationawsasset"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body={
           "account":{
              "basicInfo":{
                 "accountName":data["basicInfo"]["accountName"],
                 "serviceProviderType":"amazon",
                 "isActive":"Active",
                 "accountType":"subaccount",
                 "userType":"asset",
                 "serviceProviderCode":"amazon",
                 "credential_count":1
              },
              "advancedInfo":{
                 "accountNumber":"lkjaslkdj"

              },
              "credentials":[
                 {
                    "credentialName":"lkjadslkj",
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
                       "accessKey":accessKey,
                       "secretKey":secretKey
                    }
                 }
              ],
               "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationawsasset"
           }
        };

        resp, body = self.api_client.update_account(body, id1)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = (assertEqual(resp, 200) & assertEqual(body['translateCode'],'CO200_SUCCESSFULLY_UPDATE_ACC_AND_SUBACC'))
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(8)
    def getAccountByProviderCodeAWSAsset(self):
        randID = 'MyAmazon'
        randID += str(x)
        print(randID)
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeAsset("amazon")
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

    @assignOrder(9)
    def deleteAccountAWSAsset(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationawsasset"
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

    @assignOrder(10)
    def getAccountByWrongProviderCodeAsset(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeAsset("amazon1")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(11)
    def deleteAccountAmazonMinimalInfo(self):
        try:
            passed = False
            id = 'f16b0f4a-a76e-499e-aws-testautomationAmazon'
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

    @assignOrder(12)
    def postAccountAWS_EmptyName_EmptyId(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)

            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            body = {"account":
                    {
                        "accountId": " ",
                        "basicInfo": {
                            "accountName": " ",
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset"

                        },
                        "advancedInfo": {
                            "accountNumber": "amazon11158"
                        },
                        "credentials": [
                            {
                                "credentialName": "amazon11158",
                                "passwordFields": {
                                    "accessKey":accessKey,
                                    "secretKey":secretKey
                                },
                                "purpose": [
                                    "provisioning"
                                ],
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
                        ]

                    }
                    };


            resp, body = self.api_client.create_account(body)
            print (resp)
            #print body
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400) & assertEqual(body[1]['message'],'Invalid Account Id, please provide id which contains alphanumeric & special characters(-_) only.')
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2("%20")
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2("%20")
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2("%20")
            print (resp)
            return False

    @assignOrder(13)
    def createBillingAccount(self):
        try :
            passed = False
            randID = 'TestBillingAccount'
            randID += str(x)
            print (randID)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)
            body = {
                   "account":{
                      "basicInfo":{
                         "accountName":"amazon"+randID,
                         "serviceProviderType":"amazon",
                         "isActive":"Active",
                         "accountType":"master",
                         "userType":"billing",
                         "serviceProviderCode":"amazon"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249",
                          "s3Bucket": s3Bucket
                      },
                      "credentials":[

                      ],
                       "accountId": "f16b0f4a-Billing-AutomationAccount"
                   }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200) & assertEqual(body['translateCode'],'CO200_ACC_CREATED_SUCCESSFULLY')
            resp1=resp
            if (resp1==200 or resp1==201 or resp1==409 or passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(14)
    def getAccountByProviderCodeAWS(self):
        randID = 'MyAmazon' + 'TestBillingAccount'
        randID += str(x)
        print(randID)
        try:
            passed = False
            accountId= "f16b0f4a-Billing-AutomationAccount"
            resp, body = self.api_client.get_AccountByProviderCode("amazon")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            return False
