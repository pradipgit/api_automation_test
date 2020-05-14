import time
import datetime
import utils
from utils import assignOrder
from utils import assertEqual
import random
import logging
import configparser
import json
import sys
import os
import string
import requests
import urllib
import urllib.parse
import operator
from junit_xml import TestCase
from io import BytesIO

requests.packages.urllib3.disable_warnings()

global status, assetURL, operationURL, orderNumber, service_id, resource_id, accessoperationURL,serviceInstanceName, inventoryheaders
status = {}
orderNumber = "notfound"

logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()

config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
neg_tests_soi_delete_sid = config.get('resources', 'neg_tests_soi_delete_sid')
# service_id = config.get('resources', 'service_id1')
# resource_id = config.get('resources', 'resource_id1')
# service_id2 = config.get('resources', 'service_id2')
# resource_id2 = config.get('resources', 'resource_id2')
# service_id3 = config.get('resources', 'service_id3')
# resource_id3 = config.get('resources', 'resource_id3')
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
componentURL = config.get('urls', 'componentURL')
order_historyURL = config.get('urls', 'order_historyURL')


provider = "aws"
resource_id=""
service_id=""

class Amazon_Tests(object):
    def __init__(self,client):
        self.api_client = client

    @assignOrder(1)
    def AMAZON_Create_Order(self):
        global service_id, resource_id
        passed = False
        service_id, resource_id = self.api_client.getResourcetoRunTest("aws", "buyer", "CORE-X")
        # service_id, resource_id = self.api_client.getResourcetoRunTest("aws","buyer", teamName="mTeam")
        # service_id, resource_id = self.api_client.createAndApproveOrder(headers, "AMAZON", "buyer", teamName_buyer)
        print("service id :: " + str(service_id))
        print("resource id :: " + str(resource_id))
        if (service_id != "" or resource_id != ""):
            resource_id = urllib.parse.quote(resource_id, safe='')
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(2)
    def AMAZON_On_Edit_SOI_Request_status(self):
        global service_id
        passed = False
        url = EditSOI_URL + service_id
        body = {
            "actionCode": "notifyOperationFailure",
            "editOrderID": "",
            "sender": "",
            "error": "random failure"
        }
        resp, body, roundtrip = self.api_client.post_New_Operation(url, body)
        print (resp)
        logger.info("API response:" + str(resp))
        print (body)
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        else:
            passed = False
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(3)
    def AMAZON_On_Edit_SOI_valid_data_status(self):
        global service_id
        passed = False
        url = EditSOI_URL + service_id
        resp, body, roundtrip = self.api_client.get_response_data(url + "/status")
        print (resp)
        logger.info("API response:" + str(resp))
        print (body)
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(4)
    def AMAZON_view_properties_responsetime(self):
        global service_id
        passed = False
        print ("Expected Response Time : " + ResponseTime)
        resp, body, roundtrip = self.api_client.get_api_response_time(viewPropertyURL + "/" + provider + "/" + service_id + "/properties")
        print (resp)
        # print body
        logger.info("API response:" + str(resp))
        if (int(roundtrip) <= int(ResponseTime)):
            passed = True
        else:
            print ("Response time is more")
            passed = False
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(5)
    def AMAZON_view_properties_validate_responsedata(self):
        global service_id
        passed = False
        resp, body, roundtrip = self.api_client.get_all_tags_data(viewPropertyURL + "/" + provider + "/" + service_id + "/properties")
        print (resp)
        logger.info("API response:" + str(resp))
        # print body
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
            # passed = self.api_client.verify_View_Properties_response_data(body, passed);
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(6)
    def AMAZON_Order_History__responsetime(self):
        global service_id
        passed = False
        print ("Expected Response Time : " + ResponseTime)
        url = order_historyURL + "/" + service_id
        resp, body, roundtrip = self.api_client.get_api_response_time(url)
        print (resp)
        logger.info("API response:" + str(resp))
        if (int(roundtrip) <= int(ResponseTime)):
            passed = True
        else:
            print ("Response time is more")
            passed = False
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(7)
    def AMAZON_Order_History_valid_data(self):
        global service_id
        passed = False
        url = order_historyURL + "/" + service_id
        resp, body, roundtrip = self.api_client.get_response_data(url)
        print (resp)
        logger.info("API response:" + str(resp))
        # print body
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(8)
    def AMAZON_Order_History_instances(self):
        global service_id
        passed = False
        url = order_historyURL + "/" + service_id
        resp, body = self.api_client.get_greenfiled_services(url)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    # @assignOrder(9)
    # def AMAZON_Get_operation_state_of_resource_responsetime(self):
    #     global service_id, resource_id
    #     passed = False
    #     print "Expected Response Time : " + ResponseTime
    #     resp, body, roundtrip = self.api_client.get_api_response_time(
    #         resourceStateURL + "/" + resource_id + "/state?provider_id=" + provider + "&SID=" + service_id)
    #     print resp
    #     # print body
    #     logger.info("API response:" + str(resp))
    #     if (int(roundtrip) == int(ResponseTime)):
    #         passed = True
    #     else:
    #         print "Response time is more"
    #         passed = False
    #     status['CAM-APITest'] = passed
    #     return passed

    @assignOrder(10)
    def AMAZON_checkServiceFulfillmentId_serviceListingAPI(self):
        global service_id
        passed = False
        # config.read('testdata.conf')
        # sid = config.get('resources', 'service_id1')
        url = 'api/services?page=1&size=1&searchText=' + service_id
        print (url)
        resp, body, roundtrip = self.api_client.get_api_response_time(url)
        print (resp)
        # print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            print (body["docs"])
            if body["total_count"] > 0:
                if "serviceFulfillmentId" in body["docs"][0]:
                    if (body["docs"][0]["serviceFulfillmentId"] is not None):
                        passed = True
                else:
                    print ("serviceFulfillmentId not Found in response body")
                    passed = False
            else:
                print ("No records found in body['docs']")
                passed = False
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(11)
    def AMAZON_checkServiceFulfillmentId_viewPropertiesAPI(self):
        global service_id
        passed = False
        # config.read('testdata.conf')
        # sid = config.get('resources', 'service_id1')
        url = viewPropertyURL + '/' + provider + '/' + service_id + '/properties'
        print (url)
        resp, body, roundtrip = self.api_client.get_api_response_time(url)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            if (body["serviceFulfillmentId"] is not None):
                passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(12)
    def AMAZON_Create_New_Operation_Execution_Request_responsetime(self):
        global service_id, resource_id
        passed = False
        print ("Expected Response Time : " + ResponseTime)
        body = {
            "providerid": provider,
            "description": "reboot",
            "action": "reboot",
            "resourceId": [resource_id],
            "SID": service_id
        }
        resp, body, roundtrip = self.api_client.post_New_Operation(operationURL, body)
        print ("Actual Response Time : " + str(ResponseTime))
        print (resp)
        print (body)
        logger.info("API response:" + str(resp))
        if (int(roundtrip) <= int(ResponseTime)):
            passed = True
        else:
            print ("Response time is more")
            passed = False
        status['CAM-APITest'] = passed
        return passed

    # @assignOrder(13)
    # def AMAZON_Create_New_Operation_Execution_Reboot_valid_data(self):
    #     global service_id, resource_id
    #     passed = False
    #     alreadyOff = False
    #     turningOnState = False
    #     onState = False
    #     resp, body, roundtrip = self.api_client.get_api_response_time(
    #         resourceStateURL + "/" + resource_id + "/state?provider_id=" + provider + "&SID=" + service_id)
    #     if (str(body).find("current_status") > -1):
    #         print (body["current_status"])
    #         if str(body["current_status"]).find("Off") > -1:
    #             print (("Resource in 'Off' state. Reboot not possible. So skipping this test"))
    #             passed = True
    #             alreadyOff = True
    #         else:
    #             print (("The current state of resource is : " + str(body["current_status"])))
    #             print (("Proceeding to Reboot the resource : " + resource_id))
    #     if not alreadyOff:
    #         body = {
    #             "providerid": provider,
    #             "description": "Rebooting",
    #             "action": "reboot",
    #             "resourceId": [resource_id],
    #             "SID": service_id
    #         }
    #         resp, body, roundtrip = self.api_client.post_New_Operation(operationURL, body)
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         print (body)
    #         passOfResponseCode = assertEqual(resp, 200)
    #         if (passOfResponseCode):
    #             if (passOfResponseCode):
    #                 for i in range(0, 30):
    #                     resp, body, roundtrip = self.api_client.get_api_response_time(
    #                         resourceStateURL + "/" + resource_id + "/state?provider_id=" + provider + "&SID=" + service_id)
    #                     if (str(body).find("current_status") > -1):
    #                         print (body["current_status"])
    #                         if str(body["current_status"]).find("Rebooting") > -1:
    #                             turningOnState = True
    #                             print (("Resource Status : (expected - Rebooting) : " + str(body["current_status"])))
    #                             for i in range(0, 30):
    #                                 print ("Waiting for Resource state to be 'On' ")
    #                                 resp, body, roundtrip = self.api_client.get_api_response_time(
    #                                     resourceStateURL + "/" + resource_id + "/state?provider_id=" + provider + "&SID=" + service_id)
    #                                 if str(body["current_status"]) == "On":
    #                                     print ((
    #                                             "Resource Status : (expected - On) : " + str(body["current_status"])))
    #                                     onState = True
    #
    #                                 if onState:
    #                                     break
    #                                 time.sleep(1)
    #                         else:
    #                             print ("Resource state is still " + str(body["current_status"]))
    #                             print (body)
    #                     else:
    #                         print (body)
    #                     if turningOnState and onState:
    #                         print ("Resource went to Rebooting and then to On state as expected")
    #                         passed = True
    #                         break
    #                     time.sleep(1)
    #             else:
    #                 passed = False
    #
    #     status['CAM-APITest'] = passed
    #     return passed
    #
    # @assignOrder(14)
    # def AMAZON_Create_New_Operation_Execution_Off_valid_data(self):
    #     global service_id, resource_id
    #     passed = False
    #     alreadyOff = False
    #     turningOffState = False
    #     offState = False
    #     resp, body, roundtrip = self.api_client.get_api_response_time(
    #         resourceStateURL + "/" + resource_id + "/state?provider_id=" + provider + "&SID=" + service_id)
    #     if str(body).find("current_status") > -1:
    #         print (body["current_status"])
    #         if str(body["current_status"]).find("Off") > -1:
    #             print ("Resource already in 'Off' state. So skipping this test")
    #             passed = True
    #             alreadyOff = True
    #         else:
    #             print ("The current state of resource is : " + str(body["current_status"]))
    #             print ("Proceeding to Turn OFF the resource : " + resource_id)
    #
    #     if not alreadyOff:
    #         body = {
    #             "providerid": provider,
    #             "description": "Turning Off",
    #             "action": "powerOff",
    #             "resourceId": [resource_id],
    #             "SID": service_id
    #         }
    #         print (body)
    #         resp, body, roundtrip = self.api_client.post_New_Operation(operationURL, body)
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         print (body)
    #         passOfResponseCode = assertEqual(resp, 200)
    #         if (passOfResponseCode):
    #             for i in range(0, 30):
    #                 resp, body, roundtrip = self.api_client.get_api_response_time(
    #                     resourceStateURL + "/" + resource_id + "/state?provider_id=" + provider + "&SID=" + service_id)
    #                 if str(body).find("current_status") > -1:
    #                     print (body["current_status"])
    #                     if str(body["current_status"]).find("TurningOff") > -1:
    #                         turningOffState = True
    #                         print ("Resource Status : (expected - TurningOff) : " + str(body["current_status"]))
    #                         for i in range(0, 30):
    #                             print ("Waiting for Resource state to be 'Off' ")
    #                             resp, body, roundtrip = self.api_client.get_api_response_time(
    #                                 resourceStateURL + "/" + resource_id + "/state?provider_id=" + provider + "&SID=" + service_id)
    #                             if str(body["current_status"]) == "Off":
    #                                 print ("Resource Status : (expected - Off) : " + str(body["current_status"]))
    #                                 offState = True
    #
    #                             if offState:
    #                                 break
    #                             time.sleep(1)
    #                     else:
    #                         print ("Resource state is still " + str(body["current_status"]))
    #                         print (body)
    #                 else:
    #                     print (body)
    #                 if turningOffState and offState:
    #                     print ("Resource went to TurningOff and then to Off state as expected")
    #                     passed = True
    #                     break
    #                 time.sleep(1)
    #         else:
    #             passed = False
    #     status['CAM-APITest'] = passed
    #     return passed

    # @assignOrder(15)
    # def AMAZON_Create_New_Operation_Execution_On_valid_data(self):
    #     global service_id, resource_id
    #     passed = False
    #     alreadyOn = False
    #     turningOnState = False
    #     onState = False
    #     resp, body, roundtrip = self.api_client.get_api_response_time(
    #         resourceStateURL + "/" + resource_id + "state?provider_id=" + provider + "&SID=" + service_id)
    #     if (str(body).find("current_status") > -1):
    #         print (body["current_status"])
    #         if str(body["current_status"]).find("On") > -1:
    #             print ("Resource already in 'On' state. So skipping this test")
    #             passed = True
    #             alreadyOn = True
    #         else:
    #             print ("The current state of resource is : " + str(body["current_status"]))
    #             print ("Proceeding to Turn ON the resource : " + resource_id)
    #
    #     if not alreadyOn:
    #         body = {
    #             "providerid": provider,
    #             "description": "Turning On",
    #             "action": "powerOn",
    #             "resourceId": [resource_id],
    #             "SID": service_id
    #         }
    #         print (body)
    #         resp, body, roundtrip = self.api_client.post_New_Operation(operationURL, body)
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         print (body)
    #         come_out = 0
    #         passOfResponseCode = assertEqual(resp, 200)
    #         if (passOfResponseCode):
    #             for i in range(0, 30):
    #                 resp, body, roundtrip = self.api_client.get_api_response_time(
    #                     resourceStateURL + "/" + resource_id + "state?provider_id=" + provider + "&SID=" + service_id)
    #                 if (str(body).find("current_status") > -1):
    #                     print (body["current_status"])
    #                     if str(body["current_status"]).find("TurningOn") > -1:
    #                         turningOnState = True
    #                         print ("Resource Status : (expected - TurningOn) : " + str(body["current_status"]))
    #                         for i in range(0, 30):
    #                             print ("Waiting for Resource state to be 'On' ")
    #                             resp, body, roundtrip = self.api_client.get_api_response_time(
    #                                 resourceStateURL + "/" + resource_id + "state?provider_id=" + provider + "&SID=" + service_id)
    #                             if str(body["current_status"]) == "On":
    #                                 print ("Resource Status : (expected - On) : " + str(body["current_status"]))
    #                                 onState = True
    #
    #                             if onState:
    #                                 break
    #                             time.sleep(1)
    #                     else:
    #                         print ("Resource state is still " + str(body["current_status"]))
    #                         print (body)
    #                 else:
    #                     print (body)
    #                 if turningOnState and onState:
    #                     print ("Resource went to TurningOn and then to On state as expected")
    #                     passed = True
    #                     break
    #                 time.sleep(1)
    #         else:
    #             passed = False
    #     status['CAM-APITest'] = passed
    #     return passed

    @assignOrder(16)
    def AMAZON_Get_operation_state_of_operation_responsetime(self):
        global resource_id
        passed = False
        print ("Expected Response Time : " + ResponseTime)
        resp, body, roundtrip = self.api_client.get_api_response_time(operationURL + "/" + resource_id + "/status")
        print (resp)
        print (body)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (int(roundtrip) <= int(ResponseTime)):
            passed = True
        else:
            print ("Response time is more")
            passed = False
        status['CAM-APITest'] = passed
        return passed

    # @assignOrder(17)
    # def AMAZON_Get_operation_state_of_resource_valid_data(self):
    #     global service_id, resource_id
    #     passed = False
    #     resp, body, roundtrip = self.api_client.get_api_response_time(
    #         resourceStateURL + "/" + resource_id + "state?provider_id=" + provider + "&SID=" + service_id)
    #     print (resp)
    #     logger.info("API response:" + str(resp))
    #     print (body)
    #     passOfResponseCode = assertEqual(resp, 200)
    #     if (passOfResponseCode):
    #         passed = True
    #     status['CAM-APITest'] = passed
    #     return passed
    #
    # @assignOrder(18)
    # def AMAZON_Get_operation_state_of_operation_ValidateTags(self):
    #     global resource_id
    #     passed = False
    #     resp, body, roundtrip = self.api_client.get_all_tags_data(operationURL + "/" + resource_id + "status")
    #     print(resp)
    #     print(body)
    #     logger.info("API response:" + str(resp))
    #     if (resp == 202):
    #         if (str(body).find("'actionStatus': 'UNKNOWN'") > -1 or str(body).find(
    #                 "'actionStatus': 'IN_PROGRESS'") > -1 or str(body).find(
    #             "'actionStatus': 'INITIATED'")):
    #             passed = True
    #     elif (resp == 200):
    #         if (str(body).find("'actionStatus': 'SUCCESS'") > -1 or str(body).find(
    #                 "'actionStatus': 'FAILED'")):
    #             passed = True
    #     status['CAM-APITest'] = passed
    #     return passed

    @assignOrder(27)
    def AMAZON_API_SOI_Delete_Request_responsetime(self):
        passed = False
        print ("Expected Response Time : " + ResponseTime)
        body = {
            "SIDs": [neg_tests_soi_delete_sid],
            "action": "delete",
            "description": "Delete Service"
        }
        print (body)
        resp, body, roundtrip = self.api_client.post_response_data(deleteURL, body)
        print (resp)
        print (body)
        logger.info("API response:" + str(resp))
        if (int(roundtrip) <= int(ResponseTime)):
            passed = True
        else:
            print ("Response time is more")
            passed = False
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(28)
    def AMAZON_List_Service_Details_By_ServiceId_responsetime(self):
        global service_id
        passed = False
        print ("Expected Response Time : " + ResponseTime)
        resp, body, roundtrip = self.api_client.get_api_response_time(componentURL + "/" + provider + "/" + service_id)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(29)
    def AMAZON_List_Service_Details_By_ServiceId_valid_data(self):
        global service_id
        passed = False
        resp, body, roundtrip = self.api_client.get_all_tags_data(
            componentURL + "/" + provider + "/" + service_id)
        print (resp)
        logger.info("API response:" + str(resp))
        print (body)
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
            # passed = self.api_client.verify_List_Service_Details_By_ServiceId_response_data(body, passed)
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(30)
    def AMAZON_API_OperationRegistryList_By_ServiceId_responsetime(self):
        global service_id
        passed = False
        print ("Expected Response Time : " + ResponseTime)
        resp, body, roundtrip = self.api_client.get_api_response_time(
            componentURL + "/" + provider + "/" + service_id)
        print (resp)
        logger.info("API response:" + str(resp))
        print (body)
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(31)
    def AMAZON_API_OperationRegistryList_By_ServiceId_valid_data(self):
        global service_id
        passed = False
        resp, body, roundtrip = self.api_client.get_all_tags_data(
            componentURL + "/" + provider + "/" + service_id)
        print (resp)
        logger.info("API response:" + str(resp))
        print (body)
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
            # passed = self.api_client.verify_List_Service_Details_By_ServiceId_response_data(body, passed)
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(32)
    def AMAZON_List_Service_Details_By_ServiceId_responsetime(self):
        global service_id
        passed = False
        print ("Expected Response Time : " + ResponseTime)
        resp, body, roundtrip = self.api_client.get_api_response_time(
            componentURL + "/" + provider + "/" + service_id)
        print (resp)
        logger.info("API response:" + str(resp))
        print (body)
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(33)
    def AMAZON_SOI_Delete_valid_data_singleSID(self):
        global start_time, orderNumber
        start_time = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        global service_id
        passed = False
        if service_id == "":
            return passed
        body = {
            'SIDs': [service_id],
            'action': 'delete',
            'description': 'Delete Service'
        }
        resp, body, roundtrip = self.api_client.post_response_data(deleteURL, body)
        print (resp)
        print (body)
        orderNumber = body[service_id][1]
        passOfResponseCode = assertEqual(resp, 202)
        if (passOfResponseCode):
            passed = True
        time.sleep(10);
        self.api_client.approveOrder_v2(orderNumber)
        status['CAM-APITest'] = passed
        return passed

    # # @assignOrder(34)
    # # def AMAZON_DeleteV2_Audit_Logging(self):
    # #     passed = False
    # #     global service_id, orderNumber
    # #     print ("Checking Audit log for SOI Delete V2 service...")
    # #     # print(start_time)
    # #     time.sleep(5);
    # #     # end_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    # #     end_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # #     print (end_time)
    # #     messageType = "SOI_DELETE"
    # #     audit_URL = "core/audit/api/v2.1/logs?component=[]&subcomponent=[]&userId=[]&teamId=[]&startDate=" + start_time + "&searchType=advanced&messageType=['" + messageType + "']&limit=10&page=1&endDate=" + end_time
    # #     resp, body_audit, roundtrip = self.api_client.get_response_data(audit_URL)
    # #     print (resp)
    # #     print (body_audit)
    # #     passOfResponseCode = assertEqual(resp, 200)
    # #     if (passOfResponseCode):
    # #         if (str(body_audit).find("Error while retrieving audit log message") <= -1):
    # #             if (body_audit["total_rows"] != 0):
    # #                 i = 0;
    # #                 for i in range(body_audit["total_rows"]):
    # #                     if str(body_audit["result"][i]["message"]).find(orderNumber) > -1 and str(
    # #                             body_audit["result"][i]["message"]).find(
    # #                             '[Deletion of service with SID: [' + service_id + ']from service inventory has been initiated') > -1:
    # #                         passed = True
    # #                         break
    # #                 else:
    # #                     print ("Audit record number : " + str(i))
    # #             else:
    # #                 print ("No audit log generated")
    # #         else:
    # #             print ("Error while retrieving audit log message")
    # #     else:
    # #         print ("Audit Request failed")
    # #     status['CAM-APITest'] = passed
    # #     return passed
    #
