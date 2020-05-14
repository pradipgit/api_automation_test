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
vracredRef_asset="vra-cref-asset-001"
vracredRef_billing="vra-cref-billing-001"


vra_endPointVersion = config.get('vraBilling', 'endPointVersion')
vra_url = config.get('vraBilling', 'url')
vra_tenant = config.get('vraBilling', 'tenant')


class VraTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

    @assignOrder(230)
    def postAccountVRA(self):
        try:
            passed = False
            randID = 'TestVRAAcNew'
            randID += str(x)
            print (randID)

            endPointVersion=utils.decodeCredential(vra_endPointVersion)
            url=utils.decodeCredential(vra_url)
            tenant=utils.decodeCredential(vra_tenant)

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": "vra"+randID,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "vra",
                        "serviceProviderType": "vra",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "accountNumber": "vraAccount77",
                        "endPointVersion": endPointVersion,
                        "url" : url,
                        "tenant" : tenant
                    },
                    "credentials": [
                        {
                            "credentialName": "wwwwwwww",
                            "purpose": [
                                "costIngestion"
                            ],
                            "crefId": vracredRef_billing,
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
                    "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationvraNew1"

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


    @assignOrder(231)
    def putAccountVRA(self):
        try:
            passed = False
            randID = 'MyAmazon'
            randID += str(x)
            print (randID)

            endPointVersion=utils.decodeCredential(vra_endPointVersion)
            url=utils.decodeCredential(vra_url)
            tenant=utils.decodeCredential(vra_tenant)

            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationvraNew1"
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
                        "serviceProviderCode": "vra",
                        "serviceProviderType": "vra",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "accountNumber": "vraAccount77",
                        "endPointVersion": endPointVersion,
                        "url" : url,
                        "tenant" : tenant
                    },
                    "credentials": [
                        {
                            "credentialName": "wwwwwwww",
                            "purpose": [
                                "costIngestion"
                            ],
                            "crefId": vracredRef_billing,
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
                    "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationvraNew1"

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


    @assignOrder(232)
    def getAccountByProviderCodeVRA(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCode("vra")
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


    @assignOrder(233)
    def deleteAccountVRA(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationvraNew1"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp = self.api_client.createVRABilling_CredRefs()
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp = self.api_client.createVRABilling_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createVRABilling_CredRefs()
            print (resp)
            return False

    @assignOrder(403)
    def CORE2250_postAccountVRAMinimalInfo(self):
        try:
            passed = False
            randID = 'TestVRAAcMinimal'
            randID += str(x)
            print (randID)

            endPointVersion=utils.decodeCredential(vra_endPointVersion)
            url=utils.decodeCredential(vra_url)
            tenant=utils.decodeCredential(vra_tenant)

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": randID,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "vra",
                        "serviceProviderType": "vra",
                        "credential_count": 1
                    },
                    "advancedInfo": {
                        "accountNumber": "vraAccount77",
                        "endPointVersion": endPointVersion,
                        "url" : url,
                        "tenant" : tenant
                    },
                    "credentials": [

                    ],
                    "accountId": "f16b0f4a-a76e-499e-VRA-testautomationVRA"
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


################# V2 account VRA Asset #################

    @assignOrder(563)
    def postAccountVRAAsset(self):
        try:
            passed = False
            randID = 'TestVRAAssetAc'
            randID += str(x)
            print (randID)

            endPointVersion=utils.decodeCredential(vra_endPointVersion)
            url=utils.decodeCredential(vra_url)
            tenant=utils.decodeCredential(vra_tenant)

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":randID,
                     "serviceProviderType":"vra",
                     "isActive":"Active",
                     "accountType":"subaccount",
                     "userType":"asset",

                     "serviceProviderCode":"vra",
                     "credential_count":1
                  },
                  "advancedInfo":{
                      "accountNumber": "vraAccount77",
                      "endPointVersion": endPointVersion,
                      "url" : url,
                      "tenant" : tenant
                  },
                  "credentials":[
                     {
                        "credentialName":"fasdfasdf",
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
                            "crefId": vracredRef_asset
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationvraasset"
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


    @assignOrder(564)
    def putAccountVRAAsset(self):
        try:
            passed = False
            randID = 'TestVRAAssetAc'
            randID += str(x)
            print (randID)

            endPointVersion=utils.decodeCredential(vra_endPointVersion)
            url=utils.decodeCredential(vra_url)
            tenant=utils.decodeCredential(vra_tenant)

            id1 = "f16b0f4a-a76e-499e-b5f7-testautomationvraasset"
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)

            body = {
               "account":{
                  "basicInfo":{
                     "accountName":data["basicInfo"]["accountName"],
                     "serviceProviderType":"vra",
                     "isActive":"Active",
                     "accountType":"subaccount",
                     "userType":"asset",
                     "serviceProviderCode":"vra",
                     "credential_count":1
                  },
                  "advancedInfo":{
                      "accountNumber": "vraAccount77",
                      "endPointVersion": endPointVersion,
                      "url" : url,
                      "tenant" : tenant
                  },
                  "credentials":[
                     {
                        "credentialName":"fasdfasdf",
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
                            "crefId": vracredRef_asset
                     }
                  ],
                   "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationvraasset"
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


    @assignOrder(565)
    def getAccountByProviderCodeVRAAsset(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByProviderCodeAsset("vra")
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

    @assignOrder(566)
    def deleteAccountVRAAsset(self):
        try:
            passed = False
            id = "f16b0f4a-a76e-499e-b5f7-testautomationvraasset"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                resp = self.api_client.createVRA_CredRefs()
                print (resp)
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                resp = self.api_client.createVRA_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createVRA_CredRefs()
            print (resp)
            return False

    @assignOrder(567)
    def deleteAccount_VRA_MinimalInfo(self):
        try:
            passed = False
            id = 'f16b0f4a-a76e-499e-VRA-testautomationVRA'
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
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
