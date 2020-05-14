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
import time
import sys
status = {}
logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
# amazon
amazon_accessKey = config.get('aws', 'accessKey')
amazon_secretKey = config.get('aws', 'secretKey')

# azure
azure_clientId = config.get('azure', 'clientId')
azure_secret = config.get('azure', 'secret')
azure_subscriptionID = config.get('azure', 'subscriptionID')
azure_offerID = config.get('azure', 'offerID')
azure_tenantID = config.get('azure', 'tenantID')
azure_domain = config.get('azure', 'domain')

# google
google_serviceKey = config.get('google', 'serviceKey')
google_projectName = config.get('google', 'projectName')
google_projectId = config.get('google', 'projectId')
google_serviceAccountName = config.get('google', 'serviceAccountName')

# ibm
ibm_username = config.get('ibm', 'username')
ibm_apikey = config.get('ibm', 'apikey')

# icd
icd_username = config.get('icd', 'username')
icd_password = config.get('icd', 'password')

# snow
snow_username = config.get('snow', 'username')
snow_password = config.get('snow', 'password')

# vra
vra_username = config.get('vra', 'username')
vra_password = config.get('vra', 'password')

# azureBilling
azureBilling_applicationSecret = config.get('azureBilling', 'applicationSecret')

# googlebilling
googlebilling_serviceKey = config.get('googlebilling', 'serviceKey')
googlebilling_dataSet=config.get('googlebilling', 'dataSet')
googlebilling_bucket=config.get('googlebilling', 'bucket')

# snowBilling
snowBilling_username = config.get('snowBilling', 'username')
snowBilling_password=config.get('snowBilling', 'password')
snowBilling_url=config.get('snowBilling', 'url')

# vraBilling
vraBilling_username = config.get('vraBilling', 'username')
vraBilling_password=config.get('vraBilling', 'password')
vraBilling_tenant=config.get('vraBilling', 'tenant')

# aws-invalid
aws_invalid_accessKey = config.get('awsInvalid','accessKey')
aws_invalid_secretKey = config.get('awsInvalid','secretKey')

# aws-testConnection
aws_testConnection_accessKey = config.get('awsTestConnection', 'accessKey')
aws_testConnection_secretKey = config.get('awsTestConnection', 'secretKey')

now = datetime.datetime.now()
x = random.randint(0, 80000)
crefId2 = ""
username1 = config.get('authorization', 'username_systemuser')
apikey1 = config.get('authorization', 'apikey_systemuser')
global user_name
crefId = "automationTesting"
ROOT_DIR = os.path.abspath(os.curdir)
serviceProvider_folder = path.join(ROOT_DIR + "/testdata", "service-provider")
serviceProviderMetadata_folder = path.join(ROOT_DIR + "/testdata", "service-provider-metadata")
file_to_open = path.join(serviceProvider_folder, "sprovider.json")
file_to_open_metadata = path.join(serviceProviderMetadata_folder, "sproviderMetadata.json")

class prerequisite(object):
    def __init__(self, client):

        self.api_client = client

        global user_name

        if(sys.argv[1]=='automation-core-b'):
            user_name = config.get('params', 'username_mt')
        else:
            user_name = config.get('params', 'username')


        with open(file_to_open, 'r') as file:
            json_data = json.load(file)
            resp, body = self.api_client.get_VaultConfiguration()
            data = json.dumps(body)
            data = json.loads(data)
            print (resp)
            vault_id=data[0]['vault_id']
            print ("Vault Id is:")
            print (vault_id)
            if (json_data['amazon']['vaultAdaptorId']==vault_id):
                print ("Valid VaultID already present in Service Provider Json")
            else :
                json_data['amazon']['vaultAdaptorId']=vault_id
                json_data['aws']['vaultAdaptorId']=vault_id
                json_data['azure']['vaultAdaptorId']=vault_id
                json_data['vra']['vaultAdaptorId']=vault_id
                json_data['icd']['vaultAdaptorId']=vault_id
                json_data['softlayer']['vaultAdaptorId']=vault_id
                json_data['snow']['vaultAdaptorId']=vault_id
                json_data['google']['vaultAdaptorId']=vault_id
                print ("Changed the VaultID in Service Provider Json")
        with open(file_to_open, 'w') as file:
            json.dump(json_data, file)

        with open(file_to_open, "r+") as jsonFile:
            self.testdatajson = json.load(jsonFile)
            jsonFile.close()
        with open(file_to_open_metadata, "r+") as jsonFile:
            self.testdatajsonMetadata = json.load(jsonFile)
            jsonFile.close()

    @assignOrder(1)
    def patch_readonlyFalse(self):
        try :
            passed = False
            resp, body = self.api_client.get_VaultConfiguration()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['vault_id'])
            vault_id=data[0]['vault_id']

            body = {
                "isReadOnly": "false"
            };
            resp, body = self.api_client.patch_VaultConfiguration(body,data[0]['vault_id'])
            print (resp)
            passOfResponseCode = assertEqual(resp, 200)
            if(passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(2)
    def createCredRefId_Amazon(self):
        try :
            passed = False
            resp = self.api_client.createAWS_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(3)
    def createCredRefId_Azure(self):
        try :
            passed = False
            resp = self.api_client.createAzure_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(4)
    def createCredRefId_Google(self):
        try :
            passed = False
            resp = self.api_client.createGoogle_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(5)
    def createCredRefId_IBMCloud(self):
        try :
            passed = False
            resp = self.api_client.createIBMCloud_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(6)
    def createCredRefId_ICD(self):
        try :
            passed = False
            resp = self.api_client.createICD_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(7)
    def createCredRefId_Snow(self):
        try :
            passed = False
            resp = self.api_client.createSnow_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(8)
    def createCredRefId_VRA(self):
        try :
            passed = False
            resp = self.api_client.createVRA_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(9)
    def createCredRefId_Azure_Billing(self):
        try :
            passed = False
            resp = self.api_client.createAzureBilling_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(10)
    def createCredRefId_Google_Billing(self):
        try :
            passed = False
            resp = self.api_client.createGoogleBilling_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(11)
    def createCredRefId_Snow_Billing(self):
        try :
            passed = False
            resp = self.api_client.createSnowBilling_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(12)
    def createCredRefId_VRA_Billing(self):
        try :
            passed = False
            resp = self.api_client.createVRABilling_CredRefs()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(13)
    def createInvalidCredRefId_Amazon(self):
        try :
            passed = False
            resp = self.api_client.createInvalidCredRef_Amazon()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(14)
    def postCredRef_Automation(self):
        try :
            passed = False
            resp = self.api_client.createCredRef_Automation()
            print (resp)
            resp1=resp
            if(resp1==200 or resp1==409) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(15)
    def onboard_amazon(self):
        try :
            passed = False
            # delete the service provider
            resp, body = self.api_client.delete_serviceProvider("amazon")
            print (resp)
            print ("Deleted amazon Service Provider")
            # delete the aws provider and accountMetadata
            resp, body = self.api_client.delete_serviceProviderMetadata("amazon")
            print (resp)
            print ("Deleted amazon Service Provider Metadata")

            body = self.testdatajsonMetadata["amazon"]
            resp, body = self.api_client.create_serviceProvidersMetadata(body)
            print (resp)
            print ("Added amazon Service Provider Metadata")
            # add the service provider for aws
            body = self.testdatajson["amazon"]
            print (body)
            resp, body = self.api_client.create_serviceProviders(body)
            print (resp)

            print ("Added amazon Service Provider")
            resp1=resp
            if(resp1==200 or resp1==409 or resp1==201) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(16)
    def onboard_azure(self):
        try :
            passed = False
            # delete the service provider
            resp, body = self.api_client.delete_serviceProvider("azure")
            print (resp)
            print ("Deleted azure Service Provider")
            # delete the aws provider and accountMetadata
            resp, body = self.api_client.delete_serviceProviderMetadata("azure")
            print (resp)
            print ("Deleted azure Service Provider Metadata")

            body = self.testdatajsonMetadata["azure"]
            resp, body = self.api_client.create_serviceProvidersMetadata(body)
            print (resp)
            print ("Added azure Service Provider Metadata")
            # add the service provider for aws
            body = self.testdatajson["azure"]
            resp, body = self.api_client.create_serviceProviders(body)
            print (resp)
            print ("Added azure Service Provider")
            resp1=resp
            if(resp1==200 or resp1==409 or resp1==201) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(17)
    def onboard_google(self):
        try :
            passed = False
            # delete the service provider
            resp, body = self.api_client.delete_serviceProvider("google")
            print (resp)
            print ("Deleted google Service Provider")
            # delete the aws provider and accountMetadata
            resp, body = self.api_client.delete_serviceProviderMetadata("google")
            print (resp)
            print ("Deleted google Service Provider Metadata")

            body = self.testdatajsonMetadata["google"]
            resp, body = self.api_client.create_serviceProvidersMetadata(body)
            print (resp)
            print ("Added google Service Provider Metadata")
            # add the service provider for aws
            body = self.testdatajson["google"]
            resp, body = self.api_client.create_serviceProviders(body)
            print (resp)
            print ("Added google Service Provider")
            resp1=resp
            if(resp1==200 or resp1==409 or resp1==201) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(18)
    def onboard_softlayer(self):
        try :
            passed = False
            # delete the service provider
            resp, body = self.api_client.delete_serviceProvider("softlayer")
            print (resp)
            print ("Deleted softlayer Service Provider")
            # delete the aws provider and accountMetadata
            resp, body = self.api_client.delete_serviceProviderMetadata("softlayer")
            print (resp)
            print ("Deleted softlayer Service Provider Metadata")

            body = self.testdatajsonMetadata["softlayer"]
            resp, body = self.api_client.create_serviceProvidersMetadata(body)
            print (resp)
            print ("Added softlayer Service Provider Metadata")
            # add the service provider for aws
            body = self.testdatajson["softlayer"]
            resp, body = self.api_client.create_serviceProviders(body)
            print (resp)
            print ("Added softlayer Service Provider")
            resp1=resp
            if(resp1==200 or resp1==409 or resp1==201) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(19)
    def onboard_icd(self):
        try :
            passed = False
            # delete the service provider
            resp, body = self.api_client.delete_serviceProvider("icd")
            print (resp)
            print ("Deleted icd Service Provider")
            # delete the aws provider and accountMetadata
            resp, body = self.api_client.delete_serviceProviderMetadata("icd")
            print (resp)
            print ("Deleted icd Service Provider Metadata")

            body = self.testdatajsonMetadata["icd"]
            resp, body = self.api_client.create_serviceProvidersMetadata(body)
            print (resp)
            print ("Added icd Service Provider Metadata")
            # add the service provider for aws
            body = self.testdatajson["icd"]
            resp, body = self.api_client.create_serviceProviders(body)
            print (resp)
            print ("Added icd Service Provider")
            resp1=resp
            if(resp1==200 or resp1==409 or resp1==201) :
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
    def onboard_snow(self):
        try :
            passed = False
            # delete the service provider
            resp, body = self.api_client.delete_serviceProvider("snow")
            print (resp)
            print ("Deleted snow Service Provider")
            # delete the aws provider and accountMetadata
            resp, body = self.api_client.delete_serviceProviderMetadata("snow")
            print (resp)
            print ("Deleted snow Service Provider Metadata")

            body = self.testdatajsonMetadata["snow"]
            resp, body = self.api_client.create_serviceProvidersMetadata(body)
            print (resp)
            print ("Added snow Service Provider Metadata")
            # add the service provider for aws
            body = self.testdatajson["snow"]
            resp, body = self.api_client.create_serviceProviders(body)
            print (resp)
            print ("Added snow Service Provider")
            resp1=resp
            if(resp1==200 or resp1==409 or resp1==201) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(21)
    def onboard_vra(self):
        try :
            passed = False
            # delete the service provider
            resp, body = self.api_client.delete_serviceProvider("vra")
            print (resp)
            print ("Deleted vra Service Provider")
            # delete the aws provider and accountMetadata
            resp, body = self.api_client.delete_serviceProviderMetadata("vra")
            print (resp)
            print ("Deleted vra Service Provider Metadata")

            body = self.testdatajsonMetadata["vra"]
            resp, body = self.api_client.create_serviceProvidersMetadata(body)
            print (resp)
            print ("Added vra Service Provider Metadata")
            # add the service provider for aws
            body = self.testdatajson["vra"]
            resp, body = self.api_client.create_serviceProviders(body)
            print (resp)
            print ("Added vra Service Provider")
            resp1=resp
            if(resp1==200 or resp1==409 or resp1==201) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(22)
    def onboard_aws(self):
        try :
            passed = False
            # delete the service provider
            resp, body = self.api_client.delete_serviceProvider("aws")
            print (resp)
            print ("Deleted vra Service Provider")
            # delete the aws provider and accountMetadata
            resp, body = self.api_client.delete_serviceProviderMetadata("aws")
            print (resp)
            print ("Deleted vra Service Provider Metadata")

            body = self.testdatajsonMetadata["aws"]
            resp, body = self.api_client.create_serviceProvidersMetadata(body)
            print (resp)
            print ("Added vra Service Provider Metadata")
            # add the service provider for aws
            body = self.testdatajson["aws"]
            resp, body = self.api_client.create_serviceProviders(body)
            print (resp)
            print ("Added vra Service Provider")
            resp1=resp
            if(resp1==200 or resp1==409 or resp1==201) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(23)
    def generateSystemUser(self):
        try :
            passed = False
            userId="vijethkumarbs"
            # enable the authorization
            body = {
                     "enable": True
                };

            resp, body = self.api_client.enableAuthorization(body)
            print (resp)

            # generate a system user
            body = {
                    "enable": True,
                    "userid": userId,
                    "roles": [
                      "Audit Viewer","Service Integrator"
                    ]
                };

            resp, body = self.api_client.generateSystemUserId(body)
            print (resp)

            # generate API key for system userID
            body = {
                    "type": "systemuser"
                };

            resp, body = self.api_client.generateAPIKeyforSystemUserId(body,userId)
            print (resp)
            resp1=resp

            if(resp1==201) :
                # Print the API key
                data = json.dumps(body)
                data = json.loads(data)
                apikey=data['key']
                apikey=utils.encodeCredential(apikey)
                print (apikey)
                username=data['userid']
                print ("User Id is:")
                print (username)
                print ("Apikey is:")
                print (apikey)
                config.read('testdata.conf')
                config.set("authorization", "apikey_systemuser", apikey)
                with open("testdata.conf", "w") as f:
                    config.write(f)
            else :
                userId="vijethkumarbs"
                print ("The Username is Already Present so cant create API Key for this User")
                resp, body = self.api_client.getApikey(userId)
                print (resp)
                data = json.dumps(body)
                data = json.loads(data)
                apikey=data['key']
                apikey=utils.encodeCredential(apikey)
                username=data['userid']
                print ("User Id is:")
                print (username)
                print ("Apikey is:")
                print (apikey)
                config.read('testdata.conf')
                config.set("authorization", "apikey_systemuser", apikey)
                with open("testdata.conf", "w") as f:
                    config.write(f)

            if(resp1==201 or resp1==202) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(24)
    def createTeamandUser(self):
        try :
            # create a org
            passed = False
            body = [
                {
                	"id": "apiAutomation",
                	"name": "apiAutomation",
                	"description": "apiAutomation",
                	"status": "Active"
                }];

            resp, body = self.api_client.createOrg(body)
            print (resp)
            # create a team and assign roles
            body = {
                	"teamcode": "CORE-X",
                	"name": "CORE-X",
                	"org": "apiAutomation",
                	"enabled": True,
                	"roles": [{
                		"name": "Audit Admin",
                		"contexts": [{
                			"org": ["org_all"]
                		}],
                		"additionalinfo": {
                			"contexts": [{
                				"unassignedcontexts": [{}],
                				"org": ["org_all"]
                			}]
                		}
                	}, {
                		"name": "Audit Viewer",
                		"contexts": [{
                			"org": ["org_all"]
                		}],
                		"additionalinfo": {
                			"contexts": [{
                				"unassignedcontexts": [{}],
                				"org": ["org_all"]
                			}]
                		}
                	}]
                };

            resp, body = self.api_client.createTeam(body)
            print (resp)

            # assign user to that tem
            body = {
                    "user_id_list": [user_name],
                    "team_code_list": ["CORE-X"]
                };

            resp, body = self.api_client.assignUsersTeam(body)
            print (resp)
            resp1=resp

            if(resp1==200 or resp1==201 or resp1==202 or resp1==409 ) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(25)
    def patch_readonlyTrue(self):
        try :
            passed = False
            resp, body = self.api_client.get_VaultConfiguration()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['vault_id'])
            vault_id=data[0]['vault_id']

            body = {
                "isReadOnly": "true"
            };

            resp, body = self.api_client.patch_VaultConfiguration(body,data[0]['vault_id'])
            print (resp)
            passOfResponseCode = assertEqual(resp, 200)
            if(passOfResponseCode) :
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else :
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return
