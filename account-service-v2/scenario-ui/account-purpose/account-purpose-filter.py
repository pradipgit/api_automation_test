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
crefId_amazon = "amazon-cref-001"
crefId_icd="icd-cref-001"
aws_s3Bucket = config.get('aws', 's3Bucket')
icd_url = config.get('icd', 'url')

class AccountPurpose(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

    @assignOrder(1)
    def postAccountAWS(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print (randID)

        s3Bucket=utils.decodeCredential(aws_s3Bucket)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": randID,
                    "accountType": "master",
                    "isActive": "Active",
                    "userType": "billing",
                    "serviceProviderType": "amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "098098908098098",
                    "s3Bucket": s3Bucket
                },
                "credentials": [
                    {
                        "credentialName": "hjhkjh",
                        "purpose": [
                            "costIngestion"
                        ],
                        "status":"Active",
                        "crefId": crefId_amazon,
                        "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ]
                                }
                            ]
                    }
                ],
                "accountId": "123f16b0f4a-a76e-499e-b5f7-testautomationawsbilllingAccount"
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

    @assignOrder(2)
    def postAccountAWSAsset(self):
        passed = False
        randID = 'TestAWSAssetAc'
        randID += str(x)
        print (randID)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": randID,
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "lkjasdjfljasd"
                },
                "credentials": [
                    {
                        "credentialName": "autocred1",
                        "purpose": [
                            "provisioning"
                        ],
                        "status": "Active",
                        "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ]
                                }
                            ],
                         "crefId": crefId_amazon,
                    }
                ],
                "accountId": "123f16b0f4a-a76e-499e-b5f7-testautomation_amazon_assetAccount"
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

    @assignOrder(3)
    def postAccountICD(self):
        passed = False
        randID = 'TestICDAc'
        randID += str(x)
        print (randID)

        url=utils.decodeCredential(icd_url)

        body = {
            "account": {
                "basicInfo": {
                        "accountName": "testDataAccountforICDNewAccountViz",
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
                        "credentialName": "fasdf",
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
                         "crefId":crefId_icd
                    }
                ],
                "accountId": "123f16b0f4a-a76e-499e-b5f7-testautomationicdviz12211AccountViz"
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

    @assignOrder(4)
    def getPurposeFilter_Asset(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x)+"bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                 "page": 1,
                "limit": 1,
                "sort": "true",
                "sortBy": "accountName",
                "serviceProviderCode": "amazon",
                "purpose": "provisioning",
                "view": "summary",
                "accountType" : "asset"
            };
            resp, body = self.api_client.getPurpose_AssetFilter(body)
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

    @assignOrder(5)
    def getPurposeFilter_Billing(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x)+"bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 2,
                "limit": 2,
                "sort": "true",
                "sortBy": "accountName",
                "serviceProviderCode": "amazon",
                "purpose": "costIngestion",
                "view": "summary",
                "accountType": "billing"
            };
            resp, body = self.api_client.getPurpose_BillingFilter(body)
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

    @assignOrder(6)
    def getPurposeFilter_System(self):
        try:
            passed = False
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 1,
                "limit": 10,
                "sort": "true",
                "sortBy": "accountName",
                "serviceProviderCode": "icd",
                "purpose": "systemIntegration",
                "view": "summary",
                "accountType": "system"
            };
            resp, body = self.api_client.getPurpose_SystemFilter(body)
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

    @assignOrder(7)
    def getPurposeFilter_InvalidServiceProviderCode(self):
            try:
                passed = False
                body = {
                    "context": [
                        {"tagType": "team", "tagValueCode": "CORE-X"}

                    ],
                    "page": 2,
                    "limit": 2,
                    "sort": "true",
                    "sortBy": "accountName",
                    "serviceProviderCode": "amazon4545454",
                    "purpose": "costIngestion",
                    "view": "summary",
                    "accountType": "billing"
                };
                resp, body = self.api_client.getPurpose_BillingFilter(body)
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

    @assignOrder(8)
    def getPurposeFilter_InvalidPurpose(self):
        try:
            passed = False
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 2,
                "limit": 2,
                "sort": "true",
                "sortBy": "accountName",
                "serviceProviderCode": "amazon",
                "purpose": "billing2222",
                "view": "summary",
                "accountType": "billing"
            };
            resp, body = self.api_client.getPurpose_AssetFilter(body)
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

    @assignOrder(9)
    def getPurposeFilter_ByInvalidSortBy(self):
        try:
            passed = False
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 2,
                "limit": 2,
                "sort": "true",
                "sortBy": "accountName121212",
                "serviceProviderCode": "amazon",
                "purpose": "provisioning",
                "view": "summary",
                "accountType": "asset"
            };
            resp, body = self.api_client.getPurpose_AssetFilter(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(10)
    def getPurposeFilter_ByProvisioning(self):
            try:
                passed = False
                body = {
                    "context": [
                        {"tagType": "team", "tagValueCode": "CORE-X"}

                    ],
                    "page": 2,
                    "limit": 2,
                    "sort": "true",
                    "sortBy": "accountName",
                    "serviceProviderCode": "amazon",
                    "purpose": "provisioning",
                    "view": "summary",
                    "accountType": "asset"
                };
                resp, body = self.api_client.getPurpose_AssetFilter(body)
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

    @assignOrder(11)
    def getPurposeFilter_ByDetailsView(self):
            try:
                passed = False
                body = {
                    "context": [
                        {"tagType": "team", "tagValueCode": "CORE-X"}

                    ],
                    "page": 2,
                    "limit": 2,
                    "sort": "true",
                    "sortBy": "accountName",
                    "serviceProviderCode": "amazon",
                    "purpose": "provisioning",
                    "view": "detailed",
                    "accountType": "asset"
                };
                resp, body = self.api_client.getPurpose_AssetFilter(body)
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

    @assignOrder(12)
    def getInvalidPurposeFilter_System(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 2,
                "limit": 2,
                "sort": "true",
                "sortBy": "accountName",
                "serviceProviderCode": "amazon",
                "purpose": "systemIntegration",
                "view": "summary"
            };
            resp, body = self.api_client.getPurpose_SystemFilter(body)
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

    @assignOrder(13)
    def getPurposeFilter_ByInvalidPage(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": -1,
                "limit": 2,
                "sort": "true",
                "sortBy": "accountName",
                "serviceProviderCode": "amazon",
                "purpose": "costIngestion",
                "view": "summary"
            };
            resp, body = self.api_client.getPurpose_BillingFilter(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(14)
    def getPurposeFilter_ByInvalidLimit(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 1,
                "limit": -1,
                "sort": "true",
                "sortBy": "accountName",
                "serviceProviderCode": "amazon",
                "purpose": "costIngestion",
                "view": "summary"
            };
            resp, body = self.api_client.getPurpose_BillingFilter(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(15)
    def getPurposeFilter_ByInvalidView(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 1,
                "limit": 1,
                "sort": "true",
                "sortBy": "accountName",
                "serviceProviderCode": "amazon",
                "purpose": "costIngestion",
                "view": "summary22222"
            };
            resp, body = self.api_client.getPurpose_BillingFilter(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(16)
    def getPurposeFilter_ByExtraParameter(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 1,
                "limit": 1,
                "sort": "true",
                "sortBy": "accountName",
                "serviceProviderCode": "amazon",
                "purpose": "costIngestion",
                "view": "summary22222",
                "test": "333",
                "test": "3333"
            };
            resp, body = self.api_client.getPurpose_BillingFilter(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(17)
    def getPurposeFilter_ByRemoveParameter(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 1,
                "limit": 1,
                "sort": "true",
                "sortBy": "accountName",
                "purpose": "costIngestion",
                "view": "summary22222"
            };
            resp, body = self.api_client.getPurpose_BillingFilter(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(18)
    def getPurposeFilter_ByRemoveServiceProvider(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 1,
                "limit": 1,
                "sort": "false",
                "sortBy": "accountName",
                "purpose": "costIngestion",
                "view": "summary"
            };
            resp, body = self.api_client.getPurpose_BillingFilter(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(19)
    def getPurposeFilter_InvalidTagValue(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 1,
                "limit": 1,
                "sort": "false",
                "sortBy": "accountName",
                "purpose": "costIngestion",
                "view": "summary"
            };
            resp, body = self.api_client.getPurpose_BillingFilter(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(20)
    def getPurposeFilter_ByInvalidPurpose(self):
        try:
            passed = False
            randID = config.get('param', 'random_code_purpose')
            randID += str(x) + "bb"
            print (randID)
            body = {
                "context": [
                    {"tagType": "team", "tagValueCode": "CORE-X"}

                ],
                "page": 1,
                "limit": 1,
                "sort": "false",
                "sortBy": "accountName",
                "purpose": "assetIngestion",
                "view": "summary"
            };
            resp, body = self.api_client.getPurpose_BillingFilter(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(21)
    def deleteAccountAWS(self):
        try:
            passed = False
            id = "123f16b0f4a-a76e-499e-b5f7-testautomationawsbilllingAccount"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False

    @assignOrder(22)
    def deleteAccountICD(self):
        try:
            passed = False
            id = "123f16b0f4a-a76e-499e-b5f7-testautomationicdviz12211AccountViz"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                resp = self.api_client.createICD_CredRefs()
                print (resp)
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                resp = self.api_client.createICD_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createICD_CredRefs()
            print (resp)
            return False

    @assignOrder(23)
    def deleteAssetAccount_AWS(self):
        try:
            passed = False
            id = "123f16b0f4a-a76e-499e-b5f7-testautomation_amazon_assetAccount"
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False
