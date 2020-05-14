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
accountId = config.get('param', 'accountId')
username1 = config.get('authorization', 'username_systemuser_cicd')
apikey1 = config.get('authorization', 'apikey_systemuser_cicd')

global headersUser1

class AccountCredential(object):
    def __init__(self,client):
        global headersUser1
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

        headersUser1 = {
            "Username": username1,
            "Content-Type": "application/json",
            "apikey": apikey1
        }



############## CORE-5203 ##################

    @assignOrder(1)
    def postAccountAWS(self):
        try:
            passed = False
            randID = 'TestAWSAcTest1'
            randID += str(x)
            print (randID)

            body = {"account":
                {
                    "accountId": "activeAccount_manage_8",

                    "basicInfo": {
                        "accountName": "activeAccount_manage_8" + randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset",
                        "parentAccountId": "default_billing_account_amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "amazon11158"
                    },
                    "credentials": [
                        {
                            "credentialName": "testcred1",

                            "passwordFields": {
                                "secretKey": "amazon11158",
                                "accessKey": "amazon11158"
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
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(2)
    def postAccountAWS_Inactive(self):
        try:
            passed = False
            randID = 'TestAWSAcTest2'
            randID += str(x)
            print (randID)

            body = {"account":
                {
                    "accountId": "InactiveAccount_manage_8",

                    "basicInfo": {
                        "accountName": "InactiveAccount_manage_8" + randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "InActive",
                        "userType": "asset",
                        "parentAccountId": "default_billing_account_amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "amazon11158"
                    },
                    "credentials": [
                        {
                            "credentialName": "testcred1",

                            "passwordFields": {
                                "secretKey": "amazon11158",
                                "accessKey": "amazon11158"
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
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(3)
    def get_allAccountsV2_manageFalse(self):
        try:
            passed = False
            resp, body = self.api_client.getAllProviders_manageFalse()
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            i = 1
            while i <= 10:
                print (data[i]['basicInfo']['isActive'])
                if (data[i]['basicInfo']['isActive']) == "Active":
                    passed = True
                    status['CAM-APITest'] = passed
                    i += 1
                else:
                    status['CAM-APITest'] = False
                    return False

            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(4)
    def get_accountByID_active(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByIds_manage("activeAccount_manage_8","true")
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            # print data
            print (data ['accountId'])
            accId=data ['accountId']
            passOfResponseCode = assertEqual(resp, 200)
            if(accId is not None):
                if (passOfResponseCode):
                    passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else :
                    status['CAM-APITest'] = False
                    return False
            else :
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(5)
    def get_accountByID_InActive(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByIds_manage("InactiveAccount_manage_8","false")
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

    @assignOrder(6)
    def deleteAccountAWS_active(self):
        try:
            passed = False
            id = "activeAccount_manage_8"
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

    @assignOrder(7)
    def deleteAccountAWS_inactive(self):
        try:
            passed = False
            id = "InactiveAccount_manage_8"
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

    @assignOrder(8)
    def postAccountAWS_Inactive_cred(self):
        try:
            passed = False
            randID = 'TestAWSAcTest3'
            randID += str(x)
            print (randID)

            body = {"account":
                {
                    "accountId": "inactive_cred_8",
                    "basicInfo": {
                        "accountName": "inactive_cred_8" + randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset",
                        "parentAccountId": "default_billing_account_amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "amazon11158"
                    },
                    "credentials": [
                        {
                            "credentialName": "testcred1",

                            "passwordFields": {
                                "secretKey": "amazon11158",
                                "accessKey": "amazon11158"
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
                            "status": "InActive"
                        }
                    ]

                }
            };

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

    @assignOrder(9)
    def get_account_inactiveCred_manageTrue(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByIds_manage("inactive_cred_8", "true")
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['credentials'][0]['credentialName'])
            credName = data['accountId']
            passOfResponseCode = assertEqual(resp, 200)
            if (credName is not None):
                if (passOfResponseCode):
                    passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    status['CAM-APITest'] = False
                    return False
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(10)
    def get_accountByID_InActive(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountByIds_manage("inactive_cred_8", "false")
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['credentials'])
            cred = data['credentials']
            passOfResponseCode = assertEqual(resp, 200)
            if (cred == []):
                if (passOfResponseCode):
                    passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    status['CAM-APITest'] = False
                    return False
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(11)
    def deleteAccountAWS_InActive_cred(self):
        try:
            passed = False
            id = "inactive_cred_8"
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
    def postAccountAWS_InactiveAccount_WithActiveCredential_Id(self):
        try:
            passed = False
            randID = 'TestAWSAcTest3'
            randID += str(x)
            print (randID)

            body = {"account":
                {
                    "accountId": "inactive_cred_9",
                    "basicInfo": {
                        "accountName": "inactive_cred_9" + randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "InActive",
                        "userType": "asset",
                        "parentAccountId": "default_billing_account_amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "amazon11158"
                    },
                    "credentials": [
                        {
                            "credentialName": "testcred1",

                            "passwordFields": {
                                "secretKey": "amazon11158",
                                "accessKey": "amazon11158"
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
                    ],
                    "id": "cred1"

                }
            };

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

    @assignOrder(13)
    def get_credenital_InActive_Account(self):
        try:
            passed = False
            print (headersUser1)
            resp, body = self.api_client.get_credentials_manage("inactive_cred_9","cred1","false",headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 403)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(14)
    def putAccountAWS_Account(self):
        try:
            passed = False
            randID = 'TestAWSAcTest3'
            randID += str(x)
            print (randID)

            body = {"account":
                {
                    "accountId": "inactive_cred_9",
                    "basicInfo": {
                        "accountName": "inactive_cred_9" + randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset",
                        "parentAccountId": "default_billing_account_amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "amazon11158"
                    },
                     "credentials": [
                        {
                            "credentialName": "testcred1",
                            "passwordFields": {
                                "accessKey": "********",
                                "secretKey": "********"
                            },
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ],
                                    "contextId": "066e274f-24eb-4641-b7db-01e97f3b5074"
                                }
                            ],
                            "status": "Active",
                            "id": "cred1"
                        }
                    ]

                }
            };

            resp, body = self.api_client.update_account(body,"inactive_cred_9")
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

    @assignOrder(15)
    def get_credenital_Active_Account(self):
        try:
            passed = False
            print (headersUser1)
            resp, body = self.api_client.get_credentials_manage("inactive_cred_9", "cred1", "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['credentials'][0]['credentialName'])
            cred = data['credentials'][0]['credentialName']
            if (cred is not None):
                if (passOfResponseCode):
                    passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else :
                    status['CAM-APITest'] = False
                    return False
            else :
                status['CAM-APITest'] = False
                return False

        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(16)
    def putAccountAWS_Inactive_Credential_Account(self):
        try:
            passed = False
            randID = 'TestAWSAcTest3'
            randID += str(x)
            print (randID)

            body = {"account":
                {
                    "accountId": "inactive_cred_9",
                    "basicInfo": {
                        "accountName": "inactive_cred_9" + randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset",
                        "parentAccountId": "default_billing_account_amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "amazon11158"
                    },
                    "credentials": [
                        {
                            "credentialName": "testcred1",
                            "passwordFields": {
                                "accessKey": "********",
                                "secretKey": "********"
                            },
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {
                                    "team": [
                                        "CORE-X"
                                    ],
                                    "contextId": "066e274f-24eb-4641-b7db-01e97f3b5074"
                                }
                            ],
                            "status": "InActive",
                            "id": "cred1"
                        }
                    ]

                }
            };

            resp, body = self.api_client.update_account(body, "inactive_cred_9")
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

    @assignOrder(17)
    def get_Inactive_credenital_ManageTrue(self):
        try:
            passed = False
            print (headersUser1)
            resp, body = self.api_client.get_credentials_manage("inactive_cred_9", "cred1", "true", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['credentials'][0]['credentialName'])
            cred = data['credentials'][0]['credentialName']
            if (cred is not None):
                if (passOfResponseCode):
                    passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    status['CAM-APITest'] = False
                    return False
            else:
                status['CAM-APITest'] = False
                return False

        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(18)
    def get_Inactive_credenital_ManageFalse(self):
        try:
            passed = False
            print (headersUser1)
            resp, body = self.api_client.get_credentials_manage("inactive_cred_9", "cred1", "False", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
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

    @assignOrder(19)
    def deleteAccountAWS(self):
        try:
            passed = False
            id = "inactive_cred_9"
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
