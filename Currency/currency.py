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
# from urllib2 import urlopen
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

class Currency(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)


#################CORE-2327##################
    # @assignOrder(482)
    # def CORE2327_defaultCurreny(self):
    #     passed = False
    #     body = {
    #         "configurationkey": "default_currency",
    #         "configurationvalue": "USD"
    #     };
    #     resp, body = self.api_client.postdefaultCurreny(body)
    #     print (resp)
    #     logger.info("API response:" + str(resp))
    #     passOfResponseCode = assertEqual(resp, 200)
    #     if (passOfResponseCode):
    #         passed = True
    #     status['CAM-APITest'] = passed
    #     return passed

    # @assignOrder(483)
    # def CORE2327_lockCurreny(self):
    #     try:
    #         passed = False
    #         body = {
    #             "configurationkey": "default_currency_status",
    #             "configurationvalue": "true"
    #         };
    #         resp, body = self.api_client.lockdefaultCurreny(body)
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         passOfResponseCode = assertEqual(resp, 200)
    #         if (passOfResponseCode):
    #             passed = True
    #         status['CAM-APITest'] = passed
    #         return passed
    #     except:
    #         status['CAM-APITest'] = False
    #         return False

    # @assignOrder(484)
    # def CORE2327_getLockStatus(self):
    #     try:
    #         passed = False
    #         resp, body = self.api_client.getCurrencyLockStatus()
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         passOfResponseCode = assertEqual(resp, 200)
    #         if (passOfResponseCode):
    #             passed = True
    #         status['CAM-APITest'] = passed
    #         return passed
    #     except:
    #         status['CAM-APITest'] = False
    #         return False

    @assignOrder(485)
    def CORE2327_getdefaultCurrency(self):
            try:
                passed = False
                resp, body = self.api_client.getdefaultCurrency()
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

    @assignOrder(486)
    def CORE2327_getAllConvertions(self):
            try:
                passed = False
                resp, body = self.api_client.getAllConvertion()
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

    @assignOrder(487)
    def CORE2327_Post_Delete_Future_DateConvertionRates(self):
            try:
                passed = False
                body = {
                    "currencyfrom": "EUR",
                    "currencyto": "USD",
                    "source": "default",
                    "startdate": "2139-02-07T18:25:43.511Z",
                    "enddate": "2139-03-07T18:25:43.511Z",
                    "exchangerate": "64.6",
                    "status": "ACTIVE"
                };
                resp, body1 = self.api_client.postConvertionRates(body)
                print (resp)
                logger.info("API response:" + str(resp))
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body1['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

                data = json.dumps(body1)
                data = json.loads(data)
                print (data['id'])
                resp, body = self.api_client.deleteConvertionRates(data['id'])
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

    @assignOrder(488)
    def CORE2605_getSupportedCurrencies(self):
            try:
                passed = False
                resp, body = self.api_client.getSupportedCurrencies()
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

    #     @assignOrder(489)
    # def CORE2327_postWithUnlockedStatus(self):
    #     try:
    #         passed = False
    #         body = {
    #             "configurationkey": "default_currency_status",
    #             "configurationvalue": "false"
    #         };
    #         resp, body = self.api_client.lockdefaultCurreny(body)
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         ######post convertion rate##############
    #         body = {
    #             "currencyfrom": "EUR",
    #             "currencyto": "USD",
    #             "source": "default",
    #             "startdate": "02/07/2020",
    #             "enddate": "03/07/2020",
    #             "exchangerate": "64.6"
    #         };
    #         resp, body = self.api_client.postConvertionRates(body)
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         passOfResponseCode = assertEqual(resp, 400)
    #         if (passOfResponseCode):
    #             passed = True
    #         status['CAM-APITest'] = passed
    #         body = {
    #             "configurationkey": "default_currency_status",
    #             "configurationvalue": "true"
    #         };
    #         resp, body = self.api_client.lockdefaultCurreny(body)
    #         print (resp)
    #         logger.info("API response:" + str(resp))
    #         return passed
    #     except:
    #         status['CAM-APITest'] = False
    #         return False

    @assignOrder(490)
    def CORE2327_Post_Invalid_ConvertionFormat(self):
        try:
            passed = False
            body = {
                "configurationkey": "default_currency_status",
                "configurationvalue": "true"
            };
            resp, body = self.api_client.lockdefaultCurreny(body)
            print (resp)
            logger.info("API response:" + str(resp))
            body = {
                    "currencyfrom": "EUR@@@",
                    "currencyto": "USD",
                    "source": "default",
                    "startdate": "2139-02-07T18:25:43.511Z",
                    "enddate": "2139-03-07T18:25:43.511Z",
                    "exchangerate": "64.6",
                     "status": "ACTIVE"
            };
            resp, body = self.api_client.postConvertionRates(body)
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


    @assignOrder(491)
    def CORE2327_Post_Delete_PresentDate_ConvertionRates(self):
        try:
            passed = False
            print ("Current date and time using str method of datetime object:")
            print (str(now))
            print ("Current year: %d" % now.year)
            print ("Current month: %d" % now.month)
            print ("Current day: %d" % now.day)
            day = len(str(now.day))
            if day < 2:
                day1 = "0" + str(now.day)
            else:
                day1 = str(now.day)

            month = len(str(now.month))
            if month < 2:
                month1 = "0" + str(now.month)
            else:
                month1 =  str(now.month)

            completeDate = str(now.year) + "-" + str(month1) + "-" + str(day1) + "T" + "18:25:43.511" + "Z"
            print (completeDate)
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            resp, body = self.api_client.deleteConvertionRates(data['id'])
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


    @assignOrder(492)
    def CORE2327_Post_Delete_PastDate_ConvertionRates(self):
        try:
            passed = False
            year = random.randint(1900, 1986)
            month = random.randint(10, 12)
            day = random.randint(10, 28)

            print ("Current year: %d" % year)
            print ("Current month: %d" % month)
            print ("Current day: %d" % day)

            completeDate = str(year) + "-" + str(month) + "-" + str(day) + "T" + "18:25:43.511" + "Z"

            print (completeDate)
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            resp, body = self.api_client.deleteConvertionRates(data['id'])
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


    @assignOrder(493)
    def CORE2327_update_FutureDate_ConvertionRates(self):
        try:
            passed = False
            year = random.randint(2500, 2600)
            month = random.randint(10, 12)
            day = random.randint(10, 28)
            print ("Current year: %d" % year)
            print ("Current month: %d" % month)
            print ("Current day: %d" % day)

            completeDate = str(year) + "-" + str(month) + "-" + str(day) + "T" + "18:25:43.511" + "Z"
            print (completeDate)
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2",
                "status": "ACTIVE"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            year = random.randint(2700, 4000)
            month = random.randint(10, 12)
            day = random.randint(11, 28)
            print ("Current year: %d" % year)
            print ("Current month: %d" % month)
            print ("Current day: %d" % day)
            newcompleteDate = str(year) + "-" + str(month) + "-" + str(day) + "T18:25:43.511Z"
            print (newcompleteDate)
            body = {
                "currencyfrom": "AUD",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": newcompleteDate,
                "exchangerate": "61.0",
                "status": "ACTIVE"
            };
            resp, body = self.api_client.update_convertionRates(body, data['id']);
            print (resp)
            logger.info("API response:" + str(resp))
            # Verify Update
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 200) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])
            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False



    @assignOrder(494)
    def CORE2327_update_PastDate_ConvertionRates(self):
        try:
            passed = False
            year = random.randint(1986, 2014)
            month = random.randint(10, 12)
            day = random.randint(11, 28)
            print ("Current year: %d" % year)
            print ("Current month: %d" % month)
            print ("Current day: %d" % day)
            completeDate = str(year) + "-" + str(month) + "-" + str(day) + "T18:25:43.511Z"
            print (completeDate)
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2",
                "status": "ACTIVE"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])

            year = random.randint(2020, 2040)
            month = random.randint(10, 12)
            day = random.randint(11, 28)
            print ("Current year: %d" % year)
            print ("Current month: %d" % month)
            print ("Current day: %d" % day)
            NewcompleteDate = str(year) + "-" + str(month) + "-" + str(day) + "T18:25:43.511Z"
            print (NewcompleteDate)

            body = {
                "currencyfrom": "AUD",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": NewcompleteDate,
                "exchangerate": "61.0",
                "status": "ACTIVE"
            };
            resp, body = self.api_client.update_convertionRates(body, data['id']);
            print (resp)
            logger.info("API response:" + str(resp))
            # Verify Update
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 200) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            if (passOfResponseCode):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(495)
    def CORE2327_update_CurrentDate_ConvertionRates(self):
        try:
            passed = False
            print ("Current date and time using str method of datetime object:")
            print (str(now))
            print ("Current year: %d" % now.year)
            print ("Current month: %d" % now.month)
            print ("Current day: %d" % now.day)
            day = len(str(now.day))
            if day < 2:
                day1 = "0" + str(now.day)
            else:
                day1 = str(now.day)

            month = len(str(now.month))
            if month < 2:
                month1 = "0" + str(now.month)
            else:
                month1 = str(now.month)
            completeDate = str(now.year) + "-" + str(month1) + "-" + str(day1) + "T" + "18:25:43.511" + "Z"
            print (completeDate)
            body = {
                "currencyfrom": "INR",
                "currencyto": "EUR",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2",
                "status": "ACTIVE"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])

            year = random.randint(2020, 2040)
            month = random.randint(10, 12)
            day = random.randint(11, 28)
            print ("Current year: %d" % year)
            print ("Current month: %d" % month)
            print ("Current day: %d" % day)
            NewcompleteDate = str(year) + "-" + str(month) + "-" + str(day) + "T18:25:43.511Z"
            print (NewcompleteDate)
            body = {
                "currencyfrom": "SEK",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": NewcompleteDate,
                "exchangerate": "61.0",
                "status": "ACTIVE"
            };
            resp, body = self.api_client.update_convertionRates(body, data['id']);
            print (resp)
            logger.info("API response:" + str(resp))
            # Verify Update
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 200) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            resp, body = self.api_client.deleteConvertionRates(data['id'])
            if (passOfResponseCode):
                passed = True
                print (resp)
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return False
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(496)
    def CORE2327_update_StartDate_ConvertionRates(self):
            try:
                passed = False
                print ("Current date and time using str method of datetime object:")
                print (str(now))
                print ("Current year: %d" % now.year)
                print ("Current month: %d" % now.month)
                print ("Current day: %d" % now.day)
                day = len(str(now.day))
                if day < 2:
                    day1 = "0" + str(now.day)
                else:
                    day1 = str(now.day)

                month = len(str(now.month))
                if month < 2:
                    month1 = "0" + str(now.month)
                else:
                    month1 = str(now.month)

                completeDate = str(now.year) + "-" + str(month1) + "-" + str(day1) + "T" + "18:25:43.511" + "Z"
                print (completeDate)
                body = {
                    "currencyfrom": "NZD",
                    "currencyto": "AUD",
                    "source": "default",
                    "startdate": completeDate,
                    "enddate": completeDate,
                    "exchangerate": "64.2",
                    "status": "ACTIVE"
                };
                resp, body = self.api_client.postConvertionRates(body)
                print (resp)
                logger.info("API response:" + str(resp))
                if resp == 409:
                    print ("Record Already Exist")
                    passOfResponseCode = assertEqual(resp, 409)
                    if (passOfResponseCode):
                        passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    # Verify POST
                    get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                    passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

                data = json.dumps(body)
                data = json.loads(data)
                print (data['id'])

                year = random.randint(2020, 2040)
                month = random.randint(10, 12)
                day = random.randint(11, 28)
                print ("Current year: %d" % year)
                print ("Current month: %d" % month)
                print ("Current day: %d" % day)
                NewcompleteDate = str(year) + "-" + str(month) + "-" + str(day) + "T18:25:43.511Z"
                print (NewcompleteDate)
                body = {
                    "currencyfrom": "SEK",
                    "currencyto": "USD",
                    "source": "default",
                    "startdate": NewcompleteDate,
                    "enddate": NewcompleteDate,
                    "exchangerate": "61.0",
                    "status": "ACTIVE"
                };
                resp, body = self.api_client.update_convertionRates(body, data['id']);
                print (resp)
                logger.info("API response:" + str(resp))
                # Verify Update
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 200) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

                resp, body = self.api_client.deleteConvertionRates(data['id'])
                print (resp)
                if (passOfResponseCode):
                    passed = True
                    print (resp)
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    status['CAM-APITest'] = False
                    return False
            except:
                status['CAM-APITest'] = False
                return False

            ##########################################CORE -3671 #######################3

    @assignOrder(497)
    def CORE3671_getConversionRateWithHistrory(self):
        try:
            passed = False
            resp, body = self.api_client.getConversionRatesWithHistory()
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

    @assignOrder(498)
    def CORE3671_getConversionRateWithoutHistrory(self):
        try:
            passed = False
            resp, body = self.api_client.getConversionRatesWithoutHistory()
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

    @assignOrder(499)
    def CORE3671_getConversionRateById(self):   #doubtful
        try:
            recordId=""
            passed = False
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": "2139-02-07T18:25:43.511Z",
                "enddate": "2139-03-07T18:25:43.511Z",
                "exchangerate": "64.6",
                "status": "ACTIVE"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response:" + str(resp))
            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            recordId = data['id']
            resp, body = self.api_client.getConversionRatesById(recordId)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            resp, body = self.api_client.deleteConvertionRates(recordId)
            return passed
        except:
            status['CAM-APITest'] = False
            resp, body = self.api_client.deleteConvertionRates(recordId)
            return False

    @assignOrder(500)
    def CORE3671_getConversionRateByInvalidID(self):
        try:
            passed = False
            resp, body = self.api_client.getConversionRatesById("TestDataCurrency123456")
            print (resp)
            logger.info("API response For GET:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(501)
    def CORE3671_deleteConversionRateByInvalidID(self):
        try:
            passed = False
            resp, body = self.api_client.deleteConvertionRates("338383838989")
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(502)
    def CORE3671_getAllConversionRate_DeletedStatus(self):
        try:
            passed = False
            resp, body = self.api_client.getConversionRates_DeletedStaus()
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

    @assignOrder(503)
    def CORE3671_getAllConversionRate_validStatus(self):
        try:
            passed = False
            resp, body = self.api_client.getConversionRates_validStaus()
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

    @assignOrder(504)
    def CORE3671_getConversionRate_MultipleParameter(self):     #doubtful
        try:
            passed = False
            body = {
                "currencyfrom": "NOK",
                "currencyto": "NZD",
                "source": "apiAutomationNewTest",
                "startdate": "2019-01-05T18:25:43.511Z",
                "enddate": "2019-01-08T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)

            print (data['id'])
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                passOfResponseCode = assertEqual(resp, 201)
            resp, body = self.api_client.getConversionRates_MultipleParamter('NOK','NZD','apiAutomationNewTest')
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(505)
    def CORE3671_getStatus_DeletedConversionRates(self):
        try:
            passed = False
            body = {
                "currencyfrom": "DKK",
                "currencyto": "GBP",
                "source": "default",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response For POST:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            logger.info("API response for Delete by ID:" + str(resp))
            resp, body = self.api_client.getConversionRatesById(data['id'])
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(506)
    def CORE3671_DeletedConversionRates_for_ZAR_BRL(self):
            try:
                passed = False
                body = {
                    "currencyfrom": "ZAR",
                    "currencyto": "BRL",
                    "source": "default",
                    "startdate": "2058-12-06T18:25:43.511Z",
                    "enddate": "2058-12-06T18:25:43.511Z",
                    "exchangerate": "64.2"
                };
                resp, body = self.api_client.postConvertionRates(body)
                print (resp)
                logger.info("API response For POST:" + str(resp))
                if resp == 409:
                    print ("Record Already Exist")
                    passOfResponseCode = assertEqual(resp, 409)
                    if (passOfResponseCode):
                        passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    # Verify POST
                    get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                    passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

                data = json.dumps(body)
                data = json.loads(data)
                print (data['id'])
                resp, body = self.api_client.deleteConvertionRates(data['id'])
                print (resp)
                logger.info("API response for Delete by ID:" + str(resp))
                resp, body = self.api_client.getConversionRatesById(data['id'])
                print (resp)
                logger.info("API response for Delete by ID:" + str(resp))
                resp, body = self.api_client.getConversionRatesById(data['id'])
                print (resp)
                logger.info("API response:" + str(resp))
                passOfResponseCode = assertEqual(resp, 404)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            except:
                status['CAM-APITest'] = False
                return False

    @assignOrder(507)
    def CORE3671_DeletedConversionRates_for_HKD_CAD(self):
        try:
            passed = False
            body = {
                "currencyfrom": "HKD",
                "currencyto": "CAD",
                "source": "default",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response For POST:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

                # passOfResponseCode = assertEqual(resp, 201)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            logger.info("API response for Delete by ID:" + str(resp))
            resp, body = self.api_client.getConversionRatesById(data['id'])
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(508)
    def CORE3671_DeletedConversionRates_for_CAD_CHF(self):
            try:
                passed = False
                body = {
                    "currencyfrom": "CAD",
                    "currencyto": "CHF",
                    "source": "default",
                    "startdate": "2058-12-06T18:25:43.511Z",
                    "enddate": "2058-12-06T18:25:43.511Z",
                    "exchangerate": "64.2"
                };
                resp, body = self.api_client.postConvertionRates(body)
                print (resp)
                logger.info("API response For POST:" + str(resp))
                if resp == 409:
                    print ("Record Already Exist")
                    passOfResponseCode = assertEqual(resp, 409)
                    if (passOfResponseCode):
                        passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    # Verify POST
                    get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                    passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

                data = json.dumps(body)
                data = json.loads(data)
                print (data['id'])
                resp, body = self.api_client.deleteConvertionRates(data['id'])
                print (resp)
                logger.info("API response for Delete by ID:" + str(resp))
                resp, body = self.api_client.getConversionRatesById(data['id'])
                print (resp)
                logger.info("API response:" + str(resp))
                passOfResponseCode = assertEqual(resp, 404)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            except:
                status['CAM-APITest'] = False
                return False

    @assignOrder(509)
    def CORE3671_DeletedConversionRates_for_ZAR_CHF(self):
        try:
            passed = False
            body = {
                "currencyfrom": "ZAR",
                "currencyto": "CHF",
                "source": "default",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response For POST:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            logger.info("API response for Delete by ID:" + str(resp))
            resp, body = self.api_client.getConversionRatesById(data['id'])
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(510)
    def CORE3671_DeletedConversionRates_for_ZAR_CAD(self):
            try:
                passed = False
                body = {
                    "currencyfrom": "ZAR",
                    "currencyto": "CAD",
                    "source": "default",
                    "startdate": "2058-12-06T18:25:43.511Z",
                    "enddate": "2058-12-06T18:25:43.511Z",
                    "exchangerate": "64.2"
                };
                resp, body = self.api_client.postConvertionRates(body)
                print (resp)
                logger.info("API response For POST:" + str(resp))
                if resp == 409:
                    print ("Record Already Exist")
                    passOfResponseCode = assertEqual(resp, 409)
                    if (passOfResponseCode):
                        passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    # Verify POST
                    get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                    passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

                data = json.dumps(body)
                data = json.loads(data)
                print (data['id'])
                resp, body = self.api_client.deleteConvertionRates(data['id'])
                print (resp)
                logger.info("API response for Delete by ID:" + str(resp))
                resp, body = self.api_client.getConversionRatesById(data['id'])
                print (resp)
                logger.info("API response:" + str(resp))
                passOfResponseCode = assertEqual(resp, 404)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            except:
                status['CAM-APITest'] = False
                return False

    @assignOrder(511)
    def CORE3671_DeletedConversionRates_for_BRL_CAD(self):
        try:
            passed = False
            body = {
                "currencyfrom": "BRL",
                "currencyto": "CAD",
                "source": "default",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response For POST:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            logger.info("API response for Delete by ID:" + str(resp))
            resp, body = self.api_client.getConversionRatesById(data['id'])
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(512)
    def CORE3671_DeletedConversionRates_for_BRL_CAD(self):
            try:
                passed = False
                body = {
                    "currencyfrom": "BRL",
                    "currencyto": "ZAR",
                    "source": "default",
                    "startdate": "2058-12-06T18:25:43.511Z",
                    "enddate": "2058-12-06T18:25:43.511Z",
                    "exchangerate": "64.2"
                };
                resp, body = self.api_client.postConvertionRates(body)
                print (resp)
                logger.info("API response For POST:" + str(resp))
                if resp == 409:
                    print ("Record Already Exist")
                    passOfResponseCode = assertEqual(resp, 409)
                    if (passOfResponseCode):
                        passed = True
                    status['CAM-APITest'] = passed
                    return passed
                else:
                    # Verify POST
                    get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                    passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

                data = json.dumps(body)
                data = json.loads(data)
                print (data['id'])
                resp, body = self.api_client.deleteConvertionRates(data['id'])
                print (resp)
                logger.info("API response for Delete by ID:" + str(resp))
                resp, body = self.api_client.getConversionRatesById(data['id'])
                print (resp)
                logger.info("API response:" + str(resp))
                passOfResponseCode = assertEqual(resp, 404)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            except:
                status['CAM-APITest'] = False
                return False

    @assignOrder(513)
    def CORE3671_DeletedConversionRates_for_CHF_CAD(self):
        try:
            passed = False
            body = {
                "currencyfrom": "CHF",
                "currencyto": "ZAR",
                "source": "default",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response For POST:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            logger.info("API response for Delete by ID:" + str(resp))
            resp, body = self.api_client.getConversionRatesById(data['id'])
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(514)
    def CORE3671_DeletedConversionRates_for_HKD_CAD(self):
        try:
            passed = False
            body = {
                "currencyfrom": "HKD",
                "currencyto": "ZAR",
                "source": "default",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response For POST:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            logger.info("API response for Delete by ID:" + str(resp))
            resp, body = self.api_client.getConversionRatesById(data['id'])
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 404)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(515)
    def CORE3671_OverWriteConversionRates_for_BRL_AUD(self):
        try:
            passed = False
            body = {
                "currencyfrom": "BRL",
                "currencyto": "AUD",
                "source": "default",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-10T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            logger.info("API response For POST:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                status['CAM-APITest'] = False
                return passed
            else:
                # Verify POST
                get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
                passOfResponseCode = assertEqual(resp, 200) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

                data = json.dumps(body)
                data = json.loads(data)
                print (data['id'])
                oldID = data['id']
                logger.info("ID1  is:" + str(oldID))

            #overwrite one more record
            body = {
                "currencyfrom": "BRL",
                "currencyto": "AUD",
                "source": "default",
                "startdate": "2058-12-05T18:25:43.511Z",
                "enddate": "2058-12-11T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            print ("Actual Code is :"+str(resp))
            print ("Expected Code is 409")
            logger.info("API response For POST:" + str(resp))

            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)

            if(passOfResponseCode):
                passed = True
            resp, body = self.api_client.deleteConvertionRates(oldID)
            print (resp)
            logger.info("Deleted The Record1:" + str(resp))
            print ("Deleted The Record1")
            status['CAM-APITest'] = passed
            return passed
        except:
            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            newId = data['id']
            logger.info("ID1  is:" + str(newId))
            resp, body = self.api_client.deleteConvertionRates(oldID)
            print (resp)
            print ("Deleted The Record1")
            resp, body = self.api_client.deleteConvertionRates(newId)
            print (resp)
            print ("Deleted The Record2")
            logger.info("Deleted The Record2:" + str(resp))
            status['CAM-APITest'] = False
            return False

    @assignOrder(516)
    def CORE3671_VerifyActiveAPI_DeletedRecords(self):
        try:
            passed = False

            body = {
                "currencyfrom": "HKD",
                "currencyto": "USD",
                "source": "default",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            generatedId=data['id']

            body = {
                "currencyfrom": "HKD",
                "currencyto": "USD",
                "source": "default11",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            # Verify POST
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            generatedId1 = data['id']

            body = {
                "currencyfrom": "HKD",
                "currencyto": "USD",
                "source": "default22",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            # Verify POST
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            generatedId2 = data['id']

            body = {
                "currencyfrom": "HKD",
                "currencyto": "USD",
                "source": "default33",
                "startdate": "2058-12-06T18:25:43.511Z",
                "enddate": "2058-12-06T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            # Verify POST
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            generatedId3 = data['id']



            #call the ACTIVE API
            resp, body = self.api_client.getConversionRates_validStaus()
            data = json.dumps(body)
            data = json.loads(data)
            print (data[0]['id'])
            currencyId=data[0]['id']


            # DELETE THE FIRST RECORD
            resp, body = self.api_client.deleteConvertionRates(data[0]['id'])
            print (resp)
            logger.info("API response for Delete by ID:" + str(resp))

            # call the ACTIVE API
            resp, body = self.api_client.getConversionRates_validStaus()
            data = json.dumps(body)
            data = json.loads(data)
            #Check whether id is not present on not

            i = 0
            latestCurrencyId = ""
            for currency in data:
                print (data[i]['id'])
                latestCurrencyId = data[i]['id']
                if latestCurrencyId == currencyId:
                    passed = False
                    status['CAM-APITest'] = False
                    # resp, body = self.api_client.deleteConvertionRates(generatedId)
                    print (resp)
                    break
                else:
                    passed = True
                    status['CAM-APITest'] = passed
                    i = i + 1

            resp, body = self.api_client.deleteConvertionRates(generatedId)
            print (resp)
            resp, body = self.api_client.deleteConvertionRates(generatedId1)
            print (resp)
            resp, body = self.api_client.deleteConvertionRates(generatedId2)
            print (resp)
            resp, body = self.api_client.deleteConvertionRates(generatedId3)
            print (resp)
            return passed

        except:
            status['CAM-APITest'] = False
            return False


    @assignOrder(517)
    def CORE3671_VerifyActiveWithHistoryAPI_DeletedRecords(self):
     try:
        passed = False

        # create and update the first record
        body = {
            "currencyfrom": "HKD",
            "currencyto": "USD",
            "source": "default",
            "startdate": "2058-12-06T18:25:43.511Z",
            "enddate": "2058-12-06T18:25:43.511Z",
            "exchangerate": "64.2"
        };
        resp, body = self.api_client.postConvertionRates(body)
        print (resp)
        # Verify POST
        get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
        passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

        data = json.dumps(body)
        data = json.loads(data)
        print (data['id'])
        generatedId = data['id']

        # update the Record
        body = {
            "currencyfrom": "HKD",
            "currencyto": "USD",
            "source": "default",
            "startdate": "2058-12-06T18:25:43.511Z",
            "enddate": "2058-12-06T18:25:43.511Z",
            "exchangerate": "64.3",
            "status": "ACTIVE"
        };
        resp, body = self.api_client.update_convertionRates(body, generatedId);
        print ("Response for Update is:" +str(resp))
        logger.info("API response for Response:" + str(resp))
        # Verify Update
        get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
        passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])


        # create and update the 2nd record

        body = {
            "currencyfrom": "HKD",
            "currencyto": "USD",
            "source": "default44",
            "startdate": "2058-12-06T18:25:43.511Z",
            "enddate": "2058-12-06T18:25:43.511Z",
            "exchangerate": "64.2"
        };
        resp, body = self.api_client.postConvertionRates(body)
        print (resp)
        # Verify POST
        get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
        passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

        data = json.dumps(body)
        data = json.loads(data)
        print (data['id'])
        generatedId2 = data['id']

        # update the Record
        body = {
            "currencyfrom": "HKD",
            "currencyto": "USD",
            "source": "default44",
            "startdate": "2058-12-06T18:25:43.511Z",
            "enddate": "2058-12-06T18:25:43.511Z",
            "exchangerate": "64.3",
            "status": "ACTIVE"
        };
        resp, body = self.api_client.update_convertionRates(body, generatedId);
        print ("Response for Update is:" + str(resp))
        logger.info("API response for Response:" + str(resp))
        # Verify Update
        get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
        passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])


        # create and update the 3rd record

        body = {
            "currencyfrom": "HKD",
            "currencyto": "USD",
            "source": "default55",
            "startdate": "2058-12-06T18:25:43.511Z",
            "enddate": "2058-12-06T18:25:43.511Z",
            "exchangerate": "64.2"
        };
        resp, body = self.api_client.postConvertionRates(body)
        print (resp)
        # Verify POST
        get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
        passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

        data = json.dumps(body)
        data = json.loads(data)
        print (data['id'])
        generatedId3 = data['id']

        # update the Record
        body = {
            "currencyfrom": "HKD",
            "currencyto": "USD",
            "source": "default55",
            "startdate": "2058-12-06T18:25:43.511Z",
            "enddate": "2058-12-06T18:25:43.511Z",
            "exchangerate": "64.3",
            "status": "ACTIVE"
        };
        resp, body = self.api_client.update_convertionRates(body, generatedId);
        print ("Response for Update is:" + str(resp))
        logger.info("API response for Response:" + str(resp))
        # Verify Update
        get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
        passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

        # call the ACTIVE API
        resp, body = self.api_client.getConversionRates_validStausWithHistory()
        data = json.dumps(body)
        data = json.loads(data)
        print (data[0]['id'])
        currencyId = data[0]['id']

        # DELETE THE FIRST RECORD
        resp, body = self.api_client.deleteConvertionRates(data[0]['id'])
        print (resp)
        logger.info("API response for Delete by ID:" + str(resp))

        # call the ACTIVE API
        resp, body = self.api_client.getConversionRates_validStaus()
        data = json.dumps(body)
        data = json.loads(data)
        # Check whether id is not present on not

        i = 0
        latestCurrencyId = ""
        for currency in data:
            print (data[i]['id'])
            latestCurrencyId = data[i]['id']
            if latestCurrencyId == currencyId:
                passed = False
                status['CAM-APITest'] = False
                print (resp)
                break
            else:
                passed = True
                status['CAM-APITest'] = passed
                i = i + 1

        resp, body = self.api_client.deleteConvertionRates(generatedId)
        print (resp)
        resp, body = self.api_client.deleteConvertionRates(generatedId2)
        print (resp)
        resp, body = self.api_client.deleteConvertionRates(generatedId3)
        print (resp)
        return passed

     except:
        status['CAM-APITest'] = False
        return False

    @assignOrder(518)
    def CORE3671_getCurrency_MultipleParameter_WithStartDate(self):
         try:
             passed = False

             body = {
                 "currencyfrom": "HKD",
                 "currencyto": "USD",
                 "source": "automationDateParameter",
                 "startdate": "2088-12-06T18:25:43.511Z",
                 "enddate": "2088-12-11T18:25:43.511Z",
                 "exchangerate": "64.2"
             };
             resp, body = self.api_client.postConvertionRates(body)
             print (resp)
             # Verify POST
             get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
             passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

             data = json.dumps(body)
             data = json.loads(data)
             print (data['id'])
             generatedId = data['id']

             # call the multiple parameter api
             resp, body = self.api_client.getConversionRates_multipleParameterwithDate('HKD','USD','automationDateParameter','2088-12-06T18:25:43.511Z')
             print (resp)

             data = json.dumps(body)
             data = json.loads(data)
             print (data[0]['id'])
             i = 0
             latestCurrencyId = ""
             for currency in data:
                     latestCurrencyId = data[i]['id']
                     print (latestCurrencyId)
                     latestCurrencyStatus = data[i]['status']
                     print (latestCurrencyStatus)

                     if (latestCurrencyId == generatedId) and (latestCurrencyStatus == 'ACTIVE') :
                         passed = True
                         status['CAM-APITest'] = passed
                         resp, body = self.api_client.deleteConvertionRates(generatedId)
                         print (resp)
                         return passed
                     else:
                         i = i + 1


         except:
             resp, body = self.api_client.deleteConvertionRates(generatedId)
             print (resp)
             status['CAM-APITest'] = False
             return False

    @assignOrder(519)
    def CORE3671_getCurrency_MultipleParameter_WithEndDate(self):
        try:
            passed = False

            body = {
                "currencyfrom": "HKD",
                "currencyto": "USD",
                "source": "automationDateParameter",
                "startdate": "2088-12-06T18:25:43.511Z",
                "enddate": "2088-12-12T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            # Verify POST
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            generatedId = data['id']

            # call the multiple parameter api
            resp, body = self.api_client.getConversionRates_multipleParameterwithDate('HKD','USD','automationDateParameter','2088-12-10T18:25:43.511Z')
            print (resp)
            data = json.dumps(body)
            data = json.loads(data)
            print (data)
            # Check whether id is not present on not

            i = 0
            latestCurrencyId = ""
            for currency in data:
                print (data[i]['id'])
                print (data[i]['status'])
                latestCurrencyId = data[i]['id']
                latestCurrencyStatus = data[i]['status']

                if (latestCurrencyId == generatedId) and (latestCurrencyStatus == 'ACTIVE'):
                    passed = True
                    status['CAM-APITest'] = passed
                else:
                    i = i + 1

            resp, body = self.api_client.deleteConvertionRates(generatedId)
            print (resp)
            return passed

        except:
            resp, body = self.api_client.deleteConvertionRates(generatedId)
            print (resp)
            status['CAM-APITest'] = False
            return False

    @assignOrder(520)
    def CORE3671_getCurrency_MultipleParameter_WithBetween_StartEndDate(self):
        try:
            passed = False

            body = {
                "currencyfrom": "HKD",
                "currencyto": "USD",
                "source": "automationDateParameter",
                "startdate": "2088-12-06T18:25:43.511Z",
                "enddate": "2088-12-11T18:25:43.511Z",
                "exchangerate": "64.2"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            # Verify POST
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            generatedId = data['id']

            # call the multiple parameter api
            resp, body = self.api_client.getConversionRates_multipleParameterwithDate('HKD', 'USD',
                                                                                      'automationDateParameter',
                                                                                      '2088-12-08T18:25:43.511Z')
            print (resp)
            print (data)
            data = json.dumps(body)
            data = json.loads(data)
            # Check whether id is not present on not
            i = 0
            latestCurrencyId = ""
            for currency in data:
                print (data[i]['id'])
                print (data[i]['status'])
                latestCurrencyId = data[i]['id']
                latestCurrencyStatus = data[i]['status']

                if (latestCurrencyId == generatedId) and (latestCurrencyStatus == 'ACTIVE'):
                    passed = True
                    status['CAM-APITest'] = passed
                else:
                    i = i + 1

            resp, body = self.api_client.deleteConvertionRates(generatedId)
            print (resp)
            return passed

        except:
            resp, body = self.api_client.deleteConvertionRates(generatedId)
            print (resp)
            status['CAM-APITest'] = False
            return False

    @assignOrder(521)
    def CORE2327_update_onlyExchangeRate(self):
        try:
            passed = False
            year = random.randint(2500, 2600)
            month = random.randint(10, 12)
            day = random.randint(10, 28)
            print ("Current year: %d" % year)
            print ("Current month: %d" % month)
            print ("Current day: %d" % day)

            completeDate = str(year) + "-" + str(month) + "-" + str(day) + "T" + "18:25:43.511" + "Z"
            print (completeDate)
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.2",
                "status": "ACTIVE"
            };
            resp, body = self.api_client.postConvertionRates(body)
            print (resp)
            # Verify POST
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 201) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            logger.info("API response:" + str(resp))
            if resp == 409:
                print ("Record Already Exist")
                passOfResponseCode = assertEqual(resp, 409)
                if (passOfResponseCode):
                    passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                passOfResponseCode = assertEqual(resp, 201)
            data = json.dumps(body)
            data = json.loads(data)
            print (data['id'])
            body = {
                "currencyfrom": "EUR",
                "currencyto": "USD",
                "source": "default",
                "startdate": completeDate,
                "enddate": completeDate,
                "exchangerate": "64.5",
                "status": "ACTIVE"
            };
            resp, body = self.api_client.update_convertionRates(body, data['id']);
            print (resp)
            logger.info("API response:" + str(resp))
            # Verify Update
            get_resp, get_body = self.api_client.getConversionRatesById(body['id'])
            passOfResponseCode = assertEqual(resp, 200) & assertEqual(body['currencyfrom'], get_body['currencyfrom']) & assertEqual(body['currencyto'], get_body['currencyto']) & assertEqual(body['source'], get_body['source']) & assertEqual(body['startdate'], get_body['startdate']) & assertEqual(body['enddate'], get_body['enddate']) & assertEqual(body['exchangerate'], get_body['exchangerate']) & assertEqual(body['status'], get_body['status'])

            resp, body = self.api_client.deleteConvertionRates(data['id'])
            print (resp)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CAM-APITest'] = False
            return False

    @assignOrder(522)
    def postValidInstanceCurrency_CORE_5309(self):
        try :
            passed = False
            body = {
                    "Alphabetic Code":["USD","INR"]
                };
            resp, body = self.api_client.postInstanceCurrency(body)
            print (resp)
            logger.info("API response:" + str(resp))
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

    @assignOrder(523)
    def postInValidInstanceCurrency_CORE_5309(self):
        try :
            passed = False
            body = {
                    "Alphabetic Code":["USD33"]
                };
            resp, body = self.api_client.postInstanceCurrency(body)
            print (resp)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 400)
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
