import time
import subprocess
import utils
from utils import assignOrder
from utils import assertEqual
from utils import assertContains
from utils import randomString
import threading
import Queue
import random
from collections import OrderedDict
import logging
import pprint
import ConfigParser
import json
import random
import requests
import datetime

import random

global status
status = {}
logger = logging.getLogger("Test Run")
config = ConfigParser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
global id_cred,metadata,audit_log_download_id
id_cred={}
metadata={}
audit_log_download_id={}

class serviceProviders(object):
    def __init__(self,client):
        self.api_client = client

    @assignOrder(1)
    def delete_Google_ServiceProvider(self):
        adapterId=""
        try:
            passed = False
            resp, body = self.api_client.get_serviceProvider("google")
            print resp
            resp, body = self.api_client.get_VaultConfiguration()
            print resp
            data = json.dumps(body)
            data = json.loads(data)
            adapterId=data[0]['vault_id']
            print adapterId
            resp, body = self.api_client.delete_serviceProvider("google")
            print resp
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                body = {
                    "vaultAdaptorId":adapterId,
                    "serviceProviderName":"Google",
                    "serviceProviderType":"google",
                    "serviceProviderCode":"google"
                };
                resp, body = self.api_client.create_serviceProviders(body)
                print resp
                return passed
        except:
            status['CAM-APITest'] = False
            body = {
                "vaultAdaptorId": adapterId,
                "serviceProviderName": "Google",
                "serviceProviderType": "google",
                "serviceProviderCode": "google"
            };
            resp, body = self.api_client.create_serviceProviders(body)
            print resp
            return False

    @assignOrder(2)
    def delete_Amazon_ServiceProvider(self):
        adapterId = ""
        try:
            passed = False
            resp, body = self.api_client.get_serviceProvider("amazon")
            print resp
            resp, body = self.api_client.get_VaultConfiguration()
            print resp
            data = json.dumps(body)
            data = json.loads(data)
            adapterId = data[0]['vault_id']
            print adapterId
            resp, body = self.api_client.delete_serviceProvider("amazon")
            print resp
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                body = {
                    "vaultAdaptorId": adapterId,
                    "serviceProviderName": "Amazon",
                    "serviceProviderType": "amazon",
                    "serviceProviderCode": "amazon"
                };
                resp, body = self.api_client.create_serviceProviders(body)
                print resp
                return passed
        except:
            status['CAM-APITest'] = False
            body = {
                "vaultAdaptorId": adapterId,
                "serviceProviderName": "Amazon",
                "serviceProviderType": "amazon",
                "serviceProviderCode": "amazon"
            };
            resp, body = self.api_client.create_serviceProviders(body)
            print resp
            return False

    @assignOrder(3)
    def delete_VRA_ServiceProvider(self):
        adapterId = ""
        try:
            passed = False
            resp, body = self.api_client.get_serviceProvider("vra")
            print resp
            resp, body = self.api_client.get_VaultConfiguration()
            print resp
            data = json.dumps(body)
            data = json.loads(data)
            adapterId = data[0]['vault_id']
            print adapterId
            resp, body = self.api_client.delete_serviceProvider("vra")
            print resp
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                body = {
                    "vaultAdaptorId": adapterId,
                    "serviceProviderName": "VRA",
                    "serviceProviderType": "vra",
                    "serviceProviderCode": "vra"
                };
                resp, body = self.api_client.create_serviceProviders(body)
                print resp
                return passed
        except:
            status['CAM-APITest'] = False
            body = {
                "vaultAdaptorId": adapterId,
                "serviceProviderName": "VRA",
                "serviceProviderType": "vra",
                "serviceProviderCode": "vra"
            };
            resp, body = self.api_client.create_serviceProviders(body)
            print resp
            return False

    @assignOrder(4)
    def delete_softlayer_ServiceProvider(self):
        adapterId = ""
        try:
            passed = False
            resp, body = self.api_client.get_serviceProvider("softlayer")
            print resp
            resp, body = self.api_client.get_VaultConfiguration()
            print resp
            data = json.dumps(body)
            data = json.loads(data)
            adapterId = data[0]['vault_id']
            print adapterId
            resp, body = self.api_client.delete_serviceProvider("softlayer")
            print resp
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                body = {
                    "vaultAdaptorId": adapterId,
                    "serviceProviderName": "IBM",
                    "serviceProviderType": "ibm",
                    "serviceProviderCode": "softlayer"
                };
                resp, body = self.api_client.create_serviceProviders(body)
                print resp
                return passed
        except:
            status['CAM-APITest'] = False
            body = {
                "vaultAdaptorId": adapterId,
                "serviceProviderName": "IBM",
                "serviceProviderType": "ibm",
                "serviceProviderCode": "softlayer"
            };
            resp, body = self.api_client.create_serviceProviders(body)
            print resp
            return False

    @assignOrder(5)
    def delete_icd_ServiceProvider(self):
        adapterId = ""
        try:
            passed = False
            resp, body = self.api_client.get_serviceProvider("icd")
            print resp
            resp, body = self.api_client.get_VaultConfiguration()
            print resp
            data = json.dumps(body)
            data = json.loads(data)
            adapterId = data[0]['vault_id']
            print adapterId
            resp, body = self.api_client.delete_serviceProvider("icd")
            print resp
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                body = {
                    "vaultAdaptorId": adapterId,
                    "serviceProviderName": "ICD",
                    "serviceProviderType": "icd",
                    "serviceProviderCode": "icd"
                };
                resp, body = self.api_client.create_serviceProviders(body)
                print resp
                return passed
        except:
            status['CAM-APITest'] = False
            body = {
                    "vaultAdaptorId": adapterId,
                    "serviceProviderName": "ICD",
                    "serviceProviderType": "icd",
                    "serviceProviderCode": "icd"
            };
            resp, body = self.api_client.create_serviceProviders(body)
            print resp
            return False

    @assignOrder(6)
    def delete_azure_ServiceProvider(self):
        adapterId = ""
        try:
            passed = False
            resp, body = self.api_client.get_serviceProvider("azure")
            print resp
            resp, body = self.api_client.get_VaultConfiguration()
            print resp
            data = json.dumps(body)
            data = json.loads(data)
            adapterId = data[0]['vault_id']
            print adapterId
            resp, body = self.api_client.delete_serviceProvider("azure")
            print resp
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                body = {
                    "vaultAdaptorId": adapterId,
                    "serviceProviderName": "Azure",
                    "serviceProviderType": "azure",
                    "serviceProviderCode": "azure"
                };
                resp, body = self.api_client.create_serviceProviders(body)
                print resp
                return passed
        except:
            status['CAM-APITest'] = False
            body = {
                    "vaultAdaptorId": adapterId,
                    "serviceProviderName": "Azure",
                    "serviceProviderType": "azure",
                    "serviceProviderCode": "azure"
            };
            resp, body = self.api_client.create_serviceProviders(body)
            print resp
            return False

    @assignOrder(7)
    def delete_snow_ServiceProvider(self):
        adapterId = ""
        try:
            passed = False
            resp, body = self.api_client.get_serviceProvider("snow")
            print resp
            resp, body = self.api_client.get_VaultConfiguration()
            print resp
            data = json.dumps(body)
            data = json.loads(data)
            adapterId = data[0]['vault_id']
            print adapterId
            resp, body = self.api_client.delete_serviceProvider("snow")
            print resp
            passOfResponseCode = assertEqual(resp, 204)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                body = {
                    "vaultAdaptorId": adapterId,
                    "serviceProviderName": "Managed ServiceNow IT Services",
                    "serviceProviderType": "snow",
                    "serviceProviderCode": "snow"
                };
                resp, body = self.api_client.create_serviceProviders(body)
                print resp
                return passed
        except:
            status['CAM-APITest'] = False
            body = {
                "vaultAdaptorId": adapterId,
                "serviceProviderName": "Managed ServiceNow IT Services",
                "serviceProviderType": "snow",
                "serviceProviderCode": "snow"
            };
            resp, body = self.api_client.create_serviceProviders(body)
            print resp
            return False

    @assignOrder(8)
    def delete_Invalid_ServiceProvider(self):
        adapterId = ""
        try:
            passed = False
            resp, body = self.api_client.delete_serviceProvider("xyz123")
            print resp
            passOfResponseCode = assertEqual(resp, 500)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
        except:
            status['CAM-APITest'] = False
            return False
