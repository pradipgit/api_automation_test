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
import sys
global status
import time
status = {}
logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
now = datetime.datetime.now()
x = random.randint(0, 50000)
global id_cred,metadata,audit_log_download_id,user_name
id_cred={}
metadata={}
audit_log_download_id={}
amazoncredRef="amazon-cref-001"
amazoncredRef_invalid="amazon-cref-001-invalid"

aws_s3Bucket = config.get('aws', 's3Bucket')


class AmazonTest(object):
    def __init__(self,client):

        self.api_client = client
        self.invoice_id = random.randint(100000,999999)
        global user_name

        if(sys.argv[1]=='automation-core-b'):
            user_name = config.get('params', 'username_mt')
        else:
            user_name = config.get('params', 'username')

    @assignOrder(1)
    def postAccountAWS(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            print (amazoncredRef)

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
                                "crefId": amazoncredRef,
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
                                "crefId": amazoncredRef,
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
            else :
                status['CAM-APITest'] = False
                return False
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

        ##print body
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



############### V2 Asset AWS accounts ######################

    @assignOrder(6)
    def postAccountAWSAsset(self):
        passed = False
        randID = 'TestAWSAssetAc'
        randID += str(x)
        print (randID)

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
                    "context": [
                                    {
                                        "team": [
                                            "CORE-X"
                                        ]
                                    }
                                ],
                    "crefId": amazoncredRef,
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
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
            status['CAM-APITest'] = passed
            return passed
        else :
            status['CAM-APITest'] = False
            return False

    @assignOrder(7)
    def putAccountAWSAsset(self):
        passed = False
        randID = 'MyAmazon'
        randID += str(x)
        print (randID)
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
                    "crefId": amazoncredRef,
                 }
              ],
               "accountId": "f16b0f4a-a76e-499e-b5f7-testautomationawsasset"
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

    @assignOrder(8)
    def getAccountByProviderCodeAWSAsset(self):
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
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
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
            else :
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(11)
    def getAccountsLimitAndPage(self):
        try:
            passed = False
            resp, body = self.api_client.get_AccountsLimitAndPage()
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

    @assignOrder(12)
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
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(13)
    def postAccountAWS_EmptyName_EmptyId(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)

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
                                "crefId": amazoncredRef,
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
            # #print body
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2("%20")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2("%20")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2("%20")
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False

    @assignOrder(14)
    def createBillingAccount(self):
        try :
            passed = False
            randID = 'TestBillingAccount'
            randID += str(x)
            print (randID)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
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
            passOfResponseCode = assertEqual(resp, 200)
            resp1=resp
            if (resp1==200 or resp1==201 or resp1==409):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(15)
    def getAccountByProviderCodeAWS(self):
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

    @assignOrder(16)
    def postAccount_CORE_5768(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            credid2="123456"
            credname2="amzcred2"

            body = {
               "account":
                {
                    "basicInfo": {
                        "accountName": id1,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456"
                    },
                    "credentials": [

                    ],
                    "accountId": id1
                }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # POST Credentials
            body = {
					"credentials":
                        {
                            "credentialName": credname,
                            "id":credid,
                            "status": "Active",
                            "crefId": amazoncredRef,
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {
                                    "team": [
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            body = {
					"credentials":
                        {
                            "credentialName": credname2,
                            "id":credid2,
                            "status": "Active",
                            "crefId": amazoncredRef,
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {
                                    "org": [
                                        "org_all"
                                    ]
                                }
                            ]
                        }
    				};
            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if(passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return

    @assignOrder(17)
    def postAccount_CORE_7351_PatchCredential_SamePayload(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            body = {
               "account":
                {
                    "basicInfo": {
                        "accountName": id1,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456"
                    },
                    "credentials": [

                    ],
                    "accountId": id1
                }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # POST Credentials
            body = {
					"credentials":
                        {
                            "credentialName": credname,
                            "id":credid,
                            "status": "Active",
                            "crefId": amazoncredRef,
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {
                                    "team": [
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)

            # do a patch on credentials
            body = {
                    "credentialName": credname,
                    "id":credid,
                    "status": "Active",
                    "crefId": amazoncredRef,
                    "purpose": [
                        "provisioning"
                    ],
                    "context": [
                        {
                            "team": [
                                team
                            ]
                        }
                    ]
    				};

            resp, body = self.api_client.patchAccountCredentials(body,id1,credid)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if(passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return

    @assignOrder(18)
    def postAccount_CORE_7351_PatchCredential(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            credname2="amzcred2"

            body = {
               "account":
                {
                    "basicInfo": {
                        "accountName": id1,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456"
                    },
                    "credentials": [

                    ],
                    "accountId": id1
                }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # POST Credentials
            body = {
					"credentials":
                        {
                            "credentialName": credname,
                            "id":credid,
                            "status": "Active",
                            "crefId": amazoncredRef,
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {
                                    "team": [
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)

            # do a patch on credentials
            body = {
                    "credentialName": credname2,
                    "id":credid,
                    "status": "Active",
                    "crefId": amazoncredRef_invalid,
                    "purpose": [
                        "provisioning"
                    ],
                    "context": [
                        {
                            "org": [
                                "org_all"
                            ]
                        }
                    ]
    				};

            resp, body = self.api_client.patchAccountCredentials(body,id1,credid)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # Do get Account By id
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)
            actualCredentialName=data['credentials'][0]['credentialName']
            print (actualCredentialName)
            actualCredentialRefId=data['credentials'][0]['crefId']
            print (actualCredentialRefId)
            actualContext=data['credentials'][0]['context'][0]['org'][0]
            print (actualContext)

            if(passOfResponseCode and actualCredentialName==credname2 and actualCredentialRefId==amazoncredRef_invalid and actualContext=='org_all' ) :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                resp = self.api_client.createInvalidCredRef_Amazon()
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                resp = self.api_client.createInvalidCredRef_Amazon()
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            resp = self.api_client.createInvalidCredRef_Amazon()
            print (resp)
            return

    @assignOrder(19)
    def getAllProviderCount(self):
        try :
            passed = False
            resp, body = self.api_client.getServiceProviderCount()
            data = json.dumps(body)
            data = json.loads(data)
            print (data)
            print ("Amazon account count is:")
            amazonCount=data['amazon']
            print (data['amazon'])
            print ("Azure account count is:")
            azureCount=data['azure']
            print (data['azure'])
            print ("VRA account count is:")
            vraCount=data['vra']
            print (data['vra'])
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            totalCount=amazonCount+azureCount+vraCount
            print("total count is:")
            print(totalCount)

            # do a get call for amazon and get the count
            resp, body = self.api_client.getServiceProviderCount_ProviderCode('amazon')
            data = json.dumps(body)
            data = json.loads(data)
            print ("Amazon provider count is:")
            amz_provider_count=data[0]['total_rows']
            print (data[0]['total_rows'])

            # do a get call for azure and get the count
            resp, body = self.api_client.getServiceProviderCount_ProviderCode('azure')
            data = json.dumps(body)
            data = json.loads(data)
            print ("Azure provider count is:")
            azure_provider_count=data[0]['total_rows']
            print (data[0]['total_rows'])
            # do a get call for vra and get the count
            resp, body = self.api_client.getServiceProviderCount_ProviderCode('vra')
            data = json.dumps(body)
            data = json.loads(data)
            print ("VRA provider count is:")
            vra_provider_count=data[0]['total_rows']
            print (data[0]['total_rows'])

            total_provider_count=vra_provider_count+azure_provider_count+amz_provider_count
            print ("total provider count is:")
            print (total_provider_count)

            if(passOfResponseCode and total_provider_count==totalCount) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(20)
    def createMasterAccount_VerifyAuditLog_CORE_6550(self):
        try:
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            id="f16b0f4a-log-Verification"
            accountName=randID+ "amazon"
            print (accountName)

            # print metadata[0]
            body = {
                   "account":{
                      "basicInfo":{
                         "accountName": accountName,
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
                    "accountId": id
                   }
                };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            passOfResponseCode = assertEqual(resp, 200)

            time.sleep(3)

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('MASTER_ACCOUNT_CREATE')
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            actualAccountName = data['result'][0]['resourceName']
            print (data['result'][0]['resourceId'])

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records

            if(passOfResponseCode and actualAccountName == accountName and audit_component == 'Account Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            return False

    @assignOrder(21)
    def deleteMasterAccount_VerifyAuditLog_CORE_6550(self):
        try:
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            id="f16b0f4a-log-Verification"
            accountName=randID+ "amazon"
            # print metadata[0]
            body = {
                   "account":{
                      "basicInfo":{
                         "accountName": accountName,
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
                    "accountId": id
                   }
                };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)

            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('MASTER_ACCOUNT_DELETE')
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            actualresourceId = data['result'][0]['resourceId']
            print (data['result'][0]['resourceId'])

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records

            if(id == actualresourceId and audit_component == 'Account Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            return False

    @assignOrder(22)
    def createAssetAccount_VerifyAuditLog_CORE_6550(self):
        try:
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            id="f16b0f4a-log-Verification"
            accountName=randID+ "amazon"
            # print metadata[0]
            body = {
                   "account":{
                      "basicInfo":{
                         "accountName": accountName,
                         "serviceProviderType":"amazon",
                         "isActive":"Active",
                         "accountType":"subaccount",
                         "userType":"asset",
                         "serviceProviderCode":"amazon"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": id
                   }
                };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            passOfResponseCode = assertEqual(resp, 200)

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('ASSET_ACCOUNT_CREATE')
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            actualAccountName = data['result'][0]['resourceName']
            print (data['result'][0]['resourceId'])

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records

            if(passOfResponseCode and actualAccountName == accountName and audit_component == 'Account Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            return False

    @assignOrder(23)
    def deleteAssetAccount_VerifyAuditLog_CORE_6550(self):
        try:
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            id="f16b0f4a-log-Verification"
            accountName=randID+ "amazon"
            # print metadata[0]
            body = {
                   "account":{
                      "basicInfo":{
                         "accountName": accountName,
                         "serviceProviderType":"amazon",
                         "isActive":"Active",
                         "accountType":"subaccount",
                         "userType":"asset",
                         "serviceProviderCode":"amazon"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": id
                   }
                };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)

            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            passOfResponseCode = assertEqual(resp, 204)

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('ASSET_ACCOUNT_DELETE')
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            actualresourceId = data['result'][0]['resourceId']
            print (data['result'][0]['resourceId'])

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records

            if(passOfResponseCode and id == actualresourceId and audit_component == 'Account Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            return False

    @assignOrder(24)
    def createAccountCredential_VerifyAuditLog_CORE_6550(self):
        try:
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            id="f16b0f4a-log-Verification"
            accountName=randID+ "amazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            body = {
                   "account":{
                      "basicInfo":{
                         "accountName": accountName,
                         "serviceProviderType":"amazon",
                         "isActive":"Active",
                         "accountType":"subaccount",
                         "userType":"asset",
                         "serviceProviderCode":"amazon"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": id
                   }
                };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)

            body = {
					"credentials":
                        {
                            "credentialName": credname,
                            "id":credid,
                            "status": "Active",
                            "crefId": amazoncredRef,
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {
                                    "team": [
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('ASSET_CREDENTIAL_ADD')
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            actualresourceId = data['result'][0]['resourceId']
            print (data['result'][0]['resourceId'])

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records
            if(passOfResponseCode and credid == actualresourceId and audit_component == 'Account Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False

    @assignOrder(25)
    def patchAccountCredential_VerifyAuditLog_CORE_6550(self):
        try:
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            id="f16b0f4a-log-Verification"
            accountName=randID+ "amazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            credname2="amzcred2"

            body = {
                   "account":{
                      "basicInfo":{
                         "accountName": accountName,
                         "serviceProviderType":"amazon",
                         "isActive":"Active",
                         "accountType":"subaccount",
                         "userType":"asset",
                         "serviceProviderCode":"amazon"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": id
                   }
                };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)

            body = {
					"credentials":
                        {
                            "credentialName": credname,
                            "id":credid,
                            "status": "Active",
                            "crefId": amazoncredRef,
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {
                                    "team": [
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id)
            print (resp)

            # patch credential
            # do a patch on credentials
            body = {
                    "credentialName": credname2,
                    "id":credid,
                    "status": "Active",
                    "crefId": amazoncredRef_invalid,
                    "purpose": [
                        "provisioning"
                    ],
                    "context": [
                        {
                            "team": [
                                team
                            ]
                        }
                    ]
    				};

            resp, body = self.api_client.patchAccountCredentials(body,id,credid)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('ASSET_CREDENTIAL_UPDATE')
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            actualresourceId = data['result'][0]['resourceId']
            print (data['result'][0]['resourceId'])

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records
            if(passOfResponseCode and credid == actualresourceId and audit_component == 'Account Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                resp = self.api_client.createInvalidCredRef_Amazon()
                print (resp)
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                resp = self.api_client.createInvalidCredRef_Amazon()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            resp = self.api_client.createInvalidCredRef_Amazon()
            print (resp)
            return False

    @assignOrder(26)
    def deleteAccountCredential_VerifyAuditLog_CORE_6548(self):
        try:
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            id="f16b0f4a-log-Verification"
            accountName=randID+ "amazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            credname2="amzcred2"

            body = {
                   "account":{
                      "basicInfo":{
                         "accountName": accountName,
                         "serviceProviderType":"amazon",
                         "isActive":"Active",
                         "accountType":"subaccount",
                         "userType":"asset",
                         "serviceProviderCode":"amazon"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": id
                   }
                };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)

            body = {
					"credentials":
                        {
                            "credentialName": credname,
                            "id":credid,
                            "status": "Active",
                            "crefId": amazoncredRef,
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {
                                    "team": [
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id)
            print (resp)

            # delete credentials
            resp, body = self.api_client.deleteAccountCredentials(id,credid)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('ASSET_CREDENTIAL_DELETE')
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            actualresourceId = data['result'][0]['resourceId']
            print (data['result'][0]['resourceId'])

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records
            if(passOfResponseCode and credid == actualresourceId and audit_component == 'Account Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False


    @assignOrder(27)
    def verifyCredRef_AccountDelete(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            print (amazoncredRef)

            id="f16b0f4a-cred-ref-validation"

            body = {"account":
                    {
                        "accountId": id,

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
                                "crefId": amazoncredRef,
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

            # delete getAccounts
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)

            # try to create account one more time with same credRef

            body = {"account":
                    {
                        "accountId": id,

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
                                "crefId": amazoncredRef,
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
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False
