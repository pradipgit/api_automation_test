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
crefId = "automationTesting"
crefId_certificate="automationTesting-1234"
username1 = config.get('authorization', 'username_systemuser')
apikey1 = config.get('authorization', 'apikey_systemuser')
global headersUser1

aws_s3Bucket = config.get('aws', 's3Bucket')
aws_accessKey = config.get('aws', 'accesskey')
aws_secretKey = config.get('aws', 'secretkey')
applicationsecret = config.get('azureBilling', 'applicationsecret')
azure_clientId = config.get('azure', 'clientId')
azure_secret = config.get('azure', 'secret')
azure_subscriptionID = config.get('azure', 'subscriptionID')
azure_offerID = config.get('azure', 'offerID')
azure_tenantID = config.get('azure', 'tenantID')
azure_domain = config.get('azure', 'domain')
google_servicekey = config.get('google', 'servicekey')
ibm_username = config.get('ibm', 'username')
ibm_apikey = config.get('ibm', 'apikey')


class AccountTestConnection(object):
    def __init__(self,client):
        global headersUser1
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)
        headersUser1 = {
            "Username": username1,
            "Content-Type": "application/json",
            "apikey": utils.decodeCredential(apikey1)
        }


    @assignOrder(1)
    def createCredential_WithValue(self):
        try:
            passed = False
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
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

    @assignOrder(2)
    def postCertificate_RefId(self):
        try :
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            print (crefId_certificate)
            body = {
                    "crefId":crefId_certificate,
                    "credential":
                        {
                         "value":{
                                    "accessKey" : accessKey,
                                    "secretKey" : secretKey
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
                return passed
        except:
            status['CAM-APITest'] = False
            return


    @assignOrder(3)
    def test_connection_amazon_billing_onlyPasswordField(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            body = {
                 "basicInfo": {
                "serviceProviderType": "amazon",
                "serviceProviderCode": "amazon",
                "userType": "billing"
                },
                "advancedInfo": {
                    "s3Bucket" : s3Bucket
                },
                "credentials": {
                    "passwordFields": {
                          "accessKey":accessKey,
                          "secretKey": secretKey
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(4)
    def test_connection_amazon_billing_withCrefId_PasswordFields(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            body = {
                 "basicInfo": {
                "serviceProviderType": "amazon",
                "serviceProviderCode": "amazon",
                "userType": "billing"
                },
                "advancedInfo": {
                    "s3Bucket" : s3Bucket
                },
                "credentials": {
                    "crefId": crefId,
                    "passwordFields": {
                          "accessKey": accessKey,
                          "secretKey": secretKey
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(6)
    def test_connection_amazon_billing_InvalidcrefId(self):
        try:
            passed = False
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            body = {
                 "basicInfo": {
                "serviceProviderType": "amazon",
                "serviceProviderCode": "amazon",
                "userType": "billing"
                },
                "advancedInfo": {
                    "s3Bucket" : s3Bucket
                },
                "credentials": {
                    "crefId": "Test76327397"
                }
            };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(7)
    def test_connection_amazon_billing_wrongPasswordField(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            body = {
                 "basicInfo": {
                "serviceProviderType": "amazon",
                "serviceProviderCode": "amazon",
                "userType": "billing"
                },
                "advancedInfo": {
                    "s3Bucket" : s3Bucket
                },
                "credentials": {
                    "passwordFields": {
                          "accessKey": accessKey+accessKey,
                          "secretKey": secretKey+secretKey
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(8)
    def test_connection_amazon_billing_validCredId_wrongPasswordField(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            body = {
                 "basicInfo": {
                "serviceProviderType": "amazon",
                "serviceProviderCode": "amazon",
                "userType": "billing"
                },
                "advancedInfo": {
                    "s3Bucket" : s3Bucket
                },
                "credentials": {
                    "crefId": crefId,
                    "passwordFields": {
                          "accessKey": accessKey+accessKey+accessKey,
                          "secretKey": secretKey+secretKey+secretKey
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(7)
    def test_connection_amazon_billing_InvalidCredId_validPasswordField(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            body = {
                 "basicInfo": {
                "serviceProviderType": "amazon",
                "serviceProviderCode": "amazon",
                "userType": "billing"
                },
                "advancedInfo": {
                    "s3Bucket" : s3Bucket
                },
                "credentials": {
                    "crefId": "test3763763737hdsgdsh",
                    "passwordFields": {
                          "accessKey": accessKey,
                          "secretKey": secretKey
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
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
    def createCredential_WithoutValue(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            print (crefId)
            body = {
                    "crefId":crefId,
                    "credential":
                        {
                            "accessKey": accessKey,
                            "secretKey": secretKey
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

    @assignOrder(12)
    def test_connection_emptypasswordFields(self):
        try:
            passed = False
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            print (crefId)
            body = {
                 "basicInfo": {
                "serviceProviderType": "azure",
                "serviceProviderCode": "azure",
                "userType": "billing"
                },
                "advancedInfo": {
                    "s3Bucket" : s3Bucket
                },
                "credentials": {
                    "crefId": crefId_certificate,
                    "passwordFields": {
		            "accessKey": " ",
		            "secretKey": " "
		        }
                }
            }
            resp, body = self.api_client.testConnection(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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

    @assignOrder(13)
    def test_connection_invalidProviders(self):
        try:
            passed = False
            print (crefId)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)
            body = {
                 "basicInfo": {
                "serviceProviderType": "azure",
                "serviceProviderCode": "azure",
                "userType": "billing"
                },
                "advancedInfo": {
                    "s3Bucket" : s3Bucket
                },
                "credentials": {
                    "crefId": crefId_certificate
                }
            }
            resp, body = self.api_client.testConnection(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                resp, body = self.api_client.deleteCertificateRefsById(crefId_certificate,headersUser1)
                print (resp)
                return passed
            else :
                status['CAM-APITest'] = False
                resp, body = self.api_client.deleteCertificateRefsById(crefId_certificate,headersUser1)
                print (resp)
                return False
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteCertificateRefsById(crefId_certificate,headersUser1)
            print (resp)
            return False

    @assignOrder(14)
    def test_connection_amazon_asset(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            body = {
             "basicInfo": {
            "serviceProviderType": "amazon",
            "serviceProviderCode": "amazon",
            "userType": "asset"
            },
            "advancedInfo": {
                "accountNumber": "2222222222"
            },
            "credentials": {
                "crefId": "123-456-789-012",
                "passwordFields": {
                       "accessKey": accessKey,
                        "secretKey": secretKey
                }
            }
            };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(15)
    def test_connection_google_asset(self):
        try:
            passed = False
            serviceKey=utils.decodeCredential(google_servicekey)
            body = {
                "basicInfo": {
                "serviceProviderType": "google",
                "serviceProviderCode": "google",
                "userType": "asset"
                },
                "advancedInfo": {
                    "accountNumber": "2222222222"
                },
                "credentials": {
                    "crefId": "123-456-789-012",
                    "passwordFields": {
                         "serviceKey":serviceKey
                    }
                }
                };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(16)
    def test_connection_ibm_asset(self):
        try:
            passed = False
            username=utils.decodeCredential(ibm_username)
            apikey=utils.decodeCredential(ibm_apikey)
            body = {
                "basicInfo": {
                    "serviceProviderType": "ibm",
                    "serviceProviderCode": "softlayer",
                    "userType": "asset"
                },
                "advancedInfo": {
                    "accountNumber": "2222222222"
                },
                "credentials": {
                "crefId": "123-456-789-012",
                    "passwordFields": {
                        "apiKey": apikey,
                        "username": username
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(17)
    def test_connection_azure_asset(self):
        try:
            passed = False

            tenantID=utils.decodeCredential(azure_tenantID)
            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            clientId=utils.decodeCredential(azure_clientId)
            secret=utils.decodeCredential(azure_secret)

            body = {
                "basicInfo": {
                    "serviceProviderType": "azure",
                    "serviceProviderCode": "azure",
                    "userType": "asset"

                },
                "advancedInfo": {
                    "tenantID": tenantID,
                    "subscriptionID": subscriptionID
                },
                "credentials":
                    {
                        "passwordFields": {
                            "clientId": clientId,
                            "secret": secret
                        }
                    }
            };
            resp, body = self.api_client.testConnection(body)
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
        ########################################## Test Connection Invalid Credentials ###################################

    @assignOrder(18)
    def test_connection_amazon_billing_invalidCredentials(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            s3Bucket=utils.decodeCredential(aws_s3Bucket)

            body = {
                "basicInfo": {
                    "serviceProviderType": "amazon",
                    "serviceProviderCode": "amazon",
                    "userType": "billing"
                },
                "advancedInfo": {
                    "s3Bucket": s3Bucket
                },
                "credentials": {
                "crefId": "123-456-789-012",
                    "passwordFields": {
                        "accessKey": accessKey,
                        "secretKey": secretKey+secretKey
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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

    @assignOrder(19)
    def test_connection_amazon_asset_invalidCredentials(self):
        try:
            passed = False
            accessKey=utils.decodeCredential(aws_accessKey)
            secretKey=utils.decodeCredential(aws_secretKey)
            body = {
                "basicInfo": {
                    "serviceProviderType": "amazon",
                    "serviceProviderCode": "amazon",
                    "userType": "asset"
                },
                "advancedInfo": {
                    "accountNumber": "2222222222"
                },
                "credentials": {
                "crefId": "123-456-789-012",
                    "passwordFields": {
                        "accessKey": accessKey+accessKey+accessKey,
                        "secretKey": secretKey+secretKey+secretKey
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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

    @assignOrder(20)
    def test_connection_google_asset_invalidCredentials(self):
        try:
            passed = False
            serviceKey=utils.decodeCredential(google_servicekey)
            body = {
                "basicInfo": {
                    "serviceProviderType": "google",
                    "serviceProviderCode": "google",
                    "userType": "asset"
                },
                "advancedInfo": {
                    "accountNumber": "2222222222"
                },
                "credentials": {
                    "passwordFields": {
                        "serviceKey": serviceKey+serviceKey
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(21)
    def test_connection_ibm_asset_invalidCredentials(self):
        try:
            passed = False
            username=utils.decodeCredential(ibm_username)
            apikey=utils.decodeCredential(ibm_apikey)
            body = {
                "basicInfo": {

                    "serviceProviderType": "ibm",
                    "serviceProviderCode": "softlayer",
                    "userType": "asset"
                },
                "advancedInfo": {
                    "accountNumber": "2222222222"
                },
                "credentials": {
                "crefId": "123-456-789-012",
                    "passwordFields": {
                        "apiKey": apikey+apikey+apikey,
                        "username": username+username
                    }
                }
            };
            resp, body = self.api_client.testConnection(body)
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

    @assignOrder(22)
    def test_connection_azure_asset_invalidCredentials(self):
        try:
            passed = False

            subscriptionID=utils.decodeCredential(azure_subscriptionID)
            offerID=utils.decodeCredential(azure_offerID)
            tenantID=utils.decodeCredential(azure_tenantID)
            # decoded values
            clientId=utils.decodeCredential(azure_clientId)
            secret=utils.decodeCredential(azure_secret)


            body = {
                "basicInfo": {
                    "serviceProviderType": "azure",
                    "serviceProviderCode": "azure",
                    "userType": "asset"
                },
                "advancedInfo": {
                    "tenantID": tenantID+tenantID,
                    "subscriptionID": subscriptionID+subscriptionID
                },
                "credentials":
                    {
                    "crefId": "123-456-789-012",
                        "passwordFields": {
                            "clientId": clientId+clientId,
                            "secret": secret+secret+secret
                        }
                    }
            };
            resp, body = self.api_client.testConnection(body)
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
