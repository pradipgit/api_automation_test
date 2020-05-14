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


crefId = "automationTesting"
ROOT_DIR = os.path.abspath(os.curdir)
serviceProvider_folder = path.join(ROOT_DIR + "/testdata", "service-provider")
serviceProviderMetadata_folder = path.join(ROOT_DIR + "/testdata", "service-provider-metadata")
file_to_open = path.join(serviceProvider_folder, "sprovider.json")
file_to_open_metadata = path.join(serviceProviderMetadata_folder, "sproviderMetadata.json")

class prerequisite(object):
    def __init__(self, client):

        self.api_client = client


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
