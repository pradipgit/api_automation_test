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

class AuditLogArchiveHistory(object):
    def __init__(self,client):
        self.api_client = client
        self.invoice_id = random.randint(100000,999999)



    ########## CORE-2558 #################

    @assignOrder(465)
    def CORE2558_postArchiveHistory(self):
        passed = False
        body = [
            {
                "archive_file_startdate": "29-06-2018",
                "doc_type": "archive_file_details",
                "archive_file_user": "system",
                "archive_file_archive_date": "30-06-2018",
                "archive_file_enddate": "29-06-2018",
                "_rev": "1-7b984b7a2d79027e65fc4734de484b58",
                "archive_file_status": "Started",
                "archive_file_size": "56MB",
                "archive_file_initated_on": "29-06-2018",
                "archive_file_name": "ICB_archive_pkk_1",
                "archive_file_location": "/tmp/archive/location",
                "_id": "0cdcff314d24d545b73d11223b75b4a1",
                "archive_file_method": "Manual"
            }
        ];

        resp, body = self.api_client.postArchiveHistory(body)
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(466)
    def CORE2558_getArchiveHistory(self):
        passed = False
        resp, body = self.api_client.getArchiveHistory('ICB_archive_pkk_1')
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed


    @assignOrder(467)
    def CORE2558_deleteArchiveHistory(self):
        passed = False
        resp, body = self.api_client.deleteArchiveHistory('ICB_archive_pkk_1')
        print resp
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 204)
        if (passOfResponseCode):
            passed = True
        status['CAM-APITest'] = passed
        return passed

