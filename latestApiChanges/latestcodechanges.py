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
from pprint import pprint
import random
global status
from os import path
import os
status = {}
logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
now = datetime.datetime.now()
x = random.randint(0, 80000)
user_name = config.get('params', 'username')
crefId2 = ""
username1 = config.get('authorization', 'username_systemuser')
apikey1 = config.get('authorization', 'apikey_systemuser')
global headersUser1
crefId = "automationTesting"
ROOT_DIR = os.path.abspath(os.curdir)
serviceProvider_folder = path.join(ROOT_DIR + "/testdata", "service-provider")
serviceProviderMetadata_folder = path.join(ROOT_DIR + "/testdata", "service-provider-metadata")
file_to_open = path.join(serviceProvider_folder, "sprovider.json")
file_to_open_metadata = path.join(serviceProviderMetadata_folder, "sproviderMetadata.json")
amazoncredRef="amazon-cref-001"
aws_s3Bucket = config.get('aws', 's3Bucket')
azure_subscriptionID = config.get('azure', 'subscriptionID')
azure_offerID = config.get('azure', 'offerID')
azure_tenantID = config.get('azure', 'tenantID')
vra_endPointVersion = config.get('vraBilling', 'endPointVersion')
vra_url = config.get('vraBilling', 'url')
vra_tenant = config.get('vraBilling', 'tenant')
amazon_accessKey = config.get('aws', 'accessKey')
amazon_secretKey = config.get('aws', 'secretKey')

class lastetCodeChanges(object):
    def __init__(self, client):
        global headersUser1
        self.api_client = client
        headersUser1 = {
            "Username": username1,
            "Content-Type": "application/json",
            "apikey": utils.decodeCredential(apikey1)
        }
        with open(file_to_open, "r+") as jsonFile:
            self.testdatajson = json.load(jsonFile)
            jsonFile.close()
        with open(file_to_open_metadata, "r+") as jsonFile:
            self.testdatajsonMetadata = json.load(jsonFile)
            jsonFile.close()

    @assignOrder(1)
    def getAccountByID_SystemUser(self):
        try:
            passed = False
            randID = 'automationtest'
            randID += str(x)
            print(randID)
            print(amazoncredRef)
            accountId = 'f16b0f4a-100-automation'

            body = {"account":
                {
                    "accountId": accountId,
                    "basicInfo": {
                        "accountName": "amazon" + randID,
                        "serviceProviderType": "aws",
                        "serviceProviderCode": "aws",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                    },
                    "advancedInfo": {
                        "accountNumber": "12345678"
                    },
                    "credentials": [
                        {
                            "credentialName": "cred1",
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
            print(resp)

            # do a get call
            resp, body = self.api_client.getCredRefCredentialById(amazoncredRef, headersUser1)
            print(resp)
            data = json.dumps(body)
            data = json.loads(data)
            access_Key = data['accessKey']
            secret_Key = data['secretKey']
            print(access_Key)
            print(secret_Key)
            # do a get call
            resp, body = self.api_client.getAccountById_SystemUser(accountId, headersUser1)
            print(resp)
            data = json.dumps(body)
            data = json.loads(data)
            access_Key_byid = data['credentials'][0]['passwordFields']['accessKey']
            secret_Key_byid = data['credentials'][0]['passwordFields']['secretKey']
            print(access_Key_byid)
            print(secret_Key_byid)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and access_Key==access_Key_byid and secret_Key==secret_Key_byid):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print(resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print(resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print(resp)
            return False

    @assignOrder(2)
    def validateAccountwithDuplicateCredentialName_CORE5657(self):
        try:
            passed = False
            accountId = ""
            data = json.load(open('payload.json'))
            resp, body = self.api_client.create_account(data["account_duplicate_credentials"])
            accountId = data["account_duplicate_credentials"]["account"]["accountId"]
            print  ("Create Account Response is :")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            # get account by ID
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                print ("Failed to Create Account with both Credential Names are Same")
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print ("Created Account with Duplicate Credential Names")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print ("Created Account with Duplicate Credential Names")
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False

    @assignOrder(3)
    def validateAccountwithMixedInvalidContextTeam(self):
        try:

            passed = False
            accountId = ""
            data = json.load(open('payload.json'))
            resp, body = self.api_client.create_account(data["account_Mixedinvalid_credentials"])
            print  ("Create Account Response is :")
            print (resp)
            accountId = data["account_Mixedinvalid_credentials"]["account"]["accountId"]

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)

            # get account by ID
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                print ("Failed to Create Account with Invalid Team")
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print ("Created Account with with Invalid Team")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print ("Created Account with with Invalid Team")
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False

    @assignOrder(4)
    def validateAccountwithMixedInvalidContextTeam_Org(self):
        try:
            passed = False
            accountId = ""
            data = json.load(open('payload.json'))
            resp, body = self.api_client.create_account(data["account_Mixedinvalid_credentials_team_org"])
            print  ("Create Account Response is :")
            print (resp)
            logger.info("API response:" + str(resp))

            data = json.load(open('payload.json'))
            accountId = data["account_Mixedinvalid_credentials_team_org"]["account"]["accountId"]
            resp, body = self.api_client.deleteAccountV2(accountId)

            passOfResponseCode = assertEqual(resp, 404)

            # get account by ID
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                print ("Failed to Create Account with Invalid Org")
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print ("Created Account with with Invalid Org")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print ("Created Account with with Invalid Org")
            print (resp)
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False

    @assignOrder(5)
    def postAccount_validMultipleContexts(self):
        try:
            passed = False
            data = json.load(open('payload.json'))

            resp, body = self.api_client.create_account(data["account_multipleContext"])
            print  ("Create Account Response is :")
            print (resp)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            accountId = data["account_multipleContext"]["account"]["accountId"]
            print (accountId)

            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print  ("Deletd the Account")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print  ("Deletd the Account")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            print  ("Deletd the Account")
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False

    @assignOrder(6)
    def validateUpdateAccountName(self):
        try:

            data = json.load(open('payload.json'))
            actualAccountName = data["account_amazon_1"]["account"]["basicInfo"]["accountName"]
            updatedAccountName = data["account_amazon_2"]["account"]["basicInfo"]["accountName"]
            updatedAccountNumber = data["account_amazon_2"]["account"]["advancedInfo"]["accountNumber"]
            accountId = data["account_amazon_1"]["account"]["accountId"]
            print ("account id is:")
            print (accountId)
            passed = False
            resp, body = self.api_client.create_account(data["account_amazon_1"])
            print  ("Create Account Response is :")
            print (resp)
            resp, body = self.api_client.update_account(data["account_amazon_2"], accountId)
            print ("Update Account Response is :")
            print (resp)
            # get account by ID
            resp, body = self.api_client.get_AccountById(accountId)
            data = json.dumps(body)
            data = json.loads(data)
            print ("GET Account Response is :")
            print (resp)
            accountName = data['basicInfo']['accountName']
            print ("accountName after GET Call is:")
            print (accountName)
            accoutNumber = data['advancedInfo']['accountNumber']
            print ("accoutNumber after GET Call is:")
            print (accoutNumber)
            print ("Expected accountName is:")
            print (updatedAccountName)
            print ("Expected accoutNumber is:")
            print (updatedAccountNumber)
            if (updatedAccountName == accountName) and (updatedAccountNumber == accoutNumber):
                passed = True
                status['CAM-APITest'] = passed
                data = json.load(open('payload.json'))
                resp, body = self.api_client.deleteAccountV2(accountId)
                print ("Account Number and Account Name Both Matched with Updated Record")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                data = json.load(open('payload.json'))
                resp, body = self.api_client.deleteAccountV2(accountId)
                print ("Account Number and Account Name Didnt Matched with Updated Record")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            print ("Account Number and Account Name Didnt Matched with Updated Record")
            data = json.load(open('payload.json'))
            resp, body = self.api_client.deleteAccountV2(accountId)
            print ("Account Number and Account Name  Didnt Matched with Updated Record")
            print (resp)
            print ("Deleted the Record")
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False

    # @assignOrder(7)
    # def put_aws_provider_invalidTeam(self):
    #     try:
    #         passed = False
    #
    #         randID = config.get('param', 'random_id_amazon')
    #         randID += str(x)
    #         print (randID)
    #         # post account
    #         body = {
    #             "account_name": "amazontestaccount"+randID,
    #             "account_type": "Provisioning",
    #             "provider_code": "amazon",
    #             "provider": "amazon",
    #             "provider_type": 0,
    #             "team": "CORE-X",
    #             "account_number": "2222",
    #             "password_fields": {
    #                 "access_key": "jjkMMMMMp",
    #                 "secret_key": "lkjalksdjflkafds"
    #             }
    #         }
    #         resp, body = self.api_client.create_provider(body)
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #
    #         # get account
    #
    #         resp, body = self.api_client.get_AccountByProviderType("0")
    #         data = json.dumps(body)
    #         data = json.loads(data)
    #
    #         body = {
    #             "account_name": data[0]['account_name'],
    #             "account_type": "Provisioning",
    #             "provider_code": "amazon",
    #             "provider": "amazon",
    #             "provider_type": 0,
    #             "team": "CORE-X123456",
    #             "account_number": data[0]['account_number'],
    #             "password_fields": {
    #                 "access_key": "jjkMMMMMp",
    #                 "secret_key": "lkjalksdjflkafds"
    #             }
    #         };
    #
    #         resp, body = self.api_client.update_provider(body, data[0]['id'])
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         passOfResponseCode = assertEqual(resp, 500)
    #         if (passOfResponseCode):
    #             passed = True
    #         status['CAM-APITest'] = passed
    #         return passed
    #     except:
    #         status['CAM-APITest'] = False
    #         return False

    @assignOrder(8)
    def postAccount_invalidPayloadContexts(self):
        try:
            passed = False
            data = json.load(open('payload.json'))

            resp, body = self.api_client.create_account(data["account_invalid_payload"])
            print  ("Create Account Response is :")
            print (resp)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)

            accountId = data["account_invalid_payload"]["account"]["accountId"]
            print (accountId)

            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print  ("Deletd the Account")
                print (resp)
                resp = self.api_client.createAWS_CredRefs()
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            print  ("Deletd the Account")
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            return False


    # @assignOrder(9)
    # def deleteAll_accounts(self):
    #     try:
    #         passed = False
    #         resp, body = self.api_client.getAllProviders_manageTrue()
    #         data = json.dumps(body)
    #         data = json.loads(data)
    #         print data
    #         i = 1
    #         while i <= 100:
    #             resp, body = self.api_client.deleteAccountV2(data[i]['accountId'])
    #             print (resp)
    #             i += 1
    #         passed = True
    #         status['CAM-APITest'] = passed
    #         return passed
    #
    #     except:
    #         status['CAM-APITest'] = False
    #         return False


    @assignOrder(10)
    def postSwagger(self):
        try:
            passed = False
            data = json.load(open('payload.json'))
            resp, body = self.api_client.post_swagger(data["swagger_post"])
            print ("Post Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 201)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                print ("Failed to Post Swagger Json")
                logger.info("Failed to Post Swagger Json")
                return False
        except:
            status['CAM-APITest'] = False
            print ("Failed to Post Swagger Json")
            logger.info("Failed to Post Swagger Json")
            return False

    @assignOrder(11)
    def postSwagger_duplicate(self):
        try:
            passed = False
            data = json.load(open('payload.json'))
            resp, body = self.api_client.post_swagger(data["swagger_post"])
            print ("Post Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 409)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                print ("Failed to Post Duplicate Swagger Json")
                logger.info("Failed to Post Duplicate Swagger Json")
                return False
        except:
            status['CAM-APITest'] = False
            print ("Failed to Post DuplicateSwagger Json")
            logger.info("Failed to Post Duplicate Swagger Json")
            return False

    @assignOrder(12)
    def getSwaggerByApplication_ascending(self):
        try:
            passed = False
            data = json.load(open('payload.json'))
            appName = data["swagger_post"]["appName"]
            print (appName)
            serviceName=data["swagger_post"]["service"]["serviceName"]
            print (serviceName)
            resp, body = self.api_client.get_swagger_appName_ascending()
            print ("GET Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            total_rows = data['total_rows']
            print (total_rows)
            i=0
            while i <= total_rows:
                print (data['applications'][i]['appName'])
                if data['applications'][i]['appName'] == appName :
                    print ("Application Name is:")
                    print (data['applications'][i]['appName'])
                    print ("Service Name is:")
                    print (data['applications'][i]['services'][0])
                    if data['applications'][i]['services'][0] == serviceName and passOfResponseCode :
                        passed = True
                        status['CAM-APITest'] = passed
                        return passed
                    else :
                        status['CAM-APITest'] = False
                        print ("Failed to GET Swagger Json by Application Name")
                        logger.info("Failed to GET Swagger Json by Application Name")
                        return False
                else:
                     i += 1
        except:
            status['CAM-APITest'] = False
            print ("Failed to GET Swagger Json by Application Name")
            logger.info("Failed to GET Swagger Json by Application Name")
            return False


    @assignOrder(13)
    def getSwaggerByApplication_descending(self):
        try:
            passed = False
            data = json.load(open('payload.json'))
            appName = data["swagger_post"]["appName"]
            print (appName)
            serviceName=data["swagger_post"]["service"]["serviceName"]
            print (serviceName)
            resp, body = self.api_client.get_swagger_appName_descending()
            print ("GET Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            total_rows = data['total_rows']
            print (total_rows)
            i=0
            while i <= total_rows:
                print (data['applications'][i]['appName'])
                if data['applications'][i]['appName'] == appName :
                    print ("Application Name is:")
                    print (data['applications'][i]['appName'])
                    print ("Service Name is:")
                    print (data['applications'][i]['services'][0])
                    if data['applications'][i]['services'][0] == serviceName and passOfResponseCode :
                        passed = True
                        status['CAM-APITest'] = passed
                        return passed
                    else :
                        status['CAM-APITest'] = False
                        print ("Failed to GET Swagger Json by Application Name")
                        logger.info("Failed to GET Swagger Json by Application Name")
                        return False
                else:
                     i += 1
        except:
            status['CAM-APITest'] = False
            print ("Failed to GET Swagger Json by Application Name")
            logger.info("Failed to GET Swagger Json by Application Name")
            return False

    @assignOrder(14)
    def getSwaggerByService(self):
        try:
            passed = False
            data = json.load(open('payload.json'))
            appName = data["swagger_post"]["appName"]
            print (appName)
            serviceName=data["swagger_post"]["service"]["serviceName"]
            print (serviceName)
            resp, body = self.api_client.get_swagger_serviceName(appName,serviceName)
            print ("GET Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                print ("Failed to GET Swagger Json by Service Name")
                logger.info("Failed to GET Swagger Json by Service Name")
                return False
        except:
            status['CAM-APITest'] = False
            print ("Failed to GET Swagger Json by Service Name")
            logger.info("Failed to GET Swagger Json by Service Name")
            return False

    @assignOrder(15)
    def deleteSwaggerByAppName(self):
        try:
            passed = False
            data = json.load(open('payload.json'))
            appName = data["swagger_post"]["appName"]
            print (appName)
            resp, body = self.api_client.delete_swagger_app(appName)
            print ("Delete Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                print ("Failed to Delete Swagger Json")
                logger.info("Failed to Delete Swagger Json")
                return False
        except:
            status['CAM-APITest'] = False
            print ("Failed to Delete Swagger Json")
            logger.info("Failed to Delete Swagger Json")
            return False

    @assignOrder(16)
    def putSwagger(self):
        try:
            passed = False
            data = json.load(open('payload.json'))
            resp, body = self.api_client.post_swagger(data["swagger_post"])
            print ("Post Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))

            appName = data["swagger_post"]["appName"]
            print (appName)
            serviceName = data["swagger_post"]["service"]["serviceName"]
            print (serviceName)

            resp, body = self.api_client.put_swagger(data["swagger_put"],appName,serviceName)
            print ("PUT Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))


            # get by service name
            resp, body = self.api_client.get_swagger_serviceName(appName,serviceName)
            print ("GET Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))

            data = json.dumps(body)
            data = json.loads(data)

            applicationName = data['appName']
            print ("Service name is :"+applicationName)

            serviceName=data['serviceName']
            print ("serviceName is :"+serviceName)

            swaggerType=data['swaggerType']
            print ("swaggerType is :"+swaggerType)

            swagger=data['swaggerData']['swagger']
            print ("swagger version is :"+swagger)

            team=data['swaggerData']['info']['team']
            print ("Team Name is :"+team)

            teamsize=data['swaggerData']['info']['teamsize']
            print ("teamsize is :"+teamsize)

            country=data['swaggerData']['info']['country']
            print ("country is :"+country)


            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and applicationName=="automation" and serviceName=="cb-credential-service_automation" and
             swaggerType=="json" and swagger=="2.0" and team=="CORE-B" and teamsize=="10" and country=="India") :
                    passed = True
                    status['CAM-APITest'] = passed
                    return passed
            else :
                    status['CAM-APITest'] = False
                    print ("Failed to Update Swagger Json")
                    logger.info("Failed to Update Swagger Json")
                    return False

        except:
            status['CAM-APITest'] = False
            print ("Failed to Update Swagger Json")
            logger.info("Failed to Update Swagger Json")
            return False

    @assignOrder(17)
    def deleteSwaggerByServiceName(self):
        try:
            passed = False
            data = json.load(open('payload.json'))
            appName = data["swagger_post"]["appName"]
            print (appName)
            serviceName = data["swagger_post"]["service"]["serviceName"]
            print (serviceName)
            resp, body = self.api_client.delete_swagger_service(appName,serviceName)
            print ("Delete Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                print ("Failed to Delete Swagger Json")
                logger.info("Failed to Delete Swagger Json")
                return False
        except:
            status['CAM-APITest'] = False
            print ("Failed to Delete Swagger Json")
            logger.info("Failed to Delete Swagger Json")
            return False

    @assignOrder(18)
    def postSwagger_InvalidKey(self):
        try:
            passed = False
            data = json.load(open('payload.json'))
            appName = data["swagger_post_invalidkeys"]["appName"]
            print (appName)
            serviceName = data["swagger_post_invalidkeys"]["service"]["serviceName"]
            print (serviceName)
            resp, body = self.api_client.post_swagger(data["swagger_post_invalidkeys"])
            print ("Post Swagger Response is :")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 201)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.delete_swagger_service(appName,serviceName)
                print ("Delete Swagger Response is :")
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                print ("Failed to Post Swagger Json")
                logger.info("Failed to Post Swagger Json")
                return False
        except:
            status['CAM-APITest'] = False
            print ("Failed to Post Swagger Json")
            logger.info("Failed to Post Swagger Json")
            resp, body = self.api_client.delete_swagger_service(appName,serviceName)
            print ("Delete Swagger Response is :")
            print (resp)
            return False

    @assignOrder(19)
    def postCurrency_VerifyLog(self):
        try:
            passed = False
            print ("Current date and time using str method of datetime object:")
            print (str(now))
            print ("Current year: %d" % now.year)
            print ("Current month: %d" % now.month)
            print ("Current day: %d" % now.day)
            day = len(str(now.day))
            if day < 2:
                day1 = "0" + str(now.day)
            else:
                day1 = str(now.day)

            month = len(str(now.month))
            if month < 2:
                month1 = "0" + str(now.month)
            else:
                month1 =  str(now.month)

            completeDate = str(now.year) + "-" + str(month1) + "-" + str(day1) + "T" + "18:25:43.511" + "Z"
            print (completeDate)
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                passOfResponseCode = assertEqual(resp, 201)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            id=data['id']

            #get the currency by ID
            resp, body = self.api_client.getConversionRatesById(id)
            print (resp)
            currency_date=data['changeHistory']['createdOn']
            print (data['changeHistory']['createdOn'])

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('CONVERSION_RATE_CREATE')
            print (resp)

            data = json.dumps(body)
            data = json.loads(data)

            audit_date = data['result'][0]['initiatedUTCDate']
            print (data['result'][0]['initiatedUTCDate'])

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records

            if(audit_date == currency_date and audit_component == 'Currency Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteConvertionRates(id)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteConvertionRates(id)
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteConvertionRates(id)
            print (resp)
            return False

    @assignOrder(20)
    def deleteCurrency_VerifyLog(self):
        try:
            passed = False
            print ("Current date and time using str method of datetime object:")
            print (str(now))
            print ("Current year: %d" % now.year)
            print ("Current month: %d" % now.month)
            print ("Current day: %d" % now.day)
            day = len(str(now.day))
            if day < 2:
                day1 = "0" + str(now.day)
            else:
                day1 = str(now.day)

            month = len(str(now.month))
            if month < 2:
                month1 = "0" + str(now.month)
            else:
                month1 =  str(now.month)

            completeDate = str(now.year) + "-" + str(month1) + "-" + str(day1) + "T" + "18:25:43.511" + "Z"
            print (completeDate)
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                passOfResponseCode = assertEqual(resp, 201)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            id=data['id']

            resp, body = self.api_client.deleteConvertionRates(id)
            print (resp)

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('CONVERSION_RATE_DELETE')
            print (resp)

            data = json.dumps(body)
            data = json.loads(data)

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records

            if(audit_component == 'Currency Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteConvertionRates(id)
            print (resp)
            return False

    @assignOrder(21)
    def putCurrency_VerifyLog(self):
        try:
            passed = False
            print ("Current date and time using str method of datetime object:")
            print (str(now))
            print ("Current year: %d" % now.year)
            print ("Current month: %d" % now.month)
            print ("Current day: %d" % now.day)
            day = len(str(now.day))
            if day < 2:
                day1 = "0" + str(now.day)
            else:
                day1 = str(now.day)

            month = len(str(now.month))
            if month < 2:
                month1 = "0" + str(now.month)
            else:
                month1 =  str(now.month)

            completeDate = str(now.year) + "-" + str(month1) + "-" + str(day1) + "T" + "18:25:43.511" + "Z"
            print (completeDate)
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                passOfResponseCode = assertEqual(resp, 201)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            id=data['id']

            # Update The currency conversion
            body = {
                "currencyfrom": "AUD",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "77"
            };


            resp, body = self.api_client.update_convertionRates(body, id);
            print (resp)

            #get the currency by ID
            resp, body = self.api_client.getConversionRatesById(id)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            currency_date=data['changeHistory']['updatedOn']
            print (data['changeHistory']['updatedOn'])

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('CONVERSION_RATE_UPDATE')
            print (resp)

            data = json.dumps(body)
            data = json.loads(data)

            audit_date = data['result'][0]['initiatedUTCDate']
            print (data['result'][0]['initiatedUTCDate'])

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records

            if(audit_date == currency_date and audit_component == 'Currency Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteConvertionRates(id)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteConvertionRates(id)
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteConvertionRates(id)
            print (resp)
            return False

    @assignOrder(22)
    def postCurrencyFailure_VerifyLog(self):
        try:
            passed = False
            print ("Current date and time using str method of datetime object:")
            print (str(now))
            print ("Current year: %d" % now.year)
            print ("Current month: %d" % now.month)
            print ("Current day: %d" % now.day)
            day = len(str(now.day))
            if day < 2:
                day1 = "0" + str(now.day)
            else:
                day1 = str(now.day)

            month = len(str(now.month))
            if month < 2:
                month1 = "0" + str(now.month)
            else:
                month1 =  str(now.month)

            completeDate = str(now.year) + "-" + str(month1) + "-" + str(day1) + "T" + "18:25:43.511" + "Z"
            print (completeDate)
            body = {
                "currencyfrom": "EUR",
                "currencyto": "EUR",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)

            # check the audit log
            resp, body = self.api_client.keyWordSearchText('CONVERSION_RATE_CREATE_FAILURE')
            print (resp)

            data = json.dumps(body)
            data = json.loads(data)

            audit_component = data['result'][0]['component']
            print (data['result'][0]['component'])

            audit_user = data['result'][0]['actorUid']
            print (data['result'][0]['actorUid'])

            # compare both the timings and other records

            if(audit_component == 'Currency Management' and audit_user == user_name):
                print ("Record Matched Successfully")
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(23)
    def createMasterAccount(self):
        passed = False
        accessKey=utils.decodeCredential(amazon_accessKey)
        secretKey=utils.decodeCredential(amazon_secretKey)
        s3Bucket=utils.decodeCredential(aws_s3Bucket)
        body =  {
                "account": {
                    "basicInfo": {
                        "accountName": "amz_master",
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "amazon11158",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [
                        {
                             "credentialName": "amazon11158",
                                "status": "Active",
                                "passwordFields": {
                                    "secretKey": secretKey,
                                    "accessKey": accessKey
                                },
                                "purpose": [
                                    "costIngestion"
                                ],
                                "context": [
                                    {
                                        "team": [
                                            "CORE-X"
                                        ]
                                    }
                                ]
                        }
                    ],
                    "accountId": "amz_master"
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
        else :
            status['CAM-APITest'] = False
            return passed
        return passed

    @assignOrder(24)
    def postAccount_WrongParentID(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)


            body = {"account":
                    {
                        "accountId": "amz_id_123",
                        "basicInfo": {
                            "accountName": "amazon"+randID,
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "parentAccountId": "1234567890"
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

    @assignOrder(25)
    def postAccount_ValidParentID(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)
            body = {"account":
                    {
                        "accountId": "amz_asset_account123",
                        "basicInfo": {
                            "accountName": "amz_asset_account123",
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "parentAccountId": "amz_master"
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


    @assignOrder(26)
    def getAccount_LinkTrue(self):
        try:
            passed = False
            id = "amz_master"
            assetAccountName_id="amz_asset_account123"
            serviceProviderCode="amazon"
            userType="asset"
            resp, body = self.api_client.getAccount_Link(id,"true")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            accountName=data[1]["basicInfo"]["accountName"]
            parentID=data[1]["basicInfo"]["parentAccountId"]
            servicecode=data[1]["basicInfo"]["serviceProviderCode"]
            type=data[1]["basicInfo"]["userType"]

            if (passOfResponseCode and accountName==assetAccountName_id and parentID==id  and
             userType==type and servicecode==serviceProviderCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(27)
    def getAccount_LinkFalse(self):
        try:
            id = "amz_master"
            assetAccountName_id="amz_asset_account123"
            passed = False
            try :
                resp, body = self.api_client.getAccount_Link(id,"false")
                print (resp)
                data = json.dumps(body)
                data = json.loads(data)
                total_rows=data[0]["total_rows"]
                print (total_rows)
            except:
                print ("No Records Found")
                passed = True
                status['CAM-APITest'] = passed
                return passed
            i=1
            while(i<=total_rows):
                print (data[i]["basicInfo"]["accountName"])
                if(data[i]["basicInfo"]["accountName"]==assetAccountName_id):
                    status['CAM-APITest'] = False
                    return passed
                else :
                    i += 1
                    passed = True
                    status['CAM-APITest'] = passed
                    return passed

        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(28)
    def deleteMasterAccount(self):
        try:
            passed = False
            id = "amz_master"
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
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(29)
    def getAssetAccount_DeletedMasterAcc(self):
        try:
            passed = False
            id = "amz_master"
            assetAccount_id="amz_asset_account123"
            resp, body = self.api_client.get_AccountById(assetAccount_id)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            try :
                parentID=data["basicInfo"]["parentAccountId"]
                print (parentID)
            except:
                parentID="NA"
                print (parentID)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and parentID=="NA"):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed

        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(30)
    def patchAccount_SamePayload(self):
        try:
            passed = False
            id = "amz_asset_account123"
            body =  {
                      "basicInfo":{
                            "accountName": id,
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber": "amazon11158"
                      }
                   };
            #print body
            resp, body = self.api_client.patchBasicAdvanceInfo(body,id)
            print (resp)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(31)
    def patchAccount_ChangeAccNumber(self):
        try:
            passed = False
            id = "amz_asset_account123"
            body =  {
                      "basicInfo":{
                            "accountName": id,
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber": id
                      }
                   };
            #print body
            resp, body = self.api_client.patchBasicAdvanceInfo(body,id)
            print (resp)

            resp, body = self.api_client.get_AccountById(id)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            actual_accountNumber= id
            expected_accountNumber=data["advancedInfo"]["accountNumber"]

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and actual_accountNumber==expected_accountNumber):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(32)
    def patchAccount_AddFields(self):
        try:
            passed = False
            id = "amz_asset_account123"
            body =  {
                      "basicInfo":{
                            "accountName": id,
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                             "description": id
                      },
                      "advancedInfo":{
                         "accountNumber": id
                      }
                   };
            #print body
            resp, body = self.api_client.patchBasicAdvanceInfo(body,id)
            print (resp)

            resp, body = self.api_client.get_AccountById(id)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            actual_description= id
            expected_description=data["basicInfo"]["description"]

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and actual_description==expected_description):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(33)
    def patchAccount_MultipleFieldChanges(self):
        try:
            passed = False
            id = "amz_asset_account123"
            body =  {
                      "basicInfo":{
                            "accountName": "amz_account_new",
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                             "description": "amz_account_new_desc",
                      },
                      "advancedInfo":{
                         "accountNumber": "amz_account_new_id",
                      }
                   };
            #print body
            resp, body = self.api_client.patchBasicAdvanceInfo(body,id)
            print (resp)

            resp, body = self.api_client.get_AccountById(id)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            actual_accountName= "amz_account_new"
            actual_desc= "amz_account_new_desc"
            actual_accountNumber="amz_account_new_id"

            expected_accountName=data["basicInfo"]["accountName"]
            expected_description=data["basicInfo"]["description"]
            expected_accountNumber=data["advancedInfo"]["accountNumber"]

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and actual_accountName==expected_accountName and actual_desc==expected_description and actual_accountNumber==expected_accountNumber ) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(34)
    def patchAccount_DifferentProvider(self):
        try:
            passed = False
            id = "amz_asset_account123"
            body =  {
                      "basicInfo":{
                            "accountName": id,
                            "serviceProviderType": "vra",
                            "serviceProviderCode": "vra",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                             "description": id
                      },
                      "advancedInfo":{
                         "accountNumber": id
                      }
                   };
            #print body
            resp, body = self.api_client.patchBasicAdvanceInfo(body,id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(35)
    def patchAccount_RemoveFields(self):
        try:
            passed = False
            id = "amz_asset_account123"
            body =  {
                      "basicInfo":{
                            "accountName": "amz_account_new",
                             "description": "TestDesc",
                      },
                      "advancedInfo":{
                         "accountNumber": "123456",
                      }
                   };
            #print body
            resp, body = self.api_client.patchBasicAdvanceInfo(body,id)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(36)
    def deleteAssetAccount(self):
        try:
            passed = False
            id = "amz_asset_account123"
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
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(37)
    def postAccountAzure_WrongCode(self):
        try :
            passed = False
            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": "Test",
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "vra",
                        "serviceProviderType": "azure"
                    },
                    "advancedInfo": {
                        "subscriptionID": subscriptionID,
                        "offerID": offerID,
                        "tenantID": tenantID
                    },
                    "credentials": [

                    ],
                    "accountId": "azure123"
                }
            };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            #print body
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(38)
    def postAccountAzure_WrongType(self):
        try :
            passed = False
            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": "Test",
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "azure",
                        "serviceProviderType": "vra"
                    },
                    "advancedInfo": {
                        "subscriptionID": subscriptionID,
                        "offerID": offerID,
                        "tenantID": tenantID
                    },
                    "credentials": [

                    ],
                    "accountId": "azure123"
                }
            };

            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            #print body
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(39)
    def postAccountAzure_WrongCodeType(self):
        try:
            passed = False
            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": "Test",
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "icd",
                        "serviceProviderType": "vra"
                    },
                    "advancedInfo": {
                        "subscriptionID": subscriptionID,
                        "offerID": offerID,
                        "tenantID": tenantID
                    },
                    "credentials": [

                    ],
                    "accountId": "azure123"
                }
            };
            #print body
            resp, body = self.api_client.create_account(body)
            print (resp)
            #print body
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(40)
    def linkAccount_InvalidProvider(self):
        try :
            passed = False
            id="amz_master"
            vraId="vra1"
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            endPointVersion=utils.decodeCredential(vra_endPointVersion)
            url=utils.decodeCredential(vra_url)
            tenant=utils.decodeCredential(vra_tenant)
            body =  {
                    "account": {
                        "basicInfo": {
                            "accountName": "amz_master",
                            "accountType": "master",
                            "isActive": "Active",
                            "userType": "billing",
                            "serviceProviderCode": "amazon",
                            "serviceProviderType": "amazon"
                        },
                        "advancedInfo": {
                            "accountNumber": "amazon11158",
                            "s3Bucket":s3Bucket
                        },
                        "credentials": [

                        ],
                        "accountId": id
                    }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)
            body = {
                "account": {
                        "basicInfo": {
                            "accountName": "vraAccount123",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "serviceProviderCode": "vra",
                            "serviceProviderType": "vra",
                             "parentAccountId":"amz_master"
                        },
                        "advancedInfo": {
                            "accountNumber": "vraAccount77",
                            "endPointVersion": endPointVersion,
                            "url": url,
                            "tenant": tenant
                        },
                        "credentials": [

                        ],
                        "accountId": vraId
                    }

                }
            resp, body = self.api_client.create_account(body)
            print (resp)
            # Link the Asset Account of another Provider
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(vraId)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(vraId)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(vraId)
            print (resp)
            return False

    # Linking 3 asset account to 1 Master account
    @assignOrder(41)
    def validatePatch_Bulk_Linking1MasterAccount(self):
        try :
            passed = False
            id1="amazon1"
            id2="amazon2"
            id3="amazon3"
            id4="master1"
            s3Bucket=utils.decodeCredential(aws_s3Bucket)

            body = {
                "account":
                    {
                        "basicInfo": {
                            "accountName": "amazon1",
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "description": "automation"
                        },
                        "advancedInfo": {
                            "accountNumber": "123456"
                        },
                        "credentials": [

                        ],
                        "accountId": "amazon1"
                    }
                    };

            resp, body = self.api_client.create_account(body)
            print (resp)
            #second account
            body = {
                "account":
                    {
                        "basicInfo": {
                            "accountName": "amazon2",
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "description": "automation"
                        },
                        "advancedInfo": {
                            "accountNumber": "123456"
                        },
                        "credentials": [

                        ],
                        "accountId": "amazon2"
                    }
                    };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # 3rd asset account
            body = {
                "account":
                    {
                        "basicInfo": {
                            "accountName": "amazon3",
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "description": "automation"
                        },
                        "advancedInfo": {
                            "accountNumber": "123456"
                        },
                        "credentials": [

                        ],
                        "accountId": "amazon3"
                    }
                    };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # create master account

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": "master1",
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": "master1"
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # do a patch for thse 3 accounts
            body = {
                    "subaccounts":[id1,id2,id3]
                    };
            resp, body = self.api_client.patchBulkLining(body,id4)
            print ("PATCH Response is:")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # do a get call for all 3 account and check for parentAccountId
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)
            account1ParentId=data["basicInfo"]["parentAccountId"]
            print ("1st account Parent Id is:")
            print (account1ParentId)

            resp, body = self.api_client.get_AccountById(id2)
            data = json.dumps(body)
            data = json.loads(data)
            account2ParentId=data["basicInfo"]["parentAccountId"]
            print ("2nd account Parent Id is:")
            print (account2ParentId)

            resp, body = self.api_client.get_AccountById(id3)
            data = json.dumps(body)
            data = json.loads(data)
            account3ParentId=data["basicInfo"]["parentAccountId"]
            print ("3rd account Parent Id is:")
            print (account3ParentId)

            if (passOfResponseCode and account1ParentId==account2ParentId and account2ParentId==account3ParentId and account3ParentId==account1ParentId):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id4)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id4)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id2)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id3)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id4)
            print (resp)
            return False

# Create 2 master ,create 2 asset
# Call patch and link asset1 with master 2,asset2 with master 1
# do get call ,asset1 should be linked to master2
# delete all master and asset

    @assignOrder(42)
    def validatePatch_Bulk_Linking_MultipleMasterAccount(self):
        try :
            passed = False
            id1="amazon1"
            id2="amazon2"
            id3="master1"
            id4="master2"
            s3Bucket=utils.decodeCredential(aws_s3Bucket)

            body = {
                "account":
                    {
                        "basicInfo": {
                            "accountName": "amazon1",
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "description": "automation"
                        },
                        "advancedInfo": {
                            "accountNumber": "123456"
                        },
                        "credentials": [

                        ],
                        "accountId": "amazon1"
                    }
                    };

            resp, body = self.api_client.create_account(body)
            print (resp)
            #second account
            body = {
                "account":
                    {
                        "basicInfo": {
                            "accountName": "amazon2",
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "description": "automation"
                        },
                        "advancedInfo": {
                            "accountNumber": "123456"
                        },
                        "credentials": [

                        ],
                        "accountId": "amazon2"
                    }
                    };

            resp, body = self.api_client.create_account(body)
            print (resp)

            ###### create master account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": "master1",
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":"test"
                    },
                    "credentials": [

                    ],
                    "accountId": "master1"
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": "master2",
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": "master2"
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # asset 1 with master2 account link
            body = {
                    "subaccounts":[id1]
                    };
            resp, body = self.api_client.patchBulkLining(body,id4)
            print ("PATCH Response is:")
            print (resp)
            logger.info("API response:" + str(resp))

            # asset 2 with master1 account link
            body = {
                    "subaccounts":[id2]
                    };
            resp, body = self.api_client.patchBulkLining(body,id3)
            print ("PATCH Response is:")
            print (resp)
            logger.info("API response:" + str(resp))

            # do a get call for all 3 account and check for parentAccountId
            resp, body = self.api_client.get_AccountById(id1)
            data = json.dumps(body)
            data = json.loads(data)
            account1ParentId=data["basicInfo"]["parentAccountId"]
            print ("1st account Parent Id is:")
            print (account1ParentId)

            resp, body = self.api_client.get_AccountById(id2)
            data = json.dumps(body)
            data = json.loads(data)
            account2ParentId=data["basicInfo"]["parentAccountId"]
            print ("2nd account Parent Id is:")
            print (account2ParentId)

            if (account1ParentId==id4 and account2ParentId==id3):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id4)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id4)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id2)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id3)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id4)
            print (resp)
            return False

        # Create amazon master, create 2 asset amazon,vra
        # Do a PATCH call
        # Patch should fail -404

    @assignOrder(43)
    def validatePatch_Bulk_Linking_MultipleInvalidProviders(self):
        try :
            passed = False
            id1="amazon1"
            id2="azure1"
            id3="master1"

            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)

            body = {
                "account":
                    {
                        "basicInfo": {
                            "accountName": "amazon1",
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "description": "automation"
                        },
                        "advancedInfo": {
                            "accountNumber": "123456"
                        },
                        "credentials": [

                        ],
                        "accountId": "amazon1"
                    }
                    };

            resp, body = self.api_client.create_account(body)
            print (resp)
            #second account
            body = {
                   "account":{
                      "basicInfo":{
                         "accountName":"azure1",
                         "serviceProviderType":"azure",
                         "isActive":"Active",
                         "accountType":"subaccount",
                         "userType":"asset" ,
                         "serviceProviderCode":"azure"
                      },
                      "advancedInfo":{
                         "subscriptionID":subscriptionID,
                         "offerID":offerID,
                         "tenantID":tenantID
                      },
                      "credentials":[

                      ],
                      "accountId": "azure1"
                   }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # create master account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": "master1",
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": "master1"
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # linking diffrent provider asset account with master account
            body = {
                    "subaccounts":[id1,id2]
                    };
            resp, body = self.api_client.patchBulkLining(body,id3)
            print ("PATCH Response is:")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)

            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id2)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id3)
            print (resp)
            return False


        # Create 2 master account
        # Link master account 1 to master account 2
        # Link master account to Master account
        # Patch should fail -404
    @assignOrder(44)
    def validatePatch_Link_MastertoMaster(self):
        try :
            passed = False
            id1="master1"
            id2="master2"
            s3Bucket=utils.decodeCredential(aws_s3Bucket)

            # create first  account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": id1,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": id1
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)


            # create 2nd master accountType

            body = {
                "account": {
                    "basicInfo": {
                        "accountName": id2,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId":  id2,
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # linking diffrent provider asset account with master account
            body = {
                    "subaccounts":[id1]
                    };
            resp, body = self.api_client.patchBulkLining(body,id2)
            print ("PATCH Response is:")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)

            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id2)
            print (resp)
            return False


    # create a master account and pass wrong account id
    @assignOrder(45)
    def validatePatch_WrongAccountID(self):
        try :
            passed = False
            id1="master1"
            id2="12345678"
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            # create first master  account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": id1,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": id1
                }
            };
            resp, body = self.api_client.create_account(body)
            print (resp)
            # linking diffrent provider asset account with master account
            body = {
                    "subaccounts":[id2]
                    };
            resp, body = self.api_client.patchBulkLining(body,id1)
            print ("PATCH Response is:")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return False

    # enter wrong master account id and try to patch
    @assignOrder(46)
    def validatePatch_WrongMasterAccountID(self):
        try :
            passed = False
            id1="master1abcd"
            id2="azure1"
            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)

            body = {
                   "account":{
                      "basicInfo":{
                         "accountName":id2,
                         "serviceProviderType":"azure",
                         "isActive":"Active",
                         "accountType":"subaccount",
                         "userType":"asset" ,
                         "serviceProviderCode":"azure"
                      },
                      "advancedInfo":{
                         "subscriptionID":subscriptionID,
                         "offerID":offerID,
                         "tenantID":tenantID
                      },
                      "credentials":[

                      ],
                      "accountId": id2
                   }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)
            body = {
                    "subaccounts":[id2]
                    };
            resp, body = self.api_client.patchBulkLining(body,id1)
            print ("PATCH Response is:")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id2)
            print (resp)
            return False

    # Create a Master account
    # Create asset account link to it
    # Create one more master account
    # Do patch and link it with Master 2
    # GET Call
    # Account should be linked to Master2

    @assignOrder(47)
    def validatePatch_DLinking_ParentMasterAccount(self):
        try :
            passed = False
            id1="master1"
            id2="master2"
            id3="amazon1"
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            # create 1st master account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": id1,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": id1
                }
            };
            resp, body = self.api_client.create_account(body)
            print (resp)

            # create 2nd master account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": id2,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": id2
                }
            };
            resp, body = self.api_client.create_account(body)
            print (resp)


            # create one assset account
            body = {
                "account":
                    {
                        "basicInfo": {
                            "accountName": id3,
                            "serviceProviderType": "amazon",
                            "serviceProviderCode": "amazon",
                            "accountType": "subaccount",
                            "isActive": "Active",
                            "userType": "asset",
                            "description": "automation",
                             "parentAccountId":id1
                        },
                        "advancedInfo": {
                            "accountNumber": "123456"
                        },
                        "credentials": [

                        ],
                        "accountId": id3
                    }
                    };

            resp, body = self.api_client.create_account(body)
            print (resp)


            # do a patch for thse 3 accounts
            body = {
                    "subaccounts":[id3]
                    };
            resp, body = self.api_client.patchBulkLining(body,id2)
            print ("PATCH Response is:")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # do a get call for all 3 account and check for parentAccountId
            resp, body = self.api_client.get_AccountById(id3)
            data = json.dumps(body)
            data = json.loads(data)
            account1ParentId=data["basicInfo"]["parentAccountId"]
            print ("1st account Parent Id is:")
            print (account1ParentId)


            if (passOfResponseCode and account1ParentId==id2):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id2)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id3)
            print (resp)
            return False

    # delete 1 proper,1 wrong account
    @assignOrder(48)
    def bulkdelete_InvalidAccount(self):
        try :
            passed = False
            id1="amazon1"
            id2="amazon2"

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

            body = {
                    "accounts":[id1,id2]
                    };
            resp, body = self.api_client.postBulkDelete(body)
            print (resp)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return False

    # Create 2 asset 1-amazon,1-azure and delete by bulk
    # After delete do get by id 404
    @assignOrder(49)
    def bulkdelete_MultipleAccounts(self):
        try :
            passed = False
            id1="amazon1"
            id2="azure1"

            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)

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

            body = {
                   "account":{
                      "basicInfo":{
                         "accountName":id2,
                         "serviceProviderType":"azure",
                         "isActive":"Active",
                         "accountType":"subaccount",
                         "userType":"asset" ,
                         "serviceProviderCode":"azure"
                      },
                      "advancedInfo":{
                         "subscriptionID":subscriptionID,
                         "offerID":offerID,
                         "tenantID":tenantID
                      },
                      "credentials":[

                      ] ,
                       "accountId": id2
                   }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)

            body = {
                    "accounts":[id1,id2]
                    };
            resp, body = self.api_client.postBulkDelete(body)
            print (resp)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # do a get call for account1
            resp, body = self.api_client.get_AccountById(id1)
            print ("Response for account1 is:")
            print (resp)
            resp1=resp

            # do a get call for account2
            resp, body = self.api_client.get_AccountById(id2)
            print ("Response for account2 is:")
            print (resp)
            resp2=resp

            if (passOfResponseCode and resp1==resp2):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return False

    # create 1 master ,2 asset and link to master
    # delete asset and check whether master still has the link to account
    # link=true 404
    @assignOrder(50)
    def bulkdelete_VerifyMasterLink(self):
        try :
            passed = False
            id1="amazon1"
            id2="amazon2"
            id3="master1"
            s3Bucket=utils.decodeCredential(aws_s3Bucket)

            # create a master account and asset that id to asset account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": id3,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": id3
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)

            body = {
               "account":
                {
                    "basicInfo": {
                        "accountName": id1,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset",
                         "parentAccountId":id3
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

            body = {
               "account":
                {
                    "basicInfo": {
                        "accountName": id2,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset",
                         "parentAccountId":id3
                    },
                    "advancedInfo": {
                        "accountNumber": "123456"
                    },
                    "credentials": [

                    ],
                    "accountId": id2
                }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # delete the first account

            body = {
                    "accounts":[id1]
                    };
            resp, body = self.api_client.postBulkDelete(body)
            print (resp)

            # do a get call for master and check whether account2 is present or not
            resp, body = self.api_client.getAccount_Link(id3,"true")
            print (resp)

            data = json.dumps(body)
            data = json.loads(data)
            accountName=data[1]["basicInfo"]["accountName"]
            print ("account name is:")
            print (accountName)
            parentID=data[1]["basicInfo"]["parentAccountId"]
            print ("Parent ID is:")
            print (parentID)
            accountID=data[1]["accountId"]
            print ("account id is:")
            print (accountID)
            total=data[0]["total_rows"]
            print ("total Record count is:")
            print (total)

            if (total==1 and accountName==id2 and parentID==id3 and accountID==id2):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id2)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id3)
            print (resp)
            return False

    # create 1 master ,2 asset and link to master
    # Delete master and check whether parentid is still present in asset account
    @assignOrder(51)
    def bulkdelete_VerifyAssetLink(self):
        try :
            passed = False
            id1="amazon1"
            id2="amazon2"
            id3="master1"

            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)

            # create a master account and asset that id to asset account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": id3,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": id3
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)

            body = {
               "account":
                {
                    "basicInfo": {
                        "accountName": id1,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset",
                         "parentAccountId":id3
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

            body = {
                   "account":{
                      "basicInfo":{
                         "accountName":id2,
                         "serviceProviderType":"azure",
                         "isActive":"Active",
                         "accountType":"subaccount",
                         "userType":"asset" ,
                         "serviceProviderCode":"azure",
                         "parentAccountId":id3
                      },
                      "advancedInfo":{
                         "subscriptionID":subscriptionID,
                         "offerID":offerID,
                         "tenantID":tenantID
                      },
                      "credentials":[

                      ] ,
                       "accountId": id2
                   }
                };

            resp, body = self.api_client.create_account(body)
            print (resp)

            # delete the first account

            body = {
                    "accounts":[id3]
                    };
            resp, body = self.api_client.postBulkDelete(body)
            print (resp)

            # do a get call for account and check whether account1,2 have parent account link or not
            resp, body = self.api_client.get_AccountById(id1)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            try :
                parentID=data["basicInfo"]["parentAccountId"]
                print (parentID)
            except:
                print ("Parent id for Account1 is:")
                parentID1="NA"
                print (parentID1)

            resp, body = self.api_client.get_AccountById(id2)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            try :
                parentID=data["basicInfo"]["parentAccountId"]
                print (parentID)
            except:
                print ("Parent id for Account2 is:")
                parentID2="NA"
                print (parentID2)

            if (parentID1==parentID2):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id2)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id2)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id3)
            print (resp)
            return False


    # delinking the single sub account
    @assignOrder(52)
    def dlinkSingleValidAccount(self):
        try :
            passed = False
            id1="amazon1"
            id3="master1"
            s3Bucket=utils.decodeCredential(aws_s3Bucket)

            # create a master account and asset that id to asset account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": id3,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": id3
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)

            body = {
               "account":
                {
                    "basicInfo": {
                        "accountName": id1,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset",
                         "parentAccountId":id3
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

            # dlink the single account
            resp, body = self.api_client.dlinkSingleAccount(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # do a get call for account and check whether account1,2 have parent account link or not
            resp, body = self.api_client.get_AccountById(id1)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            try :
                parentID=data["basicInfo"]["parentAccountId"]
                print (parentID)
            except:
                print ("Parent id for Account1 is:")
                parentID1="NA"
                print (parentID1)

            if (parentID1=='NA' and passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id3)
            print (resp)
            return False

    @assignOrder(53)
    def dlinkSingleInValidAccount(self):
        try :
            passed = False
            id1="amazon1"
            id3="master1"
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            # create a master account and asset that id to asset account
            body = {
                "account": {
                    "basicInfo": {
                        "accountName": id3,
                        "accountType": "master",
                        "isActive": "Active",
                        "userType": "billing",
                        "serviceProviderCode": "amazon",
                        "serviceProviderType": "amazon"
                    },
                    "advancedInfo": {
                        "accountNumber": "123456",
                        "s3Bucket":s3Bucket
                    },
                    "credentials": [

                    ],
                    "accountId": id3
                }
            };

            resp, body = self.api_client.create_account(body)
            print (resp)

            body = {
               "account":
                {
                    "basicInfo": {
                        "accountName": id1,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset",
                         "parentAccountId":id3
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

            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)

            # dlink the single account
            resp, body = self.api_client.dlinkSingleAccount(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)

            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteAccountV2(id3)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            resp, body = self.api_client.deleteAccountV2(id3)
            print (resp)
            return False

    @assignOrder(54)
    def postValidCredential(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

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
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # get accountby id
            resp, body = self.api_client.get_AccountById(id1)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_Name=data['credentials'][0]['credentialName']
            print (cred_Name)
            print ("credential Id is:")
            cred_id=data['credentials'][0]['id']
            print (cred_id)
            print ("Team is:")
            team_name=data['credentials'][0]['context'][0]['team'][0]
            print (team_name)

            if(passOfResponseCode and cred_Name==credname and cred_id==credid and team==team_name) :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return

    @assignOrder(55)
    def postCredential_InValidContext(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

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
                                        "CORE-Xyz"
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)

            if(passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return passed

    @assignOrder(56)
    def postDuplicateCredential(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

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
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)


            body = {
					"credentials":
                        {
                            "credentialName": credname,
                            "id":credid,
                            "status": "Active",
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
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 409)
            if(passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return

    @assignOrder(56)
    def postDuplicateCredential_Name(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)


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
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)


            body = {
					"credentials":
                        {
                            "credentialName": credname,
                            "id":"credid123",
                            "status": "Active",
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
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 409)
            if(passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return

    @assignOrder(57)
    def postDuplicateCredential_id(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

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
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)


            body = {
					"credentials":
                        {
                            "credentialName": "credtest",
                            "id":credid,
                            "status": "Active",
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
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 409)
            if(passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return

    @assignOrder(58)
    def postCredential_wrongAccountId(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

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
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,"12345678")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if(passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return

    @assignOrder(59)
    def postCredential_generateCredId(self):
        try :
            passed = False
            id1="amazon1"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

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
                                        team
                                    ]
                                }
                            ]
                        }
    				};

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # get accountby id
            resp, body = self.api_client.get_AccountById(id1)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_Name=data['credentials'][0]['credentialName']
            print (cred_Name)
            print ("credential Id is:")
            cred_id=data['credentials'][0]['id']
            print (cred_id)
            print ("Team is:")
            team_name=data['credentials'][0]['context'][0]['team'][0]
            print (team_name)
            print ("contextId is:")
            contextId=data['credentials'][0]['context'][0]['contextId']
            print (contextId)

            if(passOfResponseCode and cred_Name==credname and cred_id !="" and (cred_id is not None) and team==team_name and (contextId is not None) and contextId!="") :
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            return

    @assignOrder(72)
    def postcredential_CrefsId(self):
            global crefId2
            try:
                passed = False
                accessKey=utils.decodeCredential(amazon_accessKey)
                secretKey=utils.decodeCredential(amazon_secretKey)

                resp, body = self.api_client.get_VaultConfiguration()
                print (resp)
                logger.info("API response:" + str(resp))
                data = json.dumps(body)
                data = json.loads(data)
                print (data[0]['vault_id'])
                vaultId = data[0]['vault_id']
                crefId2 = "automationTesting"
                randID = 'abc-123-092'
                print (randID)
                crefId2 = crefId2 + randID
                body = {
                    "crefId": crefId2,
                    "credential": {
                        "secretKey": secretKey,
                        "accesskey": accessKey
                    },
                    "vaultId": vaultId
                };

                resp, body = self.api_client.postCredRefCredential(body)
                print (resp)
                passOfResponseCode = assertEqual(resp, 200)
                if (passOfResponseCode):
                    passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    status['CAM-APITest'] = False
                    return passed
            except:
                status['CAM-APITest'] = False
                return

    @assignOrder(73)
    def deleteCredential_CrefsId(self):
        try:
            passed = False
            # do a delete call
            resp, body = self.api_client.deleteCredRefCredential(crefId2,headersUser1)
            print (resp)

            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteCredRefCredential(crefId2,headersUser1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteCredRefCredential(crefId2,headersUser1)
            print (resp)
            return

    @assignOrder(74)
    def getCredential_CrefsId(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            crefId = "automationTesting-123-064542282"
            resp, body = self.api_client.get_VaultConfiguration()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['vault_id'])
            vaultId = data[0]['vault_id']
            print ("credential Id is:")
            print (crefId)
            body = {
                "crefId": crefId,
                "credential": {
                    "secretKey": secretKey,
                    "accesskey": accessKey
                },
                "vaultId": vaultId
            };

            resp, body = self.api_client.postCredRefCredential(body)
            print (resp)
            # do a get call
            resp, body = self.api_client.getCredRefCredentialById(crefId,headersUser1)
            print (resp)
            passOfResponseCode = assertEqual(resp, 200)

            data = json.dumps(body)
            data = json.loads(data)
            access_Key = data ['accesskey']
            secret_Key = data ['secretKey']

            if (passOfResponseCode and access_Key == accessKey and secret_Key == secretKey):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
            print (resp)
            return

    @assignOrder(75)
    def postCredential_EmptyVaultId(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)


            crefId = "automationTesting-123-0645422822"
            vaultId = ""
            body = {
                "crefId": crefId,
                "credential": {
                    "secretKey": secretKey,
                    "accesskey": accessKey
                },
                "vaultId": vaultId
            };

            resp, body = self.api_client.postCredRefCredential(body)
            print (resp)
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
            print (resp)
            return

    @assignOrder(76)
    def postCredential_EmptyCredential(self):
        try:
            passed = False
            crefId = "automationTesting-123-0645422822"
            resp, body = self.api_client.get_VaultConfiguration()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['vault_id'])
            vaultId = data[0]['vault_id']
            print ("credential Id is:")
            print (crefId)
            body = {
                "crefId": crefId,
                "credential": {

                },
                "vaultId": vaultId
            };

            resp, body = self.api_client.postCredRefCredential(body)
            print (resp)
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
            print (resp)
            return

    @assignOrder(77)
    def postCredential_WithoutCredentialandVaultId(self):
        try:
            passed = False
            crefId = "automationTesting-123-0645422822"
            print ("credential Id is:")
            print (crefId)
            body = {
                "crefId": crefId
            };

            resp, body = self.api_client.postCredRefCredential(body)
            print (resp)
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(78)
    def postCredential_WithoutCredential(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            body = {
                "credential": {
                    "secretKey": secretKey,
                    "accesskey": accessKey
                }
            };

            resp, body = self.api_client.postCredRefCredential(body)
            print (resp)
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(79)
    def postCredential_RefID_SpecialCharacter(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            resp, body = self.api_client.get_VaultConfiguration()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['vault_id'])
            vaultId = data[0]['vault_id']
            crefId = "automationTesting-123-0677454-!*()%$##@@!(**"
            print ("credential Id is:")
            print (crefId)
            body = {
                "crefId": crefId,
                "credential": {
                    "secretKey": secretKey,
                    "accesskey": accessKey
                },
                "vaultId": vaultId
            };

            resp, body = self.api_client.postCredRefCredential(body)
            print (resp)
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(80)
    def putCredential_RefID(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            resp, body = self.api_client.get_VaultConfiguration()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['vault_id'])
            vaultId = data[0]['vault_id']
            crefId = "automationTesting-123-0677454"
            print ("credential Id is:")
            print (crefId)
            body = {
                "crefId": crefId,
                "credential": {
                    "secretKey": secretKey,
                    "accesskey": accessKey
                },
                "vaultId": vaultId
            };
            resp, body = self.api_client.postCredRefCredential(body)
            print (resp)

            # put certificate
            updated_accesskey = "1000"
            updated_secretKey = "2000"
            body = {
                "credential": {
                    "secretKey": updated_secretKey,
                    "accesskey": updated_accesskey
                }
            };

            resp, body = self.api_client.putCredentialRefsById(body,crefId,headersUser1)
            print (resp)
            passOfResponseCode = assertEqual(resp, 200)
            # do a get call
            resp, body = self.api_client.getCredRefCredentialById(crefId,headersUser1)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            access_Key = data ['accesskey']
            secret_Key = data ['secretKey']

            if (passOfResponseCode and access_Key == updated_accesskey and secret_Key == updated_secretKey):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
            print (resp)
            return

    @assignOrder(81)
    def putCredential_EmptyCredential(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            resp, body = self.api_client.get_VaultConfiguration()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['vault_id'])
            vaultId = data[0]['vault_id']
            crefId = "automationTesting-123-0677454"
            print ("credential Id is:")
            print (crefId)
            body = {
                "crefId": crefId,
                "credential": {
                    "secretKey": secretKey,
                    "accesskey": accessKey
                },
                "vaultId": vaultId
            };

            resp, body = self.api_client.postCredRefCredential(body)
            print (resp)

            # put certificate
            body = {
                "credential": {

                }
            };

            resp, body = self.api_client.putCredentialRefsById(body, crefId,headersUser1)
            print (resp)
            passOfResponseCode = assertEqual(resp, 200)
            # do a get call

            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
                print (resp)
                return passed
            else:
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
                print (resp)
                return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteCredRefCredential(crefId,headersUser1)
            print (resp)
            return

    @assignOrder(82)
    def createCredential_WithValue(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            print (crefId)
            body = {
                    "crefId":crefId,
                    "credential":
                        {
                         "value":{
                                    "accessKey": accessKey,
                                    "secretKey": secretKey
                                }
                        }
                    };

            resp, body = self.api_client.postCredRefCredential(body)
            print (resp)
            logger.info("API response:" + str(resp))
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(83)
    def postCredential_ValidCredRef_ValidPassword(self):
        try :
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            accountId="f16b0f4a-a76e-499e-aws-testautomationAmazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            print ("Credential Ref Id is:")
            print (crefId)
            body = {
                   "account":{
                      "basicInfo":{
                        "accountName": randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": accountId
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
                            "crefId": crefId,
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
                                        team
                                    ]
                                }
                            ]
                        }
                    };

            resp, body = self.api_client.postCredentials(body,accountId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            # do a get call for account and check whether the secretKey and accessKey are same
            # do a get call from system userId
            # print headersUser1
            resp, body = self.api_client.get_credentials_manage(accountId, credid, "false", headersUser1)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            print ("credential Id is:")
            cred_id = data['credentials'][0]['id']
            print (cred_id)

            print ("credential name is:")
            cred_name = data['credentials'][0]['credentialName']
            print (cred_name)

            print ("Credential Access key is:")
            cred_accesskey = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId = data['credentials'][0]['crefId']
            print (cred_credfId)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            if(passOfResponseCode and cred_name==credname and cred_id==credid and cred_accesskey==accessKey and cred_secretKey==secretKey and cred_credfId==crefId):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return passed
            else :
                status['CoreX-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            return False

    @assignOrder(84)
    def postCredential_ValidCredRef_InValidPassword(self):
        try :
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            accountId="f16b0f4a-a76e-499e-aws-testautomationAmazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            accessKey=utils.decodeCredential(amazon_accessKey)+utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)+utils.decodeCredential(amazon_secretKey)

            print ("Credential Ref Id is:")
            print (crefId)
            body = {
                   "account":{
                      "basicInfo":{
                        "accountName": randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": accountId
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
                            "crefId": crefId,
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
                                        team
                                    ]
                                }
                            ]
                        }
                    };

            resp, body = self.api_client.postCredentials(body,accountId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            # do a get call for account and check whether the secretKey and accessKey are same
            # do a get call from system userId
            # print headersUser1
            resp, body = self.api_client.get_credentials_manage(accountId, credid, "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)

            if(passOfResponseCode and cred_name==credname and cred_id==credid and cred_accesskey==accessKey and cred_secretKey==secretKey and cred_credfId==crefId):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return passed
            else :
                status['CoreX-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            return False

    @assignOrder(85)
    def postCredential_ValidCredRef(self):
        try :
            passed = False
            crefId ="amazon-cref-001"
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            accountId="f16b0f4a-a76e-499e-aws-testautomationAmazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)
            print ("Credential Ref Id is:")
            print (crefId)
            body = {
                   "account":{
                      "basicInfo":{
                        "accountName": randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": accountId
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
                            "crefId": crefId,
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

            resp, body = self.api_client.postCredentials(body,accountId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            # do a get call for account and check whether the secretKey and accessKey are same
            # do a get call from system userId
            # print headersUser1
            resp, body = self.api_client.get_credentials_manage(accountId, credid, "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)

            if(passOfResponseCode and cred_name==credname and cred_id==credid and cred_accesskey==accessKey and cred_secretKey==secretKey and cred_credfId==crefId):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return passed
            else :
                status['CoreX-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            return False

    @assignOrder(86)
    def postCredential_ValidPasswordField(self):
        try :
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            accountId="f16b0f4a-a76e-499e-aws-testautomationAmazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)
            print ("Credential Ref Id is:")
            print (crefId)
            body = {
                   "account":{
                      "basicInfo":{
                        "accountName": randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": accountId
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
                            "passwordFields": {
                                "accessKey": accessKey,
                                "secretKey": secretKey
                                },
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

            resp, body = self.api_client.postCredentials(body,accountId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            # do a get call for account and check whether the secretKey and accessKey are same
            # do a get call from system userId
            # print headersUser1
            resp, body = self.api_client.get_credentials_manage(accountId, credid, "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)

            if(passOfResponseCode and cred_name==credname and cred_id==credid and cred_accesskey==accessKey and cred_secretKey==secretKey and cred_credfId !=crefId):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return passed
            else :
                status['CoreX-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            return False

    @assignOrder(87)
    def postCredential_InValidCrefId(self):
        try :
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            accountId="f16b0f4a-a76e-499e-aws-testautomationAmazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"

            body = {
                   "account":{
                      "basicInfo":{
                        "accountName": randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": accountId
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
                            "crefId":"333333333-767-767-887873",
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

            resp, body = self.api_client.postCredentials(body,accountId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)

            if(passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return passed
            else :
                status['CoreX-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            return False

    @assignOrder(88)
    def postCredential_InValidPassword(self):
        try :
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            accountId="f16b0f4a-a76e-499e-aws-testautomationAmazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            accessKey=utils.decodeCredential(amazon_accessKey)+utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)+utils.decodeCredential(amazon_secretKey)
            print ("Credential Ref Id is:")
            print (crefId)
            body = {
                   "account":{
                      "basicInfo":{
                        "accountName": randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": accountId
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
                                        team
                                    ]
                                }
                            ]
                        }
                    };

            resp, body = self.api_client.postCredentials(body,accountId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            # do a get call for account and check whether the secretKey and accessKey are same
            # do a get call from system userId
            # print headersUser1
            resp, body = self.api_client.get_credentials_manage(accountId, credid, "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)

            if(passOfResponseCode and cred_name==credname and cred_id==credid and cred_accesskey==accessKey and cred_secretKey==secretKey and cred_credfId !=crefId):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return passed
            else :
                status['CoreX-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            return False

    @assignOrder(89)
    def postCredential_InvalidCrefId_InvalidPassword(self):
        try :
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            accountId="f16b0f4a-a76e-499e-aws-testautomationAmazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            accessKey=utils.decodeCredential(amazon_accessKey)+utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)
            print ("Credential Ref Id is:")
            crefId="1002003004000"
            print (crefId)
            body = {
                   "account":{
                      "basicInfo":{
                        "accountName": randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": accountId
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
                            "crefId":crefId,
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
                                        team
                                    ]
                                }
                            ]
                        }
                    };

            resp, body = self.api_client.postCredentials(body,accountId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            # do a get call for account and check whether the secretKey and accessKey are same
            # do a get call from system userId
            # print headersUser1
            resp, body = self.api_client.get_credentials_manage(accountId, credid, "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)

            if(passOfResponseCode and cred_name==credname and cred_id==credid and cred_accesskey==accessKey and cred_secretKey==secretKey and cred_credfId ==crefId):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId,headersUser1)
                print (resp)
                return passed
            else :
                status['CoreX-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId,headersUser1)
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            resp, body = self.api_client.deleteCertificateRefsById(crefId,headersUser1)
            print (resp)
            return False

    @assignOrder(90)
    def postCredential_InvalidCrefId_validPassword(self):
        try :
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            accountId="f16b0f4a-a76e-499e-aws-testautomationAmazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)
            print ("Credential Ref Id is:")
            crefId="1002003004000"
            print (crefId)
            body = {
                   "account":{
                      "basicInfo":{
                        "accountName": randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": accountId
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
                            "crefId":crefId,
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
                                        team
                                    ]
                                }
                            ]
                        }
                    };

            resp, body = self.api_client.postCredentials(body,accountId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            # do a get call for account and check whether the secretKey and accessKey are same
            # do a get call from system userId
            # print headersUser1
            resp, body = self.api_client.get_credentials_manage(accountId, credid, "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)

            if(passOfResponseCode and cred_name==credname and cred_id==credid and cred_accesskey==accessKey and cred_secretKey==secretKey and cred_credfId ==crefId):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId,headersUser1)
                print (resp)
                return passed
            else :
                status['CoreX-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId,headersUser1)
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            resp, body = self.api_client.deleteCertificateRefsById(crefId,headersUser1)
            print (resp)
            return False

    @assignOrder(91)
    def postCredential_withoutCrefId_withoutPasswordFields_(self):
        try :
            passed = False
            randID = 'TestAWSAcMinimal'
            randID += str(x)
            print (randID)
            accountId="f16b0f4a-a76e-499e-aws-testautomationAmazon"
            credid="12345"
            credname="amzcred"
            team="CORE-X"
            body = {
                   "account":{
                      "basicInfo":{
                        "accountName": randID,
                        "serviceProviderType": "amazon",
                        "serviceProviderCode": "amazon",
                        "accountType": "subaccount",
                        "isActive": "Active",
                        "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"3245235249"
                      },
                      "credentials":[

                      ],
                    "accountId": accountId
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

            resp, body = self.api_client.postCredentials(body,accountId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)

            if(passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return passed
            else :
                status['CoreX-APITest'] = False
                resp, body = self.api_client.deleteAccountV2(accountId)
                print (resp)
                return False
        except:
            status['CoreX-APITest'] = False
            resp, body = self.api_client.deleteAccountV2(accountId)
            print (resp)
            return False

    @assignOrder(92)
    def verifyPut_CredRefId(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            crefId="cred1"
            id1 = "f16b0f4a-test-automation-0925"
            access_Key="100100"
            secret_Key="200200"
            credupdatedName="cred_Updated_123"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            body = {"account":
                    {
                        "accountId": id1,
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
                                "credentialName": "cred1",
                                "crefId": crefId,
                                "id":crefId,
                                "passwordFields": {
                                    "secretKey": accessKey,
                                    "accessKey": secretKey
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

            # do a PUT account call
            body = {"account":
                    {
                        "accountId":id1,
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
                                "credentialName": credupdatedName,
                                "crefId": crefId,
                                "id":crefId,
                                "passwordFields": {
                                    "secretKey": secret_Key,
                                    "accessKey": access_Key
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

            resp, body = self.api_client.update_account(body, id1)
            print (resp)

            # do a get call and get the password fields
            resp, body = self.api_client.get_credentials_manage(id1, crefId, "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and cred_credfId==crefId and access_Key==cred_accesskey and secret_Key==cred_secretKey and credupdatedName==cred_name):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                status['CAM-APITest'] = False
                return False
        except:
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            status['CAM-APITest'] = False
            return False

    @assignOrder(93)
    def verifyPut_ChangeCredRefId(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            crefId="cred1"
            crefId_Updated="cred2"
            id1 = "f16b0f4a-test-automation-0925"
            access_Key="100100"
            secret_Key="200200"
            credupdatedName="cred_Updated_123"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            body = {"account":
                    {
                        "accountId": id1,
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
                                "credentialName": "cred1",
                                "crefId": crefId,
                                "id":crefId,
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

            # do a PUT account call
            body = {"account":
                    {
                        "accountId":id1,
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
                                "credentialName": credupdatedName,
                                "crefId": crefId_Updated,
                                "id":crefId,
                                "passwordFields": {
                                    "secretKey": secret_Key,
                                    "accessKey": access_Key
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

            resp, body = self.api_client.update_account(body, id1)
            print (resp)

            # do a get call and get the password fields
            resp, body = self.api_client.get_credentials_manage(id1, crefId, "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and crefId_Updated==cred_credfId and access_Key==cred_accesskey and secret_Key==cred_secretKey and credupdatedName==cred_name):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                status['CAM-APITest'] = False
                return False
        except:
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            status['CAM-APITest'] = False
            return False

    @assignOrder(94)
    def verifyPut_newGenegratedCredRefId(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            crefId="cred1"
            crefId_Updated="cred2"
            id1 = "f16b0f4a-test-automation-0925"
            access_Key="100100"
            secret_Key="200200"
            credupdatedName="cred_Updated_123"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)


            body = {"account":
                    {
                        "accountId": id1,
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
                                "credentialName": "cred1",
                                "crefId": crefId,
                                "id":crefId,
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

            # do a PUT account call
            body = {"account":
                    {
                        "accountId":id1,
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
                                "credentialName": credupdatedName,
                                "id":crefId,
                                "passwordFields": {
                                    "secretKey": secret_Key,
                                    "accessKey": access_Key
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

            resp, body = self.api_client.update_account(body, id1)
            print (resp)

            # do a get call and get the password fields
            resp, body = self.api_client.get_credentials_manage(id1, crefId, "false", headersUser1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)

            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode and crefId!=cred_credfId and access_Key==cred_accesskey and secret_Key==cred_secretKey and credupdatedName==cred_name):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                status['CAM-APITest'] = False
                return False
        except:
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            status['CAM-APITest'] = False
            return False

    @assignOrder(95)
    def verifyPut_CertificateRefId(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            crefId="cred1"
            # crefId_Updated="cred2"
            id1 = "f16b0f4a-test-automation-0925"
            credupdatedName="cred_Updated_123"
            access_Key="100-100"
            secret_Key="200-200"

            # create a credRef
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            crefId_Certificate="automationTestingCoreX"

            body = {
                "crefId": crefId_Certificate,
                "credential":
                {
                 "value":{
                        "secretKey":secretKey,
                        "accessKey":accessKey
                        }
                    }
                };

            print (body)
            resp, body = self.api_client.postCredentialRefs(body)

            body = {"account":
                    {
                        "accountId": id1,
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
                                "credentialName": "cred1",
                                "crefId": crefId,
                                "id":crefId,
                                "passwordFields": {
                                    "secretKey": secret_Key,
                                    "accessKey": access_Key
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

            # do a PUT account call
            body = {"account":
                    {
                        "accountId":id1,
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
                                "credentialName": credupdatedName,
                                "id":crefId,
                                "crefId": crefId_Certificate,
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

            resp, body = self.api_client.update_account(body, id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)

            # do a get call and get the password fields
            resp, body = self.api_client.get_credentials_manage(id1, crefId, "false", headersUser1)
            print (resp)
            # logger.info("API response:" + str(resp))
            # passOfResponseCode = assertEqual(resp, 200)
            data = json.dumps(body)
            data = json.loads(data)
            print ("credential name is:")
            cred_name  = data['credentials'][0]['credentialName']
            print (cred_name)
            print ("credential Id is:")
            cred_id  = data['credentials'][0]['id']
            print (cred_id)
            print ("Credential Access key is:")
            cred_accesskey  = data['credentials'][0]['passwordFields']['accessKey']
            print (cred_accesskey)
            print ("Credential secret key is:")
            cred_secretKey  = data['credentials'][0]['passwordFields']['secretKey']
            print (cred_secretKey)
            print ("CredRef id is:")
            cred_credfId  = data['credentials'][0]['crefId']
            print (cred_credfId)


            if (passOfResponseCode and crefId_Certificate==cred_credfId and accessKey==cred_accesskey and secretKey==cred_secretKey and credupdatedName==cred_name):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId_Certificate,headersUser1)
                print (resp)
                return passed
            else :
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId_Certificate,headersUser1)
                print (resp)
                status['CAM-APITest'] = False
                return False
        except:
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId_Certificate,headersUser1)
                print (resp)
                status['CAM-APITest'] = False
                return False

    @assignOrder(96)
    def verifyPostAccount_WithoutContext(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            crefId="cred1"
            # crefId_Updated="cred2"
            id1 = "f16b0f4a-test-automation-0925"

            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            body = {"account":
                    {
                        "accountId": id1,
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
                                "credentialName": crefId,
                                "crefId": crefId,
                                "id":crefId,
                                "passwordFields": {
                                    "secretKey": secretKey,
                                    "accessKey": accessKey
                                },
                                "purpose": [
                                    "provisioning"
                                ],
                                "context": [
                                    {

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
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                status['CAM-APITest'] = False
                return False
        except:
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            status['CAM-APITest'] = False
            return False

    @assignOrder(97)
    def verifyCredential_WithoutContext(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            crefId="cred1"
            # crefId_Updated="cred2"
            id1 = "f16b0f4a-test-automation-0925"
            body =  {
                   "account":{
                      "basicInfo":{
                         "accountName": "amazon"+randID,
                         "serviceProviderType": "amazon",
                         "serviceProviderCode": "amazon",
                         "accountType": "subaccount",
                         "isActive": "Active",
                         "userType": "asset"
                      },
                      "advancedInfo":{
                         "accountNumber":"100100"
                      },
                      "credentials":[

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
                            "credentialName": crefId,
                            "crefId": crefId,
                            "id":crefId,
                            "status": "Active",
                            "purpose": [
                                "provisioning"
                            ],
                            "context": [
                                {

                                }
                            ]
                        }
                    };

            resp, body = self.api_client.postCredentials(body,id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                return passed
            else :
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                status['CAM-APITest'] = False
                return False
        except:
            resp, body = self.api_client.deleteAccountV2(id1)
            print (resp)
            status['CAM-APITest'] = False
            return False

    @assignOrder(98)
    def verifyPut_InvalidContext(self):
        try:
            passed = False
            randID = 'TestAWSAc'
            randID += str(x)
            print (randID)
            crefId="cred1"
            # crefId_Updated="cred2"
            id1 = "f16b0f4a-test-automation-0925"
            credupdatedName="cred_Updated_123"
            access_Key="100100"
            secret_Key="200200"

            # create a credRef
            accessKey=utils.decodeCredential(amazon_accessKey)
            secretKey=utils.decodeCredential(amazon_secretKey)

            crefId_Certificate="automationTestingCoreX"
            body = {
                    "crefId":crefId_Certificate,
                    "certificate": {
                        "secretKey": secretKey,
                        "accesskey":accessKey
                    }
                    };
            resp, body = self.api_client.postCertificateRefs(body)
            print (resp)

            body = {"account":
                    {
                        "accountId": id1,
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
                                "credentialName": "cred1",
                                "crefId": crefId,
                                "id":crefId,
                                "passwordFields": {
                                    "secretKey": secret_Key,
                                    "accessKey": access_Key
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

            # do a PUT account call
            body = {"account":
                    {
                        "accountId":id1,
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
                                "credentialName": credupdatedName,
                                "id":crefId,
                                "crefId": crefId_Certificate,
                                "purpose": [
                                    "provisioning"
                                ],
                                "context": [
                                    {
                                        "team": [
                                            "CORE-X111"
                                        ]
                                    }
                                ]
                                ,
                            "status": "Active"
                            }
                        ]
                    }
                    };

            resp, body = self.api_client.update_account(body, id1)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)

            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId_Certificate,headersUser1)
                print (resp)
                return passed
            else :
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId_Certificate,headersUser1)
                print (resp)
                status['CAM-APITest'] = False
                return False
        except:
                resp, body = self.api_client.deleteAccountV2(id1)
                print (resp)
                resp, body = self.api_client.deleteCertificateRefsById(crefId_Certificate,headersUser1)
                print (resp)
                status['CAM-APITest'] = False
                return False
