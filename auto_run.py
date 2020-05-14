import configparser
import api_client
import utils
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import time
import sys
import importlib
from suite import TestSuite
from suite_storecicdv2 import StoreCicdTestSuite
from multi_stage_suite import MultiTenancy
import base64
import os
import shutil
import zipfile
import requests
requests.packages.urllib3.disable_warnings()
config = configparser.ConfigParser()
config.read('testdata.conf')
slack_channel = config.get('params', 'slack_result_channel')
token_name = config.get('params', 'token_name')

def run_api_tests():
    logger = logging.getLogger("Test Run")
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler("test_run.log", when = "m", interval = 10, backupCount=2)
    logger.addHandler(handler)
    #logging.basicConfig(filename='test.log', level=logging.INFO)
    logger.info("-----------------------------------------------")
    logger.info("Test started: "+datetime.now().strftime('%Y-%m-%d-%H%M%S'))
    start_time = time.time()
    botclient = api_client.BotClient()

    if len(sys.argv) !=3:
        print ("Error : Required arguments missing!!")
        print ("Usage : python auto_run.py <env> <build_version>")
        print ("ex : python auto_run.py qademo6 master_1945")
        exit(1)

    if (sys.argv[1]=='myminikube.info') :
        appurl = "https://" + sys.argv[1] + ":30091/"
    elif (sys.argv[1]=='automation-core-b') :
        appurl = "https://" + sys.argv[1] + "-api.multicloud-ibm.com/"
    else :
        appurl = "https://" + sys.argv[1] + "-api.gravitant.net/"

    if(sys.argv[1]=='cb-qa-corex'):
        api_key=config.get('params', 'cbqacorexapikey')
    elif(sys.argv[1]=='myminikube.info'):
        api_key = config.get('params', 'minikubeapikey')
    elif(sys.argv[1]=='store-cicd-v2'):
        api_key = config.get('params', 'store_cicd_apikey')
    elif(sys.argv[1]=='automation-core-b'):
        api_key = config.get('params', 'mtapikey')
    elif(sys.argv[1].find('cam-icp-api')!=-1):
        appurl = sys.argv[1]
        api_key = config.get('params', 'apikey')
    elif(sys.argv[1]=='cb-qa-core-premaster'):
        api_key = config.get('params', 'premaster_apikey')
    else:
        api_key = config.get('params', 'apikey')

    print("API key :" + api_key)
    print("URL :" + appurl)

    # decoding the apikey
    # api_key=utils.decodeCredential(api_key)
    print("API key decode:" + api_key)
    build_version = sys.argv[2]
    #tname = sys.argv[4]
    test_obj = config.get('params', 'test_object_name_in_suite')
    tname=config.get('params', 'test_case')
    testcase= tname.split(",")
    apiclient = api_client.APIClient(appurl,api_key)
    print ("Host Name :"+sys.argv[1])
    print ("API key:"+api_key)
    print ("Build Version :"+build_version)
    print ("URL :"+appurl)
    func_stat = {}
    #func_stat.update(utils.run_test_cases(api_tests.APITest(apiclient)))
    testSuite = TestSuite()
    testSuitenew = StoreCicdTestSuite()
    testSuiteMT=MultiTenancy()

    if (sys.argv[1] == 'cb-qa-corex' or sys.argv[1] == 'myminikube.info' or sys.argv[1] =='cb-qa-core-latest-release' or sys.argv[1] =='cb-qa-core-premaster'):
        test = testSuite.testsObj(appurl, api_key)
    elif (sys.argv[1]=='automation-core-b') :
        test = testSuiteMT.testsObj(appurl, api_key)
    else :
        test = testSuitenew.testsObj(appurl, api_key)

    if tname == 'all':
        for t in test:
            func_stat.update(utils.run_test_cases(test[t]))
    else:
        for c in testcase:
            try:
                #testname = getattr(api_tests.APITest(apiclient), t)
                testname= getattr(test[test_obj],c)
                func_stat.update(utils.run_test_cases(testname()))
            except AttributeError:
                print ("Test case not present.")

    execution_time = "*Total Time Taken for Execution : %s seconds *" % (time.time() - start_time)
    run_test = config.get('params', 'post_to_bot')
    text = "*APIs validation Result:*\n"
    if run_test == 'true':
        botclient.post_auto_stat(func_stat, slack_channel, text, appurl, build_version, execution_time)
    else:
        logger.info("Skipping posting the result to Slack!")
    logger.info("------------End of Tests------------")
    utils.get_error_logs_test_run()

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def log_upload():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    if os.path.exists("Test_Results.txt"):
        shutil.copy('Test_Results.txt', 'logs')
    if os.path.exists("test_run.log"):
        shutil.copy('test_run.log', 'logs')
    if os.path.exists('test_error.log'):
        shutil.copy('test_error.log', 'logs')
    zipf = zipfile.ZipFile('logs.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('logs/', zipf)
    zipf.close()
    #Upload results in slack based on settings configuration
    post_results = config.get('params', 'post_to_bot')
    if post_results == 'true':
        os.system(
           "curl -k -F file=@logs.zip -F channels={channels}  -F token={token} https://slack.com/api/files.upload".format(channels=slack_channel,token=token_name))
    else:
        logger.info("Skipping posting the result to Slack!")

if __name__ == '__main__':
    run_api_tests()
    log_upload()
