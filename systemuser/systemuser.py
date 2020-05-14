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
from pprint import pprint
import random
global status
from os import path
import os
status = {}
logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()
config.read('settings.conf')
ResponseTime = config.get('params', 'response_time')
config.read('testdata.conf')
now = datetime.datetime.now()
x = random.randint(0, 80000)

class systemuser(object):
    def __init__(self, client):

        self.api_client = client


    @assignOrder(1)
    def deleteSystemUser(self):
        try:
            passed = False
            userId = "vijethkumarbs"
            resp, body = self.api_client.deleteSystemuser(userId)
            print(resp)
            if (resp == 204 or resp == 200):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return

    @assignOrder(2)
    def disableAuthorization(self):
        try:
            passed = False
            body = {
                "enable": False
            };
            resp, body = self.api_client.enableAuthorization(body)
            print(resp)
            if (resp == 200 or resp == 201):
                passed = True
                status['CAM-APITest'] = passed
                return passed
            else:
                status['CAM-APITest'] = False
                return passed
        except:
            status['CAM-APITest'] = False
            return


