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
accountId = 'f16b0f4a-a76e-499e-b5f7-autoawsintegration'

#               states type    provider credential purpose org team context password-state
#   valid       s1     asset   aws       1          1       1   1    0      unmasked
#   valid       s2     asset   aws       1          1       1   1    1      unmasked
#   valid       s3     asset   aws       2          1       1   1    1      unmasked
#   invalid     s4     asset   aws       0          1       1   1    0      unmasked
#   invalid     s4     asset   aws       1          0       1   1    1      unmasked
#   invalid     s6     asset   aws       1          1       1   0    0      unmasked


class AccountOnBoarding(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)

#####################################S1 to S2,S3,S4,S5,S6 ######################################

    @assignOrder(600)
    def getCredential_noAppEnvContext_S1(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]

        body = {
            "account":{
                "basicInfo": {
                    "accountName": randID,
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.create_account(body)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        resp, body = self.api_client.deleteAccountV2(id)
        print resp
        return passed

    @assignOrder(601)
    def getCredential_withContext_S1_to_S2(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(602)
    def getCredential_noAppEnvContext_S2_to_S1(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(603)
    def getCredential_with_multipleCredentials_S1_to_S3(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    },
                    {
                        "credentialName": "autocred2",
                        "status": "Active",
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjalksdj",
                            "accessKey": "354634634564"
                        },
                        "purpose": [
                            "provisioning"
                        ],
                        "context": [
                            {
                                "Team": [
                                    "MYTEAM"
                                ]
                            }
                        ]
                      }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(604)
    def getCredential_noAppEnvContext_S3_to_S1(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(605)
    def getCredential_when_noCredential_S1_to_S4(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "4564356456"
                },
                "credentials": [

                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, '')
        print resp
        print body
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, '')
        passOfResponseCode = assertEqual(resp, 404)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(606)
    def getCredential_noAppEnvContext_S4_to_S1(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed



    @assignOrder(607)
    def getCredential_noPurpose_S1_to_S5(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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

                        ],
                        "status": "Active",
                        "context": [
                                {
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(608)
    def getCredential_noAppEnvContext_S5_to_S1(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(609)
    def getCredential_noTeamAndContext_S1_to_S6(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "674567451"
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
                                "Organization": [
                                    "All Organizations"
                                ]
                            }
                        ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body, id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(610)
    def getCredential_noAppEnvContext_S6_to_S1(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed



#####################################S2 to S1,S3,S4,S5,S6 ######################################

    @assignOrder(611)
    def getCredential_withContext_S2(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(612)
    def getCredential_with_multipleCredentials_S2_to_S3(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    },
                    {
                        "credentialName": "autocred2",
                        "status": "Active",
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjalksdj",
                            "accessKey": "354634634564"
                        },
                        "purpose": [
                            "provisioning"
                        ],
                        "context": [
                            {
                                "Team": [
                                    "MYTEAM"
                                ]
                            }
                        ]
                      }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(613)
    def getCredential_withContext_S3_to_S2(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(614)
    def getCredential_when_noCredential_S2_to_S4(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "4564356456"
                },
                "credentials": [

                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, '')
        print resp
        print body
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, '')
        passOfResponseCode = assertEqual(resp, 404)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(615)
    def getCredential_withContext_S4_to_S2(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed



    @assignOrder(616)
    def getCredential_noPurpose_S2_to_S5(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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

                        ],
                        "status": "Active",
                        "context": [
                                {
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(617)
    def getCredential_withContext_S5_to_S2(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(618)
    def getCredential_noTeamAndContext_S2_to_S6(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "674567451"
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
                                "Organization": [
                                    "All Organizations"
                                ]
                            }
                        ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body, id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(619)
    def getCredential_withContext_S6_to_S2(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ],
                                    "environment": [
                                        "All Environments"
                                    ],
                                    "application": [
                                        "All Applications"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

########################### S3 to S4,S5,S6 ###############

    @assignOrder(620)
    def getCredential_with_multipleCredentials_S3(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    },
                    {
                        "credentialName": "autocred2",
                        "status": "Active",
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjalksdj",
                            "accessKey": "354634634564"
                        },
                        "purpose": [
                            "provisioning"
                        ],
                        "context": [
                            {
                                "Team": [
                                    "MYTEAM"
                                ]
                            }
                        ]
                      }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(621)
    def getCredential_when_noCredential_S3_to_S4(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "4564356456"
                },
                "credentials": [

                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, '')
        print resp
        print body
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, '')
        passOfResponseCode = assertEqual(resp, 404)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(622)
    def getCredential_with_multipleCredentials_S4_to_S3(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    },
                    {
                        "credentialName": "autocred2",
                        "status": "Active",
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjalksdj",
                            "accessKey": "354634634564"
                        },
                        "purpose": [
                            "provisioning"
                        ],
                        "context": [
                            {
                                "Team": [
                                    "MYTEAM"
                                ]
                            }
                        ]
                      }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(623)
    def getCredential_noPurpose_S3_to_S5(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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

                        ],
                        "status": "Active",
                        "context": [
                            {
                                "Team": [
                                    "MYTEAM"
                                ]
                            },
                            {
                                "Organization": [
                                    "All Organizations"
                                ]
                            }
                        ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body, id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(624)
    def getCredential_with_multipleCredentials_S5_to_S3(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    },
                    {
                        "credentialName": "autocred2",
                        "status": "Active",
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjalksdj",
                            "accessKey": "354634634564"
                        },
                        "purpose": [
                            "provisioning"
                        ],
                        "context": [
                            {
                                "Team": [
                                    "MYTEAM"
                                ]
                            }
                        ]
                      }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(625)
    def getCredential_noTeamAndContext_S3_to_S6(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "674567451"
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
                                "Organization": [
                                    "All Organizations"
                                ]
                            }
                        ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body, id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(626)
    def getCredential_with_multipleCredentials_S6_to_S3(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    },
                    {
                        "credentialName": "autocred2",
                        "status": "Active",
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjalksdj",
                            "accessKey": "354634634564"
                        },
                        "purpose": [
                            "provisioning"
                        ],
                        "context": [
                            {
                                "Team": [
                                    "MYTEAM"
                                ]
                            }
                        ]
                      }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

################### S4 to S5 ,S6 ###########

    @assignOrder(627)
    def getCredential_when_noCredential_S4(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "4564356456"
                },
                "credentials": [

                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, '')
        print resp
        print body
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, '')
        passOfResponseCode = assertEqual(resp, 404)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(628)
    def getCredential_noPurpose_S4_to_S5(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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

                        ],
                        "status": "Active",
                        "context": [
                                {
                                    "Team": [
                                        "MYTEAM"
                                    ]
                                },
                                {
                                    "Organization": [
                                        "All Organizations"
                                    ]
                                }
                              ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
            };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(629)
    def getCredential_when_noCredential_S5_to_S4(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "4564356456"
                },
                "credentials": [

                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, '')
        print resp
        print body
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, '')
        passOfResponseCode = assertEqual(resp, 404)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(630)
    def getCredential_noTeamAndContext_S4_to_S6(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "674567451"
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
                                "Organization": [
                                    "All Organizations"
                                ]
                            }
                        ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body, id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(631)
    def getCredential_when_noCredential_S6_to_S4(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account":{
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "4564356456"
                },
                "credentials": [

                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body,id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, '')
        print resp
        print body
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, '')
        passOfResponseCode = assertEqual(resp, 404)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    #################### S5 to S6 ############

    @assignOrder(632)
    def getCredential_noPurpose_S5(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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

                        ],
                        "status": "Active",
                        "context": [
                            {
                                "Team": [
                                    "MYTEAM"
                                ]
                            },
                            {
                                "Organization": [
                                    "All Organizations"
                                ]
                            }
                        ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body, id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(633)
    def getCredential_noTeamAndContext_S5_to_S6(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
                    "serviceProviderCode": "amazon",
                    "credential_count": 1
                },
                "advancedInfo": {
                    "accountNumber": "674567451"
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
                                "Organization": [
                                    "All Organizations"
                                ]
                            }
                        ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body, id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(634)
    def getCredential_noPurpose_S6_to_S5(self):
        passed = False
        randID = 'TestAWSAc'
        randID += str(x)
        print randID
        # print metadata[0]
        id1 = "f16b0f4a-a76e-499e-b5f7-autoawsintegration"
        resp, body = self.api_client.get_AccountById(id1)
        data = json.dumps(body)
        data = json.loads(data)

        body = {
            "account": {
                "basicInfo": {
                    "accountName": data["basicInfo"]["accountName"],
                    "serviceProviderType": "amazon",
                    "isActive": "Active",
                    "accountType": "subaccount",
                    "userType": "asset",
                    "parentAccountId": "default_billing_account_amazon",
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

                        ],
                        "status": "Active",
                        "context": [
                            {
                                "Team": [
                                    "MYTEAM"
                                ]
                            },
                            {
                                "Organization": [
                                    "All Organizations"
                                ]
                            }
                        ],
                        "passwordFields": {
                            "secretKey": "lkjasdlkfjasldfjljsdf",
                            "accessKey": "lkasdjfalksdjflkj",
                            "accountNumber": "lkjasdjfljasd"
                        }

                    }
                ],
                "accountId": "f16b0f4a-a76e-499e-b5f7-autoawsintegration"

            }
        };

        print body
        resp, body = self.api_client.update_account(body, id1)
        print resp
        print body
        logger.info("API response:" + str(resp))
        resp, body = self.api_client.getCredentialsByName(accountId, 'autocred1')
        data = json.dumps(body)
        data = json.loads(data)
        print data['credentials'][0]['id']
        resp, body = self.api_client.getCredentialsByCredentialId(accountId, data['credentials'][0]['id'])
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed
