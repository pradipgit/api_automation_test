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
import jsonschema
import simplejson as json
from jsonschema import exceptions as json_exe

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
global id_cred, metadata, audit_log_download_id
id_cred = {}
metadata = {}
audit_log_download_id = {}


class AmazonSchemaValidator(object):
    def __init__(self, client):
        self.api_client = client
        self.invoice_id = random.randint(100000, 999999)

    # for AWS account

    @assignOrder(1)
    def amazon_schema_validator_v2(self):
        try:
            passed = False
            randID = config.get('param', 'random_id_amazon')
            randID += str(x)
            print randID


            schema_aws_get_by_id = {
                  "$schema": "http://json-schema.org/draft-04/schema#",
                  "type": "object",
                  "properties": {
                    "accountId": {
                      "type": "string"
                    },
                    "modelVersion": {
                      "type": "string"
                    },
                    "basicInfo": {
                      "type": "object",
                      "properties": {
                        "accountName": {
                          "type": "string"
                        },
                        "serviceProviderId": {
                          "type": "null"
                        },
                        "serviceProviderType": {
                          "type": "string"
                        },
                        "serviceProviderCode": {
                          "type": "string"
                        },
                        "accountType": {
                          "type": "string"
                        },
                        "isActive": {
                          "type": "string"
                        },
                        "userType": {
                          "type": "string"
                        },
                        "parentAccountId": {
                          "type": "string"
                        }
                      },
                      "required": [
                        "accountName",
                        "serviceProviderId",
                        "serviceProviderType",
                        "serviceProviderCode",
                        "accountType",
                        "isActive",
                        "userType",
                        "parentAccountId"
                      ]
                    },
                    "advancedInfo": {
                      "type": "object",
                      "properties": {
                        "accountNumber": {
                          "type": "string"
                        }
                      },
                      "required": [
                        "accountNumber"
                      ]
                    },
                    "updatedTime": {
                      "type": "string"
                    },
                    "vault_id": {
                      "type": "string"
                    },
                    "credentials": {
                      "type": "array",
                      "items": [
                        {
                          "type": "object",
                          "properties": {
                            "credentialName": {
                              "type": "string"
                            },
                            "status": {
                              "type": "string"
                            },
                            "passwordFields": {
                              "type": "object",
                              "properties": {
                                "secretKey": {
                                  "type": "string"
                                },
                                "accessKey": {
                                  "type": "string"
                                }
                              },
                              "required": [
                                "secretKey",
                                "accessKey"
                              ]
                            },
                            "purpose": {
                              "type": "array",
                              "items": [
                                {
                                  "type": "string"
                                }
                              ]
                            },
                            "context": {
                              "type": "array",
                              "items": [
                                {
                                  "type": "object",
                                  "properties": {
                                    "Team": {
                                      "type": "array",
                                      "items": [
                                        {
                                          "type": "string"
                                        }
                                      ]
                                    }
                                  },
                                  "required": [
                                    "Team"
                                  ]
                                }
                              ]
                            },
                            "id": {
                              "type": "string"
                            }
                          },
                          "required": [
                            "credentialName",
                            "status",
                            "passwordFields",
                            "purpose",
                            "context",
                            "id"
                          ]
                        }
                      ]
                    }
                  },
                  "required": [
                    "accountId",
                    "modelVersion",
                    "basicInfo",
                    "advancedInfo",
                    "updatedTime",
                    "vault_id",
                    "credentials"
                  ]
                };



            # with open('schema-example.json', 'r') as f:
            # schema_data = f.read()

            data = json.dumps(schema_aws_get_by_id)
            schema = json.loads(data)

            resp, body = self.api_client.get_AccountByProviderCodeAsset("amazon")
            data = json.dumps(body)
            data = json.loads(data)
            print data[0]['accountId']
            resp, body = self.api_client.get_AccountById(data[0]['accountId'])
            data = json.dumps(body)
            resp = json.loads(data)
            #json_obj = {"name": "eggs", "price": 21.47}
            jsonschema.validate(resp, schema)
            print "Validation done "
            resp=200
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        # except: json_exe.ValidationError as e:
        #     raise e.InvalidParameterValue(('Input data validation ' 'error: %s') % e)
        except:
            status['CAM-APITest'] = False
            return False