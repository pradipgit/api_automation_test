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

adapter_url = config.get('vault', 'vault_adapter_url')
endpoint_url = config.get('vault', 'vault_endpoint_url')


class ExternalVaultOnboarding(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

    @assignOrder(1)
    def getVaultConfigurationByName(self):
        try:
            passed = False
            resp, body = self.api_client.get_VaultConfiguration()
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


    @assignOrder(2)
    def deleteVaultConfiguration(self):
        try:
            passed = False
            resp, body = self.api_client.get_VaultConfiguration()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['vault_id'])
            resp, body = self.api_client.delete_VaultConfiguration(data[0]['vault_id'])
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


    @assignOrder(3)
    def postNewDefaultConfiguration(self):
        try:
            passed = False
            x = random.randint(0, 50000)
            randID = 'xys778'
            randID += str(x)
            print (randID)
            vault_adapter_url=utils.decodeCredential(adapter_url)
            vault_endpoint_url=utils.decodeCredential(endpoint_url)
            body = {
                "display_name": randID,
                "vault_type": "default",
                "isReadOnly": "false",
                "vault_adapter_url": vault_adapter_url,
                "vault_endpoint_url": vault_endpoint_url
            };
            resp, body = self.api_client.postVaultConfiguration(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 409)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(4)
    def deleteNewConfiguration(self):
        try:
            passed = False
            x = random.randint(0, 50000)
            randID = 'xys779'
            randID += str(x)
            print (randID)
            vault_adapter_url=utils.decodeCredential(adapter_url)
            vault_endpoint_url=utils.decodeCredential(endpoint_url)
            body = {
                "display_name": randID,
                "vault_type": "Test",
                "isReadOnly": "false",
                "vault_adapter_url": vault_adapter_url,
                "vault_endpoint_url": vault_endpoint_url
            };
            resp, body = self.api_client.postVaultConfiguration(body)
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['vault_id'])
            resp, body = self.api_client.delete_VaultConfiguration(data['vault_id'])
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
