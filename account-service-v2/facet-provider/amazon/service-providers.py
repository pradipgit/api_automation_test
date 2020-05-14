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
now = datetime.datetime.now()
# db=config.get('params','db')
# invalidUrl =config.get('params', 'invalidUrl')
x = random.randint(0, 50000)
global id_cred,metadata,audit_log_download_id
id_cred={}
metadata={}
audit_log_download_id={}

class ServiceProviderTest(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

    @assignOrder(140)
    def get_serviceProviderMetadata_test(self):
        try:
            passed = False
            resp, body = self.api_client.get_serviceProviderMetadata("testcoreauto")
            print resp
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(141)
    def get_serviceProvider_test(self):
        try:
            passed = False
            resp, body = self.api_client.get_serviceProviders("testcoreauto")
            print resp
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(142)
    def delete_serviceProvider_test(self):
        passed = False
        resp, body = self.api_client.get_serviceProviders("testcoreauto")
        data = json.dumps(body)
        data = json.loads(data)
        print data[0]['serviceProviderID']
        resp, body = self.api_client.delete_serviceProvider(data[0]['serviceProviderID'])
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(143)
    def delete_serviceProviderMetadata_test(self):
        passed = False
        resp, body = self.api_client.delete_serviceProviderMetadata("testcoreauto")
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 204)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(144)
    def post_serviceProviderMetadata_test(self):
        passed = False
        body = {
            "providerType": "testcoreauto",
            "displayName": "testcoreauto",
            "iconImage": "path of icon for this provider",
            "canSupportSubAccounts": "false",
            "canDiscoverSubAccounts": "false",
            "canDetachSubAccounts": "false",
            "canDoTestConnection": "false",
            "version": 1,
            "accountMetadata": {
                "dummyField1": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 25,
                    "canUpdate": "true",
                    "regex": "",
                    "displayLabel": "dummy field",
                    "helpText": "dummy field",
                    "appliesTo": [
                        {
                            "accountType": "billing",
                            "isRequired": "false"
                        },
                        {
                            "accountType": "asset",
                            "isRequired": "false"
                        }
                    ]
                }
            },
            "credentialMetadata": {
                "provisioning": {
                    "dummyfield2": {
                        "type": "password",
                        "canUpdate": "true",
                        "minLength": 8,
                        "maxLength": 20,
                        "isRequired": "true",
                        "displayLabel": "dummyfield2",
                        "helpText": "dummyfield2"
                    }
                }
            }
        };

        resp, body = self.api_client.create_serviceProvidersMetadata(body)
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(145)
    def put_serviceProviderMetadata_test(self):
        passed = False
        body = {
            "providerType": "testcoreauto",
            "displayName": "testcoreauto",
            "iconImage": "path of icon for this provider",
            "canSupportSubAccounts": "true",
            "canDiscoverSubAccounts": "true",
            "canDetachSubAccounts": "false",
            "canDoTestConnection": "false",
            "version": 1,
            "accountMetadata": {
                "dummyField1": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 25,
                    "canUpdate": "true",
                    "regex": "",
                    "displayLabel": "dummy field",
                    "helpText": "dummy field",
                    "appliesTo": [
                        {
                            "accountType": "billing",
                            "isRequired": "false"
                        },
                        {
                            "accountType": "asset",
                            "isRequired": "false"
                        }
                    ]
                }
            },
            "credentialMetadata": {
                "provisioning": {
                    "dummyfield2": {
                        "type": "password",
                        "canUpdate": "true",
                        "minLength": 8,
                        "maxLength": 20,
                        "isRequired": "true",
                        "displayLabel": "dummyfield2",
                        "helpText": "dummyfield2"
                    }
                }
            }
        };

        resp, body = self.api_client.update_serviceProviderMetadata(body, "testcoreauto")
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(146)
    def post_serviceProvider_test(self):
        passed = False
        body = {
            "serviceProviderType": "testcoreauto",
            "serviceProviderName": "testcoreauto",
            "vaultAdaptorId": "f2dd17dc-db3d-4a59-9315-db04a69a9055",
            "serviceProviderCode": "testcoreauto"
        };
        resp, body = self.api_client.create_serviceProviders(body)
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(147)
    def put_serviceProvider_test(self):
        passed = False
        body = {
            "serviceProviderType": "testcoreauto",
            "serviceProviderName": "testcoreauto",
            "vaultAdaptorId": "f2dd17dc-db3d-4a59-9315-db04a69a9055",
            "serviceProviderCode": "testcoreauto"
        };
        resp, body = self.api_client.update_serviceProvider(body, "testcoreauto")
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

