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
x = random.randint(0, 80000)

class NotificationAIOpsTest(object):
    def __init__(self, client):
        self.api_client = client

    @assignOrder(1)
    def postNotify_discovery_success(self):
        try:
            passed = False

            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"discovery_success",
               "parameters":[
                  {
                     "name":"schedule_name",
                     "value":"test_discovery_success"
                  },
                  {
                    "name":"time",
                    "value":"2019-10-30T18:25:43.511Z"
                  }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_discovery_success' in data['response'][0]['content']['body']
            subject = 'test_discovery_success' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days='2' in data['response'][0]['ttl_in_days']
            severity='info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body==type==subject==ttl_in_days==severity==userid==source==version==version==viewed==True:
                passOfResponseCode=True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False


    @assignOrder(2)
    def postNotify_discovery_in_progress(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"discovery_in_progress",
               "parameters":[
                  {
                     "name":"schedule_name",
                     "value":"test_discovery_in_progress"
                  },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body = 'test_discovery_in_progress' in data['response'][0]['content']['body']
            subject = 'test_discovery_in_progress' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(3)
    def postNotify_discovery_failed(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"discovery_failed",
               "parameters":[
                  {
                     "name":"schedule_name",
                     "value":"test_discovery_fail"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_discovery_fail' in data['response'][0]['content']['body']
            subject = 'test_discovery_fail' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(4)
    def postNotify_tag_update_in_progress(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"tag_update_in_progress",
               "parameters":[
                  {
                     "name":"job_id",
                     "value":"test_tag_update_in_progress"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_tag_update_in_progress' in data['response'][0]['content']['body']
            subject = 'test_tag_update_in_progress' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(5)
    def postNotify_tag_update_success(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"tag_update_success",
               "parameters":[
                  {
                     "name":"job_id",
                     "value":"test_tag_update_success"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_tag_update_success' in data['response'][0]['content']['body']
            subject = 'test_tag_update_success' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(6)
    def postNotify_tag_update_failed(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"tag_update_failed",
               "parameters":[
                  {
                     "name":"job_id",
                     "value":"test_tag_update_failed"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_tag_update_failed' in data['response'][0]['content']['body']
            subject = 'test_tag_update_failed' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(7)
    def postNotify_tag_removal_in_progress(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"tag_removal_in_progress",
               "parameters":[
                  {
                     "name":"job_id",
                     "value":"test_tag_removal_in_progress"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_tag_removal_in_progress' in data['response'][0]['content']['body']
            subject = 'test_tag_removal_in_progress' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(8)
    def postNotify_tag_removal_success(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"tag_removal_success",
               "parameters":[
                  {
                     "name":"job_id",
                     "value":"test_tag_removal_success"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_tag_removal_success' in data['response'][0]['content']['body']
            subject = 'test_tag_removal_success' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(9)
    def postNotify_tag_removal_failed(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"tag_removal_failed",
               "parameters":[
                  {
                     "name":"job_id",
                     "value":"test_tag_removal_failed"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_tag_removal_failed' in data['response'][0]['content']['body']
            subject = 'test_tag_removal_failed' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(10)
    def postNotify_export_in_progress(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"export_in_progress",
               "parameters":[
                  {
                     "name":"file_name",
                     "value":"test_export_in_progress"
                  },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_export_in_progress' in data['response'][0]['content']['body']
            subject = 'test_export_in_progress' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(11)
    def postNotify_export_success(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"export_success",
               "parameters":[
                  {
                     "name":"file_name",
                     "value":"test_export_success"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_export_success' in data['response'][0]['content']['body']
            subject = 'test_export_success' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(12)
    def postNotify_export_failed(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"export_failed",
               "parameters":[
                  {
                     "name":"file_name",
                     "value":"test_export_failed"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_export_failed' in data['response'][0]['content']['body']
            subject = 'test_export_failed' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(13)
    def postNotify_import_in_progress(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"import_in_progress",
               "parameters":[
                  {
                     "name":"file_name",
                     "value":"test_import_in_progress"
                  },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_import_in_progress' in data['response'][0]['content']['body']
            subject = 'test_import_in_progress' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(14)
    def postNotify_import_success(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"import_success",
               "parameters":[
                  {
                     "name":"file_name",
                     "value":"test_import_success"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_import_success' in data['response'][0]['content']['body']
            subject = 'test_import_success' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(15)
    def postNotify_import_failed(self):
        try:
            passed = False
            body = {
               "icb_application":"aiops",
               "applicationrefid":"app-ref-id-1",
               "userids":[
                  "prkarmak@in.ibm.com"
               ],
               "template":"import_failed",
               "parameters":[
                  {
                     "name":"file_name",
                     "value":"test_import_failed"
                  },
                   {
                       "name": "time",
                       "value": "2019-10-30T18:25:43.511Z"
                   },
                  {
                       "name": "severity",
                       "value": "info"
                   }
               ],
               "teams":["MYTEAM"]
            };

            resp, body = self.api_client.post_notify(body)
            print resp
            logger.info("Notification post successful" + str(resp))
            resp, body = self.api_client.get_nofication_message()
            data = json.dumps(body)
            data = json.loads(data)
            print data['response'][0]['content']['body']
            body= 'test_import_failed' in data['response'][0]['content']['body']
            subject = 'test_import_failed' in data['response'][0]['content']['subject']
            type = 'plain' in data['response'][0]['content']['type']
            ttl_in_days = '2' in data['response'][0]['ttl_in_days']
            severity = 'info' in data['response'][0]['severity']
            userid = 'prkarmak@in.ibm.com' in data['response'][0]['userid']
            source = 'aiops' in data['response'][0]['source']
            version = 'v1' in data['response'][0]['version']
            viewed = 'false' in data['response'][0]['viewed']
            if body == type == subject == ttl_in_days == severity == userid == source == version == version == viewed == True:
                passOfResponseCode = True

            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(16)
    def get_notification_msg_by_severity(self):
        try:
            passed = False
            resp, body = self.api_client.get_nofication_message_severity('low')
            data = json.dumps(body)
            data = json.loads(data)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(17)
    def get_notification_msg_by_viewed(self):
        try:
            passed = False
            resp, body = self.api_client.get_nofication_message_viewed('false')
            data = json.dumps(body)
            data = json.loads(data)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False

    @assignOrder(18)
    def get_nofication_message_by_page(self):
        try:
            passed = False
            resp, body = self.api_client.get_nofication_message_page(1)
            data = json.dumps(body)
            data = json.loads(data)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False



    @assignOrder(19)
    def get_nofication_message_by_all(self):
        try:
            passed = False
            resp, body = self.api_client.get_nofication_message_all(1,2,'false')
            data = json.dumps(body)
            data = json.loads(data)
            logger.info("API response:" + str(resp))
            passOfResponseCode = assertEqual(resp, 200)
            if (passOfResponseCode):
                passed = True
            status['CAM-APITest'] = passed
            return passed
        except:
            status['CoreX-APITest'] = False
            return False