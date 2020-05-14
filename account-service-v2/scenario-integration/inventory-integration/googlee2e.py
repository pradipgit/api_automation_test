import time
import datetime
import utils
from utils import assignOrder
from utils import assertEqual
import random
import logging
import ConfigParser
import json
import sys
import os
import string
import requests
import operator
from junit_xml import TestCase
requests.packages.urllib3.disable_warnings()

global status, assetURL, operationURL, orderNumber, service_id, resource_id, service_id2, resource_id2, service_id3, resource_id3, accessoperationURL,serviceInstanceName
status = {}
orderNumber = "notfound"

logger = logging.getLogger("Test Run")
config = ConfigParser.ConfigParser()

config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')

config.read('testdata.conf')
service_id = config.get('resources', 'service_id1')
resource_id = config.get('resources', 'resource_id1')
service_id2 = config.get('resources', 'service_id2')
resource_id2 = config.get('resources', 'resource_id2')
service_id3 = config.get('resources', 'service_id3')
resource_id3 = config.get('resources', 'resource_id3')
provider = config.get('resources', 'provider')

config.read('testurls.conf')
assetURL = config.get('urls', 'assetURL')
accessoperationURL = config.get('urls', 'accessoperationURL')
operationURL = config.get('urls', 'operationURL')
deleteURL = config.get('urls', 'deleteURL')
viewPropertiesURL = config.get('urls', 'viewPropertiesURL')
auditPropertiesURL = config.get('urls', 'auditPropertiesURL')
viewPropertyURL = config.get('urls', 'viewPropertyURL')
EditSOI_URL= config.get('urls', 'EditSOIURL')
resourceStateURL = config.get('urls', 'resourceStateURL')
orderURL = config.get('urls', 'orderURL')
viewbudgetPropertiesURL= config.get('urls', 'viewbudgetPropertiesURL')

provider = "google"

class Google_Tests(object):
    def __init__(self,client):
        self.api_client = client

    @assignOrder(1)
    def Reg_Create_Google_order(self):
        test_case_result = TestCase(name="Reg_Create_Google_order", classname=self.__class__.__name__)
        global serviceInstanceName
        provider = "google"
        passed = False
        try:
            for i in range(1, 2):
                print "Placing order: " + str(i + 1)
                epoch_time = str(int(time.time()))
                serviceInstanceName = "testAPIGoogle" + epoch_time
                print "serviceInstanceName : " + str(serviceInstanceName)
                # To avoid 429 HTTP server error, we have to add a sleep between http requests
                time.sleep(4)
                print 111
                orderNumber, passed = self.api_client.createOrder(orderURL, serviceInstanceName, provider, i + 1)
                print 2222
                print orderNumber
                print 3333
                print passed
                time.sleep(4)
                if passed:
                    print "Approving order: " + str(orderNumber)
                    print 444
                    passed = self.api_client.approveOrder(orderNumber)
                    print 555
                if not passed:
                    responseBody = "Failure to create order"
                    print "Softlayer order creation failed. Approve will be skipped"
                    test_case_result.add_failure_info("Input " + str(i + 1) + " failed", responseBody)
                    break
        except:
            print "An Error Occured"
            passed=False
        status['APITest'] = passed
        return passed, test_case_result