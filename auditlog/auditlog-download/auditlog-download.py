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

user_name = config.get('params', 'username')
global headersUser1

x = random.randint(0, 50000)
global id_cred,metadata,audit_log_download_id
id_cred={}
metadata={}
audit_log_download_id={}

class AuditLogDownload(object):
    def __init__(self,client):
        global headersUser1
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)
        headersUser1 = {
            "Username": user_name,
            "Content-Type": "application/json"
        }


########################### CORE-1915 ##########################

    # @assignOrder(205)
    # def CORE1915_downloadAuditLogJSON(self):
    #     passed = False
    #     body = 	{
    #             "format": "json",
    #             "secret": "Test123!",
    #             "searchType": "keyword",
    #             "searchText": "cloud",
    #             "messageType": "[]",
    #             "component": "[]",
    #             "subcomponent": "[]",
    #             "userId": "[]",
    #             "teamId": "[]",
    #             "sort": "asc",
    #             "sortBy": "userId"
    #             };
    #     try:
    #         resp, body = self.api_client.downloadAuditLog(body)
    #         print (resp)
    #         print body
    #         data = json.dumps(body)
    #         data = json.loads(data)
    #         print data
    #         audit_log_download_id[0] = data['job_id']
    #     except Exception:
    #         audit_log_download_id[0]=0
    #         passed=False
    #         status['CAM-APITest'] = passed
    #         return passed
    #
    #     logger.info("API response:" + str(resp))
    #     passOfResponseCode = assertEqual(resp, 200)
    #     if (passOfResponseCode):
    #         passed = True
    #     status['CAM-APITest'] = passed
    #     return passed
    #
    # @assignOrder(206)
    # def CORE1915_downloadAuditLogLocalSystemValidId(self):
    #     passed = False
    #     resp, body = self.api_client.downloadAuditLogLocal(audit_log_download_id[0])
    #     print (resp)
    #     logger.info("API response:" + str(resp))
    #     passOfResponseCode = assertEqual(resp, 200)
    #     if (passOfResponseCode):
    #         passed = True
    #     status['CAM-APITest'] = passed
    #     return passed

    @assignOrder(370)
    def CORE1915_downloadAuditLogJSONAllParam(self):
        passed = False
        body = {
                "format": "json",
                "secret": "Test123!",
                "searchType": "advanced",
				"startDate": "2017-01-01T01:00:00.000Z",
				"endDate": "2018-06-01T12:00:00.000Z",
                "messageType": "['Search']",
                "component": "['comp']",
                "subcomponent": "['sub']",
                "userId": "['system']",
                "teamId": "['default']",
                "sort": "asc",
                "sortBy": "userId"
                };
        resp, body = self.api_client.downloadAuditLog(body)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(371)
    def CORE1915_downloadAuditLogLocalSystemInValidId(self):
        passed = False
        resp, body = self.api_client.downloadAuditLogLocal(3434)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 500)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(372)
    def CORE1915_downloadAuditLogCSV(self):
        passed = False
        body = 	{
                "format": "csv",
                "secret": "Test123!",
                "searchType": "advanced",
				"startDate": "2018-01-01T01:00:00.000Z",
				"endDate": "2018-06-01T12:00:00.000Z",
                "messageType": "['Search']",
                "component": "['']",
                "subcomponent": "['']",
                "userId": "['system']",
                "teamId": "['default']",
                "sort": "asc",
                "sortBy": "userId"
                };
        resp, body = self.api_client.downloadAuditLog(body)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(373)
    def CORE1915_downloadAuditLogCSVNoPassword(self):
        passed = False
        body = {
                "searchType": "advanced",
				"startDate": "2018-01-01T01:00:00.000Z",
				"endDate": "2018-06-01T12:00:00.000Z",
                "messageType": "['Search']",
                "component": "['comp']",
                "subcomponent": "['sub']",
                "userId": "['system']",
                "teamId": "['default']",
                "sort": "asc",
                "sortBy": "userId"
                };
        resp, body = self.api_client.downloadAuditLog(body)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 400)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(374)
    def CORE1915_downloadAuditLogNoformat(self):
        passed = False
        body = 	{
                "secret": "Test123!",
                "searchType": "advanced",
				"startDate": "2018-01-01T01:00:00.000Z",
				"endDate": "2018-06-01T12:00:00.000Z",
                "messageType": "['Search']",
                "component": "['comp']",
                "subcomponent": "['sub']",
                "userId": "['system']",
                "teamId": "['default']",
                "sort": "asc",
                "sortBy": "userId"
                };
        resp, body = self.api_client.downloadAuditLog(body)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 400)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(375)
    def CORE1915_downloadAuditLogWrongFormat(self):
        passed = False
        body = 	{
                "format": "xyz",
                "secret": "Test123!",
                "searchType": "advanced",
				"startDate": "2018-01-01T01:00:00.000Z",
				"endDate": "2018-06-01T12:00:00.000Z",
                "messageType": "['Search']",
                "component": "['comp']",
                "subcomponent": "['sub']",
                "userId": "['system']",
                "teamId": "['default']",
                "sort": "asc",
                "sortBy": "userId"
                };
        resp, body = self.api_client.downloadAuditLog(body)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 400)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(376)
    def CORE1915_downloadAuditLogBasicSearch(self):
        passed = False
        body = 	{
                "format": "json",
                "secret": "Test123!",
                "searchType": "basic",
				"startDate": "2018-01-01T01:00:00.000Z",
				"endDate": "2018-06-01T12:00:00.000Z",
                "messageType": "[]",
                "component": "[]",
                "subcomponent": "[]",
                "userId": "[]",
                "teamId": "[]",
                "sort": "asc",
                "sortBy": "userId"
                };
        resp, body = self.api_client.downloadAuditLog(body)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(377)
    def CORE1915_downloadAuditLogBasicSearchNoDates(self):
        passed = False
        body = {
                "format": "json",
                "secret": "Test123!",
                "searchType": "basic",
			    "messageType": "[]",
                "component": "[]",
                "subcomponent": "[]",
                "userId": "[]",
                "teamId": "[]",
                "sort": "asc",
                "sortBy": "userId"
                };
        resp, body = self.api_client.downloadAuditLog(body)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 400)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(378)
    def CORE1915_downloadAuditLogKeywordSearch(self):
        try:
            passed = False
            body = {
                    "format": "json",
                    "secret": "Test123!",
                    "searchType": "keyword",
                    "searchText": "cloud",
                    "startDate": "",
                    "endDate": "",
                    "messageType": "[]",
                    "component": "[]",
                    "subcomponent": "[]",
                    "userId": "[]",
                    "teamId": "[]",
                    "sort": "asc",
                    "sortBy": "userId"
                    };
            resp, body = self.api_client.downloadAuditLog(body)
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

    @assignOrder(379)
    def CORE1915_downloadAuditLogNoKeyword(self):
        try:
            passed = False
            body = {
                    "format": "json",
                    "secret": "Test123!",
                    "searchType": "keyword",
                    "searchText": "",
                    "startDate": "",
                    "endDate": "",
                    "messageType": "[]",
                    "component": "[]",
                    "subcomponent": "[]",
                    "userId": "[]",
                    "teamId": "[]",
                    "sort": "asc",
                    "sortBy": "userId"
                    };
            resp, body = self.api_client.downloadAuditLog(body)
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

    @assignOrder(380)
    def CORE1915_downloadAuditLogOnlyDates(self):
        try:
            passed = False
            body = {
                    "format": "json",
                    "secret": "Test123!",
                    "searchType": "advanced",
                    "startDate": "2018-01-01T01:00:00.000Z",
                    "endDate": "2018-06-01T12:00:00.000Z",
                    "messageType": "[]",
                    "component": "[]",
                    "subcomponent": "[]",
                    "userId": "[]",
                    "teamId": "[]",
                    "sort": "asc",
                    "sortBy": "userId"
                    };
            resp, body = self.api_client.downloadAuditLog(body)
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

    @assignOrder(381)
    def CORE1915_downloadAuditLogOnlyActionType(self):
        try:
            passed = False
            body = {
                    "format": "json",
                    "secret": "Test123!",
                    "searchType": "advanced",
                    "startDate": "",
                    "endDate": "",
                    "messageType": "['UPDATE ROLE']",
                    "component": "[]",
                    "subcomponent": "[]",
                    "userId": "[]",
                    "teamId": "[]",
                    "sort": "asc",
                    "sortBy": "userId"
                    };
            resp, body = self.api_client.downloadAuditLog(body)
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

    @assignOrder(382)
    def CORE1915_downloadAuditLogOnlyComponent(self):
        try:
            passed = False
            body = {
                    "format": "json",
                    "secret": "Test123!",
                    "searchType": "advanced",
                    "startDate": "",
                    "endDate": "",
                    "messageType": "[]",
                    "component": "['component']",
                    "subcomponent": "[]",
                    "userId": "[]",
                    "teamId": "[]",
                    "sort": "asc",
                    "sortBy": "userId"
                    };
            resp, body = self.api_client.downloadAuditLog(body)
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

    @assignOrder(383)
    def CORE1915_downloadAuditLogOnlySubComponent(self):
        try:
            passed = False
            body = {
                    "format": "json",
                    "secret": "Test123!",
                    "searchType": "advanced",
                    "startDate": "",
                    "endDate": "",
                    "messageType": "[]",
                    "component": "[]",
                    "subcomponent": "['subcomponent']",
                    "userId": "[]",
                    "teamId": "[]",
                    "sort": "asc",
                    "sortBy": "userId"
                    };
            resp, body = self.api_client.downloadAuditLog(body)
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

    @assignOrder(384)
    def CORE1915_downloadAuditLogOnlyUser(self):
        try:
            passed = False
            body = {
                    "format": "json",
                    "secret": "Test123!",
                    "searchType": "advanced",
                    "startDate": "",
                    "endDate": "",
                    "messageType": "[]",
                    "component": "[]",
                    "subcomponent": "[]",
                    "userId": "[user_name]",
                    "teamId": "[]",
                    "sort": "asc",
                    "sortBy": "userId"
                    };
            resp, body = self.api_client.downloadAuditLog(body)
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

    @assignOrder(385)
    def CORE1915_downloadAuditLogOnlyTeam(self):
        passed = False
        body = {
                "format": "json",
                "secret": "Test123!",
                "searchType": "advanced",
				"startDate": "",
				"endDate": "",
                "messageType": "[]",
                "component": "[]",
                "subcomponent": "[]",
                "userId": "[]",
                "teamId": "['TEAM1']",
                "sort": "asc",
                "sortBy": "userId"
                };
        resp, body = self.api_client.downloadAuditLog(body)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    # @assignOrder(223)
    # def downloadAuditLogOnlyDetails(self):
    #     passed = False
    #     body = {
    #         "format": "json",
    #         "secret": "Test1234!",
    #         "searchType": "advanced",
    #         "startDate": "",
    #         "endDate": "",
    #         "actionType": [],
    #         "component": [],
    #         "subComponent": [],
    #         "user": [],
    #         "userTeam": [],
    #         "details": "test"
    #     };
    #     resp, body = self.api_client.downloadAuditLog(body)
    #     print (resp)
    #     logger.info("API response:" + str(resp))
    #     passOfResponseCode = assertEqual(resp, 200)
    #     if (passOfResponseCode):
    #         passed = True
    #     status['CAM-APITest'] = passed
    #     return passed

    @assignOrder(386)
    def CORE1915_downloadAuditLogOnlyAdvanceSearchNoFilter(self):
        passed = False
        body = {
                "format": "json",
                "secret": "Test123!",
                "searchType": "advanced",
				"startDate": "",
				"endDate": "",
                "messageType": "[]",
                "component": "[]",
                "subcomponent": "[]",
                "userId": "[]",
                "teamId": "[]",
                "sort": "asc",
                "sortBy": "userId"
                };
        resp, body = self.api_client.downloadAuditLog(body)
        print (resp)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

    @assignOrder(387)
    def CORE1915_auditLogPaginationCheck(self):
        passed = False
        try:
            resp, body = self.api_client.keyWordSearch()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['total_rows'])
            record1 = data['total_rows']

            # change the limit to 25
            resp, body = self.api_client.keyWordSearchwithLimit25()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['total_rows'])
            record2 = data['total_rows']

            #change the pagination and move to next page
            resp, body = self.api_client.keyWordSearchwithLimit25_pagination()
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['total_rows'])
            record3 = data['total_rows']

            if(record1==record2 & record2==record3):
                    passed = True
                    status['CAM-APITest'] = passed
                    return passed
        except:
            status['CAM-APITest'] = False
            return False
