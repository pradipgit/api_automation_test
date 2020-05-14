import requests
import json
from utils import assertEqual
import operator
import logging
import time
import pprint
import utils
import sys
import configparser
from os import path
from requests import exceptions
import base64
import os
import shutil

logger = logging.getLogger("Test Run")
config = configparser.ConfigParser()
config.read('testdata.conf')
amazon_accessKey = config.get('aws', 'accessKey')
amazon_secretKey = config.get('aws', 'secretKey')
# azure
azure_clientId = config.get('azure', 'clientId')
azure_secret = config.get('azure', 'secret')
azure_subscriptionID = config.get('azure', 'subscriptionID')
azure_offerID = config.get('azure', 'offerID')
azure_tenantID = config.get('azure', 'tenantID')
azure_domain = config.get('azure', 'domain')

# google
google_serviceKey = config.get('google', 'serviceKey')
google_projectName = config.get('google', 'projectName')
google_projectId = config.get('google', 'projectId')
google_serviceAccountName = config.get('google', 'serviceAccountName')

# ibm
ibm_username = config.get('ibm', 'username')
ibm_apikey = config.get('ibm', 'apikey')

# icd
icd_username = config.get('icd', 'username')
icd_password = config.get('icd', 'password')

# snow
snow_username = config.get('snow', 'username')
snow_password = config.get('snow', 'password')

# vra
vra_username = config.get('vra', 'username')
vra_password = config.get('vra', 'password')

# azureBilling
azureBilling_applicationSecret = config.get('azureBilling', 'applicationSecret')

# googlebilling
googlebilling_serviceKey = config.get('googlebilling', 'serviceKey')
googlebilling_dataSet=config.get('googlebilling', 'dataSet')
googlebilling_bucket=config.get('googlebilling', 'bucket')

# snowBilling
snowBilling_username = config.get('snowBilling', 'username')
snowBilling_password=config.get('snowBilling', 'password')
snowBilling_url=config.get('snowBilling', 'url')

# vraBilling
vraBilling_username = config.get('vraBilling', 'username')
vraBilling_password=config.get('vraBilling', 'password')
vraBilling_tenant=config.get('vraBilling', 'tenant')

# aws-invalid
aws_invalid_accessKey = config.get('awsInvalid','accessKey')
aws_invalid_secretKey = config.get('awsInvalid','secretKey')

# aws-testConnection
aws_testConnection_accessKey = config.get('awsTestConnection', 'accessKey')
aws_testConnection_secretKey = config.get('awsTestConnection', 'secretKey')


class RestClient(object):
    def post(self, url, body, headers=None):
        resp = requests.post(url, body, headers=headers, verify=False)
        print("API Response Time for POST Call in Second's:",resp.elapsed.total_seconds())
        try:
            output = json.loads(resp.text)
            # resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def postsp(self, url, body, headers=None):
        resp = requests.post(url, body, headers=headers, verify=False)
        print("API Response Time for POST Call in Second's:",resp.elapsed.total_seconds())
        try:
            output = json.loads(resp.text)
            # resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, resp.text

    def put(self, url, body, headers=None):
        resp = requests.put(url, body, headers=headers, verify=False)
        print("API Response Time for PUT Call in Second's:",resp.elapsed.total_seconds())
        try:
            output = json.loads(resp.text)
            # resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def get(self, url, headers=None):
        resp = requests.get(url, headers=headers, verify=False)
        print("API Response Time for GET Call in Second's:",resp.elapsed.total_seconds())
        try:
            output = json.loads(resp.text)
            # resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def get_with_auth(self, url, username, password, headers=None):
        resp = requests.get(url, auth=(username, password), headers=headers, verify=False)
        print("API Response Time for GET Call in Second's:",resp.elapsed.total_seconds())
        try:
            output = json.loads(resp.text)
            # resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def delete(self, url, headers=None):
        resp = requests.delete(url, headers=headers, verify=False)
        print("API Response Time for DELETE Call in Second's:",resp.elapsed.total_seconds())
        # return resp.status_code
        try:
            output = json.loads(resp.text)
            # resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def patch(self, url, body, headers=None):
        resp = requests.patch(url, body, headers=headers, verify=False)
        print("API Response Time for PATCH Call in Second's:",resp.elapsed.total_seconds())
        try:
            output = json.loads(resp.text)
            # resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None


class BotClient(RestClient):
    def __init__(self):
        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    def post_auto_stat(self, status, channel, text_message, URL, build_version, execution_time):
        config.read('testdata.conf')
        url = config.get('params', 'slack_url')
        #url=utils.decodeCredential(url)
        text = text_message + "URL: " + URL + " Build Version: " + build_version + "\n"
        pcount = 0
        fcount = 0
        for key in sorted(status):
            if status[key][1] == True:
                text = text + status[key][0] + " : Passed\n"
                pcount += 1
            else:
                text = text + status[key][0] + " : *Failed*\n"
                fcount += 1
        print (text)
        # print execution_time
        logger.info(text)
        TotalFailed = utils.TotalTests - utils.TotalPassed
        # TestStatus = "\n" + "*Test Execution Summary*\n" + "Total Tests: "+str(utils.TotalTests)+"; Passed: "+str(utils.TotalPassed)+"; Failed: "+str(TotalFailed) +"\n" + execution_time
        TestStatus = "\n" + "*Test Execution Summary*\n" + "Total Tests: " + str(pcount + fcount) + "; Passed: " + str(
            pcount) + "; Failed: " + str(fcount) + "\n" + execution_time
        OpenDefects = "\n" + "*Open Defects : ----*\n"
        print (TestStatus)
        logger.info(TestStatus)
        Test_Results = text + TestStatus
        Test_Results_file = open("Test_Results.txt", "w")
        Test_Results_file.write(Test_Results)
        Test_Results_file.close()

        Pass_Results_file = open("PassCount.txt", "w")
        Pass_Results_file.write(str(utils.TotalPassed))
        Pass_Results_file.close()

        body = {"channel": channel, "username": "CBSCAMBot", "text": text + TestStatus + OpenDefects,
                "icon_emoji": ":mega:"}
        resp, body = self.post(url, json.dumps(body), headers=self.headers)
        return resp, body


class APIClient(RestClient):
    def __init__(self, appurl, api_key):
        # super(APIClient, self).__init__(output)
        self.endpoint = appurl
        config = configparser.ConfigParser()
        config.read('testdata.conf')
        if(sys.argv[1]=='automation-core-b'):
            username = config.get('params', 'username_mt')
        else:
            username = config.get('params', 'username')

        self.headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'apikey': api_key,
                        'username': username}

    # Rules API
    def add_rule(self, body):
        url = '%scb-credential-service/api/v2.0/rules' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print (url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def get_rule_by_id(self, ruleId):
        url = '%scb-credential-service/api/v2.0/rules/%s' % (self.endpoint, ruleId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def delete_rule_by_id(self, ruleId):
        url = '%scb-credential-service/api/v2.0/rules/%s' % (self.endpoint, ruleId)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def get_all_rules(self):
        url = '%scb-credential-service/api/v2.0/rules' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def patch_rule_status(self, body, ruleId):
        url = '%scb-credential-service/api/v2.0/rules/%s/isenabled' % (self.endpoint, ruleId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.patch(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    # Rule validation- Account & credential
    def validate_account_rule(self, body):
        url = '%scb-credential-service/api/v2.0/rules/accountvalidator' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def validate_credential_rule(self, body):
        url = '%scb-credential-service/api/v2.0/rules/credentialvalidator' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def revalidate_credential_rule(self, body):
        url = '%scb-credential-service/api/v2.0/rules/credentialrevalidator' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    #validation-result api
    def get_validation_result_by_id(self, valResId):
        url = '%scb-credential-service/api/v2.0/validationresults/%s' % (self.endpoint, valResId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def add_validation_result(self, body):
        url = '%scb-credential-service/api/v2.0/validationresults/' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def get_validation_result_by_credid(self, valResId, credId):
        url = '%scb-credential-service/api/v2.0/validationresults/%s/credentials/%s' % (self.endpoint, valResId, credId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_val_count_by_id(self, valResId):
        url = '%scb-credential-service/api/v2.0/validationresults/%s/validationcount' % (self.endpoint, valResId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp


    def get_val_count_by_credid(self, valResId, credId):
        url = '%scb-credential-service/api/v2.0/validationresults/%s/credentials/%s/validationcount' % (self.endpoint, valResId, credId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp


    #provider

    # def create_provider(self, body):
    #     url = '%scb-credential-service/api/v1.0/provider_account' % (self.endpoint)
    #     logger.info("Rest URL:" + url)
    #     print ("Rest URL: " + url)
    #     start = time.time()
    #     status, resp = self.post(url, json.dumps(body), headers=self.headers)
    #     logger.info(pprint.pformat(resp))
    #     data = json.dumps(resp)
    #     return status, resp

    # def update_provider(self, body, validId):
    #     url = '%scb-credential-service/api/v1.0/provider_account/%s' % (self.endpoint, validId)
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     start = time.time()
    #     status, resp = self.put(url, json.dumps(body), headers=self.headers)
    #     logger.info(pprint.pformat(resp))
    #     data = json.dumps(resp)
    #     return status, resp
    #
    # def delete_provider(self, validId):
    #     url = '%scb-credential-service/api/v1.0/provider_account/%s' % (self.endpoint, validId)
    #     logger.info("Rest URL:" + url)
    #     print ("Rest URL: " + url)
    #     start = time.time()
    #     status, resp = self.delete(url, headers=self.headers)
    #     # print status, resp
    #     logger.info(pprint.pformat(resp))
    #     # roundtrip = time.time() - start
    #     # print start, roundtrip
    #     data = json.dumps(resp)
    #     data = json.dumps(resp)
    #     return status, resp
    #
    # def get_providerById(self, validId):
    #     url = '%scb-credential-service/api/v1.0/provider_account?id=%s' % (self.endpoint, validId)
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     status, resp = self.get(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(data)
    #     return status, resp
    #
    # def get_providerByName(self, name):
    #     url = '%scb-credential-service/api/v1.0/provider_account?account_name=%s' % (self.endpoint, name)
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     status, resp = self.get(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(data)
    #     return status, resp
    #
    # def getAllProviders(self):
    #     url = '%scb-credential-service/api/v1.0/provider_accounts' % (self.endpoint)
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     status, resp = self.get(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(data)
    #     return status, resp
    #
    # def getProvider_InvalidURL(self):
    #     url = '%scb-credential-service/api/v1.0/provider_accounts444444' % (self.endpoint)
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     status, resp = self.get(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(data)
    #     return status, resp
    #
    # def get_providerByAccountName(self, validAccountName):
    #     url = '%scb-credential-service/api/v1.0/provider_account?account_name=%s' % (self.endpoint, validAccountName)
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     status, resp = self.get(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(data)
    #     return status, resp
    #
    # def get_providerByTeam_ProviderType(self, team):
    #     url = '%scb-credential-service/api/v1.0/provider_accounts?provider_type=[0]&team=%s' % (
    #     self.endpoint, '"' + team + '"')
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     status, resp = self.get(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(data)
    #     return status, resp
    #
    # def get_providerByTeam_ProviderType_AccountType(self, team, account_type):
    #     url = '%scb-credential-service/api/v1.0/provider_accounts?provider_type=[0]&team=%s' % (
    #     self.endpoint, '"' + team + '"' + "&account_type="'"' + account_type + '"')
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     status, resp = self.get(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(data)
    #     return status, resp
    #
    # def get_AccountByProviderType(self, type):
    #     url = '%scb-credential-service/api/v1.0/provider_accounts?provider_type=[%s]' % (self.endpoint, type)
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     status, resp = self.get(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(data)
    #     return status, resp

    def get_AccountByProviderCode(self, code):
        url = '%scb-credential-service/api/v2.0/accounts/type/billing?view=summary&serviceProviderCode=%s' % (
        self.endpoint, code)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountByProviderCodeSystem(self, code):
        url = '%scb-credential-service/api/v2.0/accounts/type/system?view=summary&serviceProviderCode=%s' % (
            self.endpoint, code)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountByProviderCodeAsset(self, code):
        url = '%scb-credential-service/api/v2.0/accounts/type/asset?view=summary&serviceProviderCode=%s' % (
            self.endpoint, code)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_Teams(self):
        url = 'https://' + sys.argv[1] + ':30093/authorization/v2/teams'
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def create_serviceProviders(self, body):
        url = '%scb-credential-service/api/v2.0/serviceProviders' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getIntegrationEndPoints_ById(self, validId):
        url = '%scb-credential-service/api/v2.0/integration_endpoint?id=%s' % (self.endpoint, validId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def update_serviceProviderMetadata(self, body, provider):
        url = '%scb-credential-service/api/v2.0/metadata/serviceProviders/%s' % (self.endpoint, provider)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def update_serviceProvider(self, body, provider):
        url = '%scb-credential-service/api/v2.0/serviceProviders/%s' % (self.endpoint, provider)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def delete_integration_endpoint(self, validId):
        url = '%scb-credential-service/api/v2.0/integration_endpoint/%s' % (self.endpoint, validId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=self.headers)
        # print status, resp
        logger.info(pprint.pformat(resp))
        # roundtrip = time.time() - start
        # print start, roundtrip
        data = json.dumps(resp)
        data = json.dumps(resp)
        return status, resp

    ############ Story CORE-608 ##########

    def create_vault_endPoint(self, body):
        url = '%scb-credential-service/api/v2.0/vault_endpoint' % (self.endpoint)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getAllVaultEndPoints(self):
        url = '%scb-credential-service/api/v2.0/vault_endpoints' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def getVaultEndPoints_ById(self, validId):
        url = '%scb-credential-service/api/v2.0/vault_endpoint/%s' % (self.endpoint, validId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def update_vault_endpoint(self, body, validId):
        url = '%scb-credential-service/api/v2.0/vault_endpoint/%s' % (self.endpoint, validId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def delete_vault_endpoint(self, validId):
        url = '%scb-credential-service/api/v2.0/vault_endpoint/%s' % (self.endpoint, validId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=self.headers)
        # print status, resp
        logger.info(pprint.pformat(resp))
        # roundtrip = time.time() - start
        # print start, roundtrip
        data = json.dumps(resp)
        data = json.dumps(resp)
        return status, resp

    def create_account(self, body):
        url = '%scb-credential-service/api/v2.0/accounts' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        body = json.dumps(body)
        # #print body
        status, resp = self.post(url, body, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def create_accounts(self, body):
        url = '%scb-credential-service/api/v2.0/accounts' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def get_AccountsEndpointPurpose(self):
        url = '%scb-credential-service/api/v2.0/account/endpointID/5e9cc48d-3f27-49fb-bb2b-09572c8a6aa4/purpose/billing' % (
        self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountsEndpointTypePurpose(self):
        url = '%scb-credential-service/api/v2.0/account/endpointType/AWS/purpose/billing' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountsContextEndpointPurpose(self):
        url = '%scb-credential-service/api/v2.0/account/teamCode/team1/app/App1/env/Env1/org/Org1/endpointID/MyAmanzonID/purpose/test' % (
        self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountById(self, id):
        url = '%scb-credential-service/api/v2.0/accounts/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountsByIdContextPurpose(self, id):
        url = '%scb-credential-service/api/v2.0/account/id/%s/teamCode/teamA/app/App1/env/Env1/org/Org1/purpose/test' % (
        self.endpoint, id)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountByIds(self, id):
        url = '%scb-credential-service/api/v2.0/accounts/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def create_serviceProvidersMetadata(self, body):
        url = '%scb-credential-service/api/v2.0/metadata/serviceProviders' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def update_integration_endPoint_metadata(self, body, id):
        url = '%scb-credential-service/api/v2.0/integration_endpoint_metadata/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def get_serviceProvider(self, provider):
        url = '%scb-credential-service/api/v2.0/serviceProviders/%s' % (self.endpoint, provider)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def get_serviceProviderMetadata(self, provider):
        url = '%scb-credential-service/api/v2.0/metadata/serviceProviders/%s' % (self.endpoint, provider)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def get_serviceProviders(self, id):
        url = '%scb-credential-service/api/v2.0/serviceProviders/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def delete_serviceProviderMetadata(self, provider):
        url = '%scb-credential-service/api/v2.0/metadata/serviceProviders/%s' % (self.endpoint, provider)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def delete_serviceProvider(self, provider):
        url = '%scb-credential-service/api/v2.0/serviceProviders/serviceProviderCode/%s' % (self.endpoint, provider)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def create_credential(self, body):
        url = '%scb-credential-service/api/v2.0/credential' % (self.endpoint)
        logger.info("Rest URL:" + url)
        status, resp = self.postsp(url, json.dumps(body), headers=self.headers)
        print ("Rest URL: " + url)
        #print body
        print (resp)
        print (status)
        logger.info(pprint.pformat(resp))
        return status, resp

    def update_credential(self, body, id):
        url = '%scb-credential-service/api/v2.0/credential/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def get_credential(self, id):
        url = '%scb-credential-service/api/v2.0/credential/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def delete_credential(self, id):
        url = '%scb-credential-service/api/v2.0/credential/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def update_accounts(self, body, id):
        url = '%scb-credential-service/api/v2.0/accounts/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def update_account(self, body, id):
        url = '%scb-credential-service/api/v2.0/accounts/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def get_AccountsLimitAndPage(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/billing?limit=5&page=1' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountsForWrongLimit(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/billing?limit=-5&page=1' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountsForWrongPage(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/billing?limit=5&page=-1' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def create_purpose(self, body):
        url = '%scb-credential-service/api/v2.0/purpose' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getAll_purpose(self):
        url = '%scb-credential-service/api/v2.0/purpose' % (self.endpoint)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getByCode_purpose(self, code):
        url = '%scb-credential-service/api/v2.0/purpose?code=%s' % (self.endpoint, code)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def updatePurpose_ByCode(self, body, code):
        url = '%scb-credential-service/api/v2.0/purpose?code=%s' % (self.endpoint, code)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def updatePurpose_ById(self, body, id):
        url = '%scb-credential-service/api/v2.0/purpose?id=%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def deletePurpose_ByCode(self, code):
        url = '%scb-credential-service/api/v2.0/purpose?code=%s' % (self.endpoint, code)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def deletePurpose_ById(self, id):
        url = '%scb-credential-service/api/v2.0/purpose?id=%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def getAllAccountsV2(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/billing' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def deleteAccountV2(self, id):
        url = '%scb-credential-service/api/v2.0/accounts/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def testConnection(self, body):
        url = '%scb-credential-service/api/v2.0/credentialsValidator' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def searchProviderAccount(self, id):
        url = '%scb-credential-service/api/v2.0/search?userType=asset&searchText=%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    ############### CORE-1914 & CORE-787 ##############

    def searchByDetails(self, text):
        url = '%score/audit/api/v2.1/logs?searchText=%s' % (self.endpoint, text)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def searchByActionType(self, actiontype):
        url = '%score/audit/api/v2.1/logs?searchText=%s' % (self.endpoint, actiontype)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def searchByComponent(self, component):
        url = '%score/audit/api/v2.1/logs?searchText=%s' % (self.endpoint, component)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def searchBySubComponent(self, subcomponent):
        url = '%score/audit/api/v2.1/logs?searchText=%s' % (self.endpoint, subcomponent)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def searchByUser(self, user):
        url = '%score/audit/api/v2.1/logs?searchText=%s' % (self.endpoint, user)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def searchByTeam(self, team):
        url = '%score/audit/api/v2.1/logs?searchText=%s' % (self.endpoint, team)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

        ############### CORE-1914 & CORE-1732 ##############

    def advanceSearchByStartDateAndEndDate(self, sdate, edate):
        url = '%score/audit/api/v2.1/logs?startDate=%s&endDate=%s' % (self.endpoint, sdate, edate)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def advanceSearchByActionType(self, actiontype):
        url = '%score/audit/api/v2.1/logs?searchType=advanced&sortBy=initiatedDate&sort=desc&searchText=&startDate=&endDate=&subcomponent=[]&userId=[]&teamId=[]&component=[]&messageType=[\'%s\']'% (self.endpoint, actiontype)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def advanceSearchByComponent(self, comp):
        url = '%score/audit/api/v2.1/logs?searchText=""&startDate=&endDate=&messageType=[ ]&subcomponent=[ ]&userId=[ ]&teamId=[ ]&searchType=advanced&sortBy=initiatedDate&sort=desc&component=[\'%s\']'% (self.endpoint, comp)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def advanceSearchBySubComponent(self, subcomp):
        url = '%score/audit/api/v2.1/logs?searchText=""&startDate=&endDate=&messageType=[ ]&component=[ ]&userId=[ ]&teamId=[ ]&searchType=advanced&sortBy=initiatedDate&sort=desc&subcomponent=[\'%s\']'% (self.endpoint, subcomp)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def advanceSearchByUser(self, user):
        url = '%score/audit/api/v2.1/logs?searchText=""&startDate=&endDate=&messageType=[ ]&component=[ ]&subcomponent=[ ]&teamId=[ ]&searchType=advanced&sortBy=initiatedDate&sort=desc&userId=[\'%s\']'%(self.endpoint, user)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def advanceSearchByUserTeam(self, userteam):
        url = '%score/audit/api/v2.1/logs?searchText=""&startDate=&endDate=&messageType=[ ]&component=[ ]&subcomponent=[ ]&searchType=advanced&sortBy=initiatedDate&sort=desc&userId=[]&teamId=[\'%s\']'% (self.endpoint, userteam)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def advanceSearchByActionTypeAndUser(self, actiontype, user):
        url = '%score/audit/api/v2.1/logs?actionType=%s&user=%s' % (self.endpoint, actiontype, user)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def advanceSearchByAllCategory(self, sText,sdate, edate, actiontype, subcomp,user,team,comp):
        url = '%score/audit/api/v2.1/logs?searchType=advanced&sortBy=initiatedDate&sort=desc&searchText=%s&startDate=%s&endDate=%s&messageType=[\'%s\']&subcomponent=[\'%s\']&userId=[\'%s\']&teamId=[\'%s\']&component=[\'%s\']' % (
        self.endpoint, sText,sdate, edate, actiontype, subcomp,user,team,comp)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    ################### CORE-1909 #########################

    def sortByAction(self, sorttype, field):
        url = '%score/audit/api/v2.1/logs?sort=%s&sortBy=%s' % (self.endpoint, sorttype, field)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def filterByStartDataAndEndDate(self, sdate, edate):
        url = '%score/audit/api/v2.1/logs?startDate=%s&endDate=%s' % (self.endpoint, sdate, edate)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def filterByAll(self, sdate, edate, limit, page, sort, sortby):
        url = '%score/audit/api/v2.1/logs?startDate=%s&endDate=%s&limit=%s&page=%s&sort=%s&sortby=%s' % (
        self.endpoint, sdate, edate, limit, page, sort, sortby)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def paginationWithLimitAndPage(self, limit, page):
        url = '%score/audit/api/v2.1/logs?limit=%s&page=%s' % (self.endpoint, limit, page)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    ########################### CORE-1915 ##########################

    def downloadAuditLog(self, body):
        url = '%score/audit/api/v2.1/logsArchive' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def downloadAuditLogLocal(self, id):
        url = '%score/audit/api/v2.1/logsArchive/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    ########################CORE-2005#################

    def get_systemAccount(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/system?limit=100&page=1' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_billingAccount(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/billing?limit=100&page=1' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_systemAccountWrongData(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/system?limit=-100&page=1' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_billingAccountWrongData(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/billing?limit=100&page=-1' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp


        ########################CORE-2273#################

    def populateAdvancedSearchScreen(self, attr):
        url = '%score/audit/api/v2.1/logs/filterValues?attribute=%s' % (self.endpoint, attr)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    ######################## CORE-2268 ##############


    def postArchivePolicy(self, body):
        url = '%score/audit/api/v2.1/archivePolicies/policy' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getArchivePolicy(self):
        url = '%score/audit/api/v2.1/archivePolicies/policy' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def putArchivePolicy(self, body):
        url = '%score/audit/api/v2.1/archivePolicies/policy' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def deleteArchivePolicy(self):
        url = '%score/audit/api/v2.1/archivePolicies/policy' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    ############CORE-2558 ###############

    def postArchiveHistory(self, body):
        url = '%score/audit/api/v2.1/logs/archive/details' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getArchiveHistory(self, archive_file_name):
        url = '%score/audit/api/v2.1/logs/archive/details/%s' % (self.endpoint, archive_file_name)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def putArchiveHistory(self, body, storage_configuration_id):
        url = '%score/audit/api/v2.1/logs/archive/configurations/%s' % (self.endpoint, storage_configuration_id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def deleteArchiveHistory(self, archive_file_name):
        url = '%score/audit/api/v2.1/logs/archive/details/%s' % (self.endpoint, archive_file_name)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    ################ CORE-2280 ##############

    def postAuditLogNotification(self, body):
        url = '%score/audit/api/v2.1/notification' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    #############CORE-2269#############

    def postAuditLogArchive(self, body):
        url = '%score/audit/api/v2.1/archiveUntil' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    #############CORE-2302#############

    def putArchiveConfiguration(self, body):
        url = '%score/audit/api/v2.1/logs/archive/configurations' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    #####################CORE-2572###############

    def purgeAuditLog(self):
        url = '%score/audit/api/v2.1/purge/logs' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp


    ##############################
    def keyWordSearch(self):
        url = '%score/audit/api/v2.1/logs?page=1&limit=10&searchText=Failed&searchType=keyword' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def keyWordSearchText(self,Text):
        url = '%score/audit/api/v2.1/logs?page=1&limit=10&searchText=%s&searchType=keyword' % (self.endpoint,Text)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def keyWordSearchwithLimit25(self):
        url = '%score/audit/api/v2.1/logs?page=1&limit=25&searchText=Failed&searchType=keyword&sortBy=initiatedDate&sort=desc' % (
        self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def keyWordSearchwithLimit25_pagination(self):
        url = '%score/audit/api/v2.1/logs?page=2&limit=25&searchText=Failed&searchType=keyword&sortBy=initiatedDate&sort=desc' % (
        self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp



    #####################CORE-2327###############
    def postdefaultCurreny(self, body):
        url = '%score/configuration/v1/configvalues' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def lockdefaultCurreny(self, body):
        url = '%score/configuration/v1/configvalues' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getCurrencyLockStatus(self):
        url = '%score/configuration/v1/configvalues/default_currency_status' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getdefaultCurrency(self):
        url = '%score/configuration/v1/configvalues/default_currency' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getAllConvertion(self):
        url = '%score/currency/v2/currencyConversionRates' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def postConvertionRates(self, body):
        url = '%score/currency/v2/currencyConversionRates' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def deleteConvertionRates(self, id):
        url = '%score/currency/v2/currencyConversionRates/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getSupportedCurrencies(self):
        url = '%score/currency/v2/supportedCurrencies' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def update_convertionRates(self, body, id):
        url = '%score/currency/v2/currencyConversionRates/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def getCredentialsByName(self, id, credName):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials?credentialName=%s' % (
        self.endpoint, id, credName)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getCredentialsByPurpose(self, id, purpose):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials?purpose=%s' % (self.endpoint, id, purpose)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getCredentialsByTeam(self, id, team):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials?team=%s' % (self.endpoint, id, team)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getCredentialsByOrg(self, id, org):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials?organization=%s' % (self.endpoint, id, org)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getCredentialsByEnv(self, id, env):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials?environment=%s' % (self.endpoint, id, env)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getCredentialsByApp(self, id, app):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials?application=%s' % (self.endpoint, id, app)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp


    def getCredentialsByCredentialId(self, id, credId):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials?credentialId=%s' % (self.endpoint, id, credId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    ################ CORE-2762 ################

    def auditArchiveSearchText(self, text):
        url = '%score/audit/api/v2.1/archives?searchText=%s' % (self.endpoint, text)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def auditArchiveLimitPage(self, limit, page):
        url = '%score/audit/api/v2.1/archives?limit=%s&page=%s' % (self.endpoint, limit, page)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def auditArchiveJobType(self, jobType):
        url = '%score/audit/api/v2.1/archives?jobType=%s' % (self.endpoint, jobType)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def auditArchiveStatus(self, status):
        url = '%score/audit/api/v2.1/archives?JobStatus=%s' % (self.endpoint, status)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def auditArchiveSortBy(self, sortBy, sort):
        url = '%score/audit/api/v2.1/archives?sortBy=%s&sort=%s' % (self.endpoint, sortBy, sort)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    ######################CORE-2763#######################

    def initiateArchiveJobs(self, body):
        url = '%score/audit/api/v2.1/logs/archives' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def patchArchiveJobs(self, body):
        url = '%score/audit/api/v2.1/logs/archives' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.patch(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def get_VaultConfiguration(self):
        url = '%scb-credential-service/api/v2.0/vault/configuration/name/HashiCorp-Vault' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        # Making a get request
        data = json.dumps(resp)
        logger.info(data)
        return status,resp

    def delete_VaultConfiguration(self, id):
        url = '%scb-credential-service/api/v2.0/vault/configuration/id/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def postVaultConfiguration(self, body):
        url = '%scb-credential-service/api/v2.0/vault/configuration' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getInvalidVaultConfiguration(self):
        url = '%scb-credential-service/api/v2.0/vault/configuration/name/HashiCorp-Vault47329^^^%s' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    # def createOrder(self, orderURL, serviceInstanceName, provider, orderNumber):
    #     config = ConfigParser.ConfigParser()
    #     config.read('testdata.conf')
    #     print ("orderNumber" + str(orderNumber))
    #     passed = False
    #     config.read('testdata.conf')
    #     print (666666)
    #     with open(self.findBluePrint(provider), "r+") as jsonFile:
    #         body = json.load(jsonFile)
    #         body["serviceInstanceName"] = serviceInstanceName
    #         jsonFile.close()
    #     # #print body
    #     resp, body, roundtrip = self.post_New_Operation(orderURL, body)
    #     print (resp)
    #     # #print body
    #     logger.info("API response:" + str(resp))
    #     passOfResponseCode = assertEqual(resp, 201)
    #     if (passOfResponseCode):
    #         passed = True
    #         config.set('order', 'order_number' + str(orderNumber), str(body["orderNumber"]))
    #         with open('testdata.conf', 'wb') as configfile:
    #             config.write(configfile)
    #         print ("order Number" + str(orderNumber) + " : " + str(body["orderNumber"]))
    #     if body:
    #         retBody = str(body["orderNumber"])
    #     else:
    #         retBody = ""
    #     return retBody, passed
    def createOrder(self, orderURL, serviceInstanceName, provider, role, teamName):

        # providerAccountName = str(provider + "-" + role).upper()
        print("inside create order")
        passed = False
        orderNumber = ""
        config.read('testdata.conf')
        with open(self.findBluePrint(provider), "r+") as jsonFile:
            body = json.load(jsonFile)
            body["serviceInstancePrefix"] = serviceInstanceName
            body["providerAccountRefId"], body["providerCredentialRefId"] = self.getRefIDs(provider, teamName)
            body["context"] = self.getContextOfTeam(role, teamName)
            # if (isCustOps == True):
            #     body["serviceOfferingId"] = "CentOS65-CustOps"
            #     # body["serviceOfferingName"] = "CentOS65-CustOps"
            jsonFile.close()
        # print body
        print
        print("inside create order222")
        "&&&&&&&&&&&&&&& CREATE ORDER HEADER AND BODY &&&&&&&&&&&&&&&&&&&&&&&&"
        "&&&&&&&&&&&&&&& CREATE ORDER HEADER AND BODY &&&&&&&&&&&&&&&&&&&&&&&&"

        resp, body, roundtrip = self.post_New_Operation(orderURL, body)
        print(resp)
        print(body)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
            print
            "order Number : " + str(body["orderNumber"])
            orderNumber = body["orderNumber"]
        else:
            print
            "Order not placed successfully"
        return orderNumber

    def post_New_Operation(self, url, body):
        url = '%s%s' % (self.endpoint, url)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        # print json.dumps(body)
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        # print status, resp
        logger.info(pprint.pformat(resp))
        roundtrip = time.time() - start
        # print start, roundtrip
        data = json.dumps(resp)
        logger.info(data)
        return status, resp, roundtrip

    def findBluePrint(self, provider):
        # file_to_open=""
        if provider == 'vra':
            blueprint_folder = path.join("testdata", "vra")
            file_to_open = path.join(blueprint_folder, "vraBluePrint.json")
        elif provider == 'aws':
            blueprint_folder = path.join("testdata", "amazon")
            file_to_open = path.join(blueprint_folder, "amazonBluePrint.json")
        elif provider == 'icd':
            blueprint_folder = path.join("testdata", "icd")
            file_to_open = path.join(blueprint_folder, "icdBluePrint.json")
        elif provider == 'snow':
            blueprint_folder = path.join("testdata", "snow")
            file_to_open = path.join(blueprint_folder, "snowBluePrint.json")
        elif provider == 'softlayer':
            blueprint_folder = path.join("testdata", "softlayer")
            file_to_open = path.join(blueprint_folder, "softlayerBluePrint.json")
            #file_to_open = path.join(blueprint_folder, "softlayerBluePrintMultiple.json")
        elif provider == 'azure':
            blueprint_folder = path.join("testdata", "azure")
            epoch_time = str(int(time.time()))
            resourceGrpName = "test" + epoch_time
            print (resourceGrpName)
            # with open(os.getcwd()+"/testdata/azure/azureBluePrint.json", 'r') as file:
            #      json_data = json.load(file)
            #      for item in json_data:
            #            if item['label'] in ["sadsdsasaddaad","sadd"]:
            #               item['label'] = resourceGrpName
            # with open(os.getcwd()+"/testdata/azure/azureBluePrint.json", 'w') as file:
            #     json.dump(json_data, file, indent=2)
            src = os.getcwd()+"/testdata/azure/azureBluePrint.json"
            dst = os.getcwd()+"/testdata/azure/azureBluePrint1.json"
            shutil.copy(src, dst)
            print(resourceGrpName)
            fin = open(dst, "rt")
            data = fin.read()
            data = data.replace('sadsdsasaddaad', resourceGrpName)
            data = data.replace('asdsd', resourceGrpName)
            fin.close()
            fin = open(dst, "wt")
            fin.write(data)
            fin.close()
            # with open(src, "r") as test:
            #     json_data = json.load(test)
            #     for config_grp in json_data["configGroups"]:
            #         for configGroups in json_data['Resource_Group_Parameters']:
            #             print(json_data['configGroupCode/Resource_Group_Parameters'][''][resourceGrpName])
            #         #config_grp["configGroupCode"] = config_grp["configGroupCode"].replace("Resource_Group_Parameters", resourceGrpName)
            #         # for config_grp1 in json_data["configs"]:
            #             # config_grp1["configId"] = config_grp1["configId"].replace("newResourceGroupRequired", resourceGrpName)
            #         #     for selectedValues in configs:
            #         #         selectedValues["label"] = selectedValues["label"].replace('sadsdsasaddaad', resourceGrpName)
            #         #config_grp["tagValueCode"] = config_grp["tagValueCode"].replace("my_org", resourceGrpName)
            # with open(dst, "w") as new_file:
            #     new_file.write(json.dumps(json_data))
            file_to_open = path.join(blueprint_folder, "azureBluePrint1.json")
            #import pytest; pytest.set_trace()
        elif provider == 'google':
            blueprint_folder = path.join("testData", "google")
            file_to_open = path.join(blueprint_folder, "googleBluePrint.json")
        print ("file to open : " + str(file_to_open))
        return file_to_open


    def approveOrder(self, orderNumber):
        passed = False
        print ("Approving order number : " + str(orderNumber))
        orderURL = "api/orders/" + str(orderNumber) + "/approval"
        with open("approveOrder.json", "r+") as jsonFile:
            body = json.load(jsonFile)
            body["orderNumber"] = str(orderNumber)
            jsonFile.close()
        # #print body
        resp, body, roundtrip = self.post_New_Operation(orderURL, body)
        # print resp, body
        ##print body
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        return passed

    def getPurpose_AssetFilter(self, body):
        url = '%scb-credential-service/api/v2.0/accounts/accountSearch' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getPurpose_BillingFilter(self, body):
        url = '%scb-credential-service/api/v2.0/accounts/accountSearch' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getPurpose_SystemFilter(self, body):
        url = '%scb-credential-service/api/v2.0/accounts/accountSearch' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getConversionRatesWithHistory(self):
        url = '%score/currency/v2/currencyConversionRates?withHistory=true' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getConversionRatesWithoutHistory(self):
        url = '%score/currency/v2/currencyConversionRates?withHistory=false' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getConversionRatesById(self, validId):
        url = '%score/currency/v2/currencyConversionRates/%s' % (self.endpoint, validId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def getConversionRates_DeletedStaus(self):
       url = '%score/currency/v2/currencyConversionRates?status=DELETED' % (self.endpoint)
       logger.info("Rest URL:" + url)
       print ("Rest URL: " + url)
       start = time.time()
       status, resp = self.get(url, headers=self.headers)
       logger.info(pprint.pformat(resp))
       data = json.dumps(resp)
       return status, resp

    def getConversionRates_validStaus(self):
       url = '%score/currency/v2/currencyConversionRates?status=ACTIVE' % (self.endpoint)
       logger.info("Rest URL:" + url)
       print ("Rest URL: " + url)
       start = time.time()
       status, resp = self.get(url, headers=self.headers)
       logger.info(pprint.pformat(resp))
       data = json.dumps(resp)
       return status, resp

    def getConversionRates_InvalidStaus(self):
      url = '%score/currency/v2/currencyConversionRates?status=TEST' % (self.endpoint)
      logger.info("Rest URL:" + url)
      print ("Rest URL: " + url)
      start = time.time()
      status, resp = self.get(url, headers=self.headers)
      logger.info(pprint.pformat(resp))
      data = json.dumps(resp)
      return status, resp

    def getConversionRates_MultipleParamter(self,fromdt,todt,source):
      url = '%score/currency/v2/currencyConversionRates?from=%s&to=%s&source=%s ' % (self.endpoint,fromdt,todt,source)
      logger.info("Rest URL:" + url)
      print ("Rest URL: " + url)
      start = time.time()
      status, resp = self.get(url, headers=self.headers)
      logger.info(pprint.pformat(resp))
      data = json.dumps(resp)
      return status, resp

    def getConversionRates_validStausWithHistory(self):
       url = '%score/currency/v2/currencyConversionRates?status=ACTIVE&withHistory=true' % (self.endpoint)
       logger.info("Rest URL:" + url)
       print ("Rest URL: " + url)
       start = time.time()
       status, resp = self.get(url, headers=self.headers)
       logger.info(pprint.pformat(resp))
       data = json.dumps(resp)
       return status, resp

    def getConversionRates_multipleParameterwithDate(self,fromdt,todt,source,date):
        url = '%score/currency/v2/currencyConversionRates?from=%s&to=%s&source=%s&date=%s' % (self.endpoint,fromdt,todt,source,date)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getAuditLogArchive(self):
        url = '%score/audit/api/v2.1/archives' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp
    def getAuditLogArchiveByID(self,id):
        url = '%score/audit/api/v2.1/archives/%s' % (self.endpoint,id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def create_contextTagType(self, body):
        url = '%sauthorization/v2/contexts' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        body = json.dumps(body)
        #print body
        status, resp = self.post(url, body, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def create_contextTagValues(self, body,tagType):
        url = '%sauthorization/v2/contexts/contextvalues/%s' % (self.endpoint,tagType)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        body = json.dumps(body)
        #print body
        status, resp = self.post(url, body, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def update_contextTagType(self, body,tagType):
        url = '%sauthorization/v2/contexts/%s' % (self.endpoint,tagType)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp


#     BCM-857

    # def create_provider_authorization(self, body,headers):
    #     url = '%scb-credential-service/api/v1.0/provider_account' % (self.endpoint)
    #     logger.info("Rest URL:" + url)
    #     print ("Rest URL: " + url)
    #     start = time.time()
    #     status, resp = self.post(url, json.dumps(body),headers)
    #     logger.info(pprint.pformat(resp))
    #     data = json.dumps(resp)
    #     return status, resp

    # def get_providerByAccountName_authorization(self, validAccountName,headers):
    #     url = '%scb-credential-service/api/v1.0/provider_account?account_name=%s' % (self.endpoint, validAccountName)
    #     print ("Rest URL: " + url)
    #     logger.info("Rest URL:" + url)
    #     status, resp = self.get(url, headers)
    #     data = json.dumps(resp)
    #     logger.info(data)
    #     return status, resp
    #
    # def delete_provider_authorization(self, validId,headers):
    #     url = '%scb-credential-service/api/v1.0/provider_account/%s' % (self.endpoint, validId)
    #     logger.info("Rest URL:" + url)
    #     print ("Rest URL: " + url)
    #     start = time.time()
    #     status, resp = self.delete(url,headers)
    #     logger.info(pprint.pformat(resp))
    #     data = json.dumps(resp)
    #     data = json.dumps(resp)
    #     return status, resp

    def get_AccountById_authorization(self, id,headers):
        url = '%scb-credential-service/api/v2.0/accounts/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def create_account_authorization(self, body,headers):
        url = '%scb-credential-service/api/v2.0/accounts' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        body = json.dumps(body)
        #print body
        status, resp = self.post(url, body, headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def deleteAccountV2_authorization(self,id,headers):
        url = '%scb-credential-service/api/v2.0/accounts/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers)
        logger.info(pprint.pformat(resp))
        return status, resp


    def patchCredentials(self, body,accountId,credentialID,headers):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials/%s' % (self.endpoint,accountId,credentialID)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.patch(url, json.dumps(body),headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp


    def update_accounts_authorization(self, body, id,headers):
        url = '%scb-credential-service/api/v2.0/accounts/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body),headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp


    def patchContext(self, body,accountId,credentialID,ContextId,headers):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials/%s/context/%s' % (self.endpoint,accountId,credentialID,ContextId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.patch(url, json.dumps(body),headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getAllProviders_manageFalse(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/asset?manage=false&limit=1000' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_AccountByIds_manage(self,id,flag):
        url = '%scb-credential-service/api/v2.0/accounts/%s?manage=%s' % (self.endpoint,id,flag)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_credentials_manage(self,accountId,credentialId,flag,headers):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials?credentialId=%s&manage=%s' % (self.endpoint,accountId,credentialId,flag)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url,headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp


    def getAllProviders_manageTrue(self):
        url = '%scb-credential-service/api/v2.0/accounts/type/asset?manage=True&limit=100' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def migrateAcount(self, body):
        url = '%scb-credential-service/api/v2.0/accounts/migrate' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getMigrationFailedAccount(self, validId):
        url = '%scb-credential-service/api/v2.0/accounts?modelVersion=v2.0&accountId=%s' % (self.endpoint, validId)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def patchCredentials_migAccount(self, body,accountId,credentialID):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials/%s' % (self.endpoint,accountId,credentialID)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        #print body
        start = time.time()
        status, resp = self.patch(url, json.dumps(body),headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp


    def post_notify(self, body):
        url = '%score/notifications/v1/notify' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def get_nofication_message(self):
        url = '%score/notifications/v1/inapp/messages?size=1' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_nofication_message_severity(self,severity):
        url = '%score/notifications/v1/inapp/messages?severity=%s' % (self.endpoint,severity)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_nofication_message_viewed(self,view):
        url = '%score/notifications/v1/inapp/messages?viewed=%s' % (self.endpoint,view)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_nofication_message_page(self,page):
        url = '%score/notifications/v1/inapp/messages?page=%s' % (self.endpoint,page)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def get_nofication_message_all(self,page,size,view):
        url = '%score/notifications/v1/inapp/messages?page=%s&size=%s&viewed=%s' % (self.endpoint,page,size,view)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp


    def post_swagger(self, body):
        url = '%scb-core-swagger/v1/applications' % (self.endpoint)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp


    def delete_swagger_app(self, appName):
        url = '%scb-core-swagger/v1/applications/%s' % (self.endpoint, appName)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        data = json.dumps(resp)
        return status, resp

    def delete_swagger_service(self, appName,servicename):
        url = '%scb-core-swagger/v1/applications/%s/services/%s' % (self.endpoint, appName,servicename)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        data = json.dumps(resp)
        return status, resp

    def get_swagger_appName_ascending(self):
        url = '%scb-core-swagger/v1/applications?limit=100&page=1&sort=asc' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        data = json.dumps(resp)
        return status, resp

    def get_swagger_appName_descending(self):
        url = '%scb-core-swagger/v1/applications?limit=100&page=1&sort=desc' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        data = json.dumps(resp)
        return status, resp


    def get_swagger_serviceName(self,appName,ServiceName):
        url = '%scb-core-swagger/v1/applications/%s/services/%s' % (self.endpoint,appName,ServiceName)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        data = json.dumps(resp)
        return status, resp


    def put_swagger(self, body,appName,ServiceName):
        url = '%scb-core-swagger/v1/applications/%s/services/%s' % (self.endpoint,appName,ServiceName)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def create_validation_result_validation(self, body):
        url = '%scb-credential-service/api/v2.0/validationresults' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def update_validation_result_validation(self, body, valResId):
        url = '%scb-credential-service/api/v2.0/validationresults/%s' % (self.endpoint, valResId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def patch_validation_result_validation(self, body, valResId):
        url = '%scb-credential-service/api/v2.0/validationresults/%s' % (self.endpoint, valResId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.patch(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def storeCredValResult(self, body, id):
        url = '%scb-credential-service/api/v2.0/validationresults/%s/credentials' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def updateCredValResult(self, body, valresId, credId):
        url = '%scb-credential-service/api/v2.0/validationresults/%s/credentials/%s' % (self.endpoint, valresId, credId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def getAccount_Link(self,accountId,flag):
        url = '%scb-credential-service/api/v2.0/accounts/%s/subaccounts?link=%s&page=1&size=100' % (self.endpoint,accountId,flag)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def patchBasicAdvanceInfo(self,body,accountId):
        url = '%scb-credential-service/api/v2.0/accounts/%s/basicAdvancedInfo' % (self.endpoint,accountId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.patch(url, json.dumps(body),headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def patchBulkLining(self,body,accountId):
        url = '%scb-credential-service/api/v2.0/accounts/%s/subaccounts' % (self.endpoint,accountId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.patch(url, json.dumps(body),headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def postBulkDelete(self, body):
        url = '%scb-credential-service/api/v2.0/accounts/deleteaccounts' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def dlinkSingleAccount(self,body,accountId):
        url = '%scb-credential-service/api/v2.0/accounts/%s/parentaccountid' % (self.endpoint,accountId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.patch(url, json.dumps(body),headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def postCredentials(self, body,id):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials' % (self.endpoint,id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def postCertificateRefs(self, body):
        url = '%scb-credential-service/api/v1.0/certificatesrefs' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def postCredentialRefs(self, body):
        url = '%scb-credential-service/api/v1.0/credentialrefs' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp
    #
    # def deleteCertificateRefsById(self,id):
    #     url = '%scb-credential-service/api/v1.0/certificatesrefs/%s' % (self.endpoint, id)
    #     print ("Rest URL: " + url)
    #     start = time.time()
    #     status, resp = self.delete(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(resp)
    #     return status, resp

    def deleteCertificateRefsById(self,id,headers):
        url = '%scb-credential-service/api/v1.0/certificatesrefs/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=headers)
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def getCertificateRefsById(self,id,headers):
        url = '%scb-credential-service/api/v1.0/certificatesrefs/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=headers)
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    # def getCertificateRefsById(self,id):
    #     url = '%scb-credential-service/api/v1.0/certificatesrefs/%s' % (self.endpoint, id)
    #     print ("Rest URL: " + url)
    #     start = time.time()
    #     status, resp = self.get(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(resp)
    #     return status, resp

    # def putCertificateRefsById(self,body,id):
    #     url = '%scb-credential-service/api/v1.0/certificatesrefs/%s' % (self.endpoint, id)
    #     print ("Rest URL: " + url)
    #     start = time.time()
    #     status, resp = self.put(url, json.dumps(body), headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(resp)
    #     return status, resp

    def putCertificateRefsById(self,body,id,headers):
        url = '%scb-credential-service/api/v1.0/certificatesrefs/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=headers)
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def postCredRefCredential(self, body):
        url = '%scb-credential-service/api/v1.0/credentialrefs' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    # def deleteCredRefCredential(self,id):
    #     url = '%scb-credential-service/api/v1.0/credentialrefs/%s' % (self.endpoint, id)
    #     print ("Rest URL: " + url)
    #     start = time.time()
    #     status, resp = self.delete(url, headers=self.headers)
    #     data = json.dumps(resp)
    #     logger.info(resp)
    #     return status, resp

    def deleteCredRefCredential(self,id,headers):
        url = '%scb-credential-service/api/v1.0/credentialrefs/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.delete(url, headers=headers)
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def getCredRefCredentialById(self,id,headers):
        url = '%scb-credential-service/api/v1.0/credentialrefs/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=headers)
        #print "Status is" + status
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def putCredentialRefsById(self,body,id,headers):
        url = '%scb-credential-service/api/v1.0/credentialrefs/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.put(url, json.dumps(body), headers=headers)
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def patch_VaultConfiguration(self,body,id):
        url = '%scb-credential-service/api/v2.0/vault/configuration/id/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.patch(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def migrateProviders(self, body):
        url = '%scb-credential-service/api/v2.0/accounts/providerMetadata/migrate' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def patchAccountCredentials(self, body,accountId,credentialID):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials/%s' % (self.endpoint,accountId,credentialID)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.patch(url, json.dumps(body),headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def postInstanceCurrency(self, body):
        url = '%score/currency/v2/instanceCurrencies' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getServiceProviderCount(self):
        url = '%scb-credential-service/api/v2.0/accounts/serviceproviders/count?type=asset' % (self.endpoint)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def getServiceProviderCount_ProviderCode(self,code):
        url = '%scb-credential-service/api/v2.0/search?userType=asset&page=1&size=10&searchText=&serviceProviderCode[]=%s' % (self.endpoint,code)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def deleteAccountCredentials(self,accId,credId):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials/%s' % (self.endpoint,accId,credId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

#-------------------------------------e2e code added-----------------------------------------#

    def getResourcetoRunTest(self, provider, role, teamName):
        # Place Order
        findExistingSOI = False
        SID = "";
        RID = ""
        config.read('testurls.conf')
        orderURL = config.get('urls', 'orderURL')
        epoch_time = str(int(time.time()))
        serviceInstanceName = "testAPI" + epoch_time
        # print ("11111111111")
        print
        "Checking if there are any existing SOIs for the provider :: " + str(provider)
        if (provider == "aws"):
            SID, RID = self.findServiceInstance("Elastic%20Compute%20Cloud", "3", "aws", teamName)
        elif (provider == "vra"):
            SID, RID = self.findServiceInstance("CentOS65", "1", "vra", teamName)
        elif (provider == "softlayer"):
            SID, RID = self.findServiceInstance("Virtual%20Server", "2", "softlayer", teamName)
        elif (provider == "azure"):
            SID, RID = self.findServiceInstance("Windows%20Virtual%20Machine", "4", "azure", teamName)
        elif (provider == "google"):
            SID, RID = self.findServiceInstance("Cloud%20Storage", "4", "google", teamName)
        elif (provider == "googlepubsub"):
            SID, RID = self.findServiceInstance("Pub/Sub", "4", "google", teamName)
        else:
            print
            "provider is invalid"
        if (SID == "" or RID == ""):
            orderNumber = self.createOrder(orderURL, serviceInstanceName, provider, role, teamName)
            time.sleep(20)
            if (orderNumber != ""):
                # Approve Order
                passed = self.approveOrder_v2(orderNumber)
                # Wait for order to complete
                # orderNumber = "MFER7UUL"
                passed = self.checkForOrderCompletion(orderNumber)
                if (passed):
                    print
                    "Order successfully Completed for provider :: " + str(provider)
                    # get SID and resource ID
                    SID, RID = self.getSIDRID(orderNumber, provider)
                    if (SID != "" and RID != ""):
                        return SID, RID
                else:
                    print
                    "Order creation is not successful"
                    SID = ""
                    RID = ""
                    return SID, RID
        else:
            print
            "Automation will use the existing SOI to test"
            print
            "SID  :: " + str(SID)
            print
            "RID  :: " + str(RID)

        return SID, RID

    def findServiceInstance(self, searchText, orderNo, provider, teamName):
        config.read('userdata.conf')
        # providerAccount, serviceOfferingId, credentialsName = self.findProviderAccount(provider)
        SOI_search_URL = "v2/api/services?page=1&size=10&searchText=" + searchText + "&sortBy=ProvisionDate&sortOrder=desc&filterBy=status:Active|providerName:" + provider
        resp, body, roundtrip = self.get_all_tags_data(SOI_search_URL)
        SID = "";
        RID = ""
        print (resp)
        # print (body)
        # print ("333333333333333")
        if (str(body).find("orderID") > -1):
            for j in range(str(body).count("providerSID")):
                print (j)
                if (str(body["docs"][j]).find("External") > -1 or str(body["docs"][j]).find(teamName) <= -1):
                    continue
                print ("Order Id : " + str(body["docs"][j]["orderID"]))
                orderId = body["docs"][j]["orderID"]
                SOI_expansion_URL = "v3/api/services/" + provider + "/"
                SID = body["docs"][j]["SID"]
                resp_exp, body_exp, roundtrip = self.get_all_tags_data(SOI_expansion_URL + body["docs"][j]["SID"])
                print (resp_exp)
                print (body_exp)
                passOfResponseCode = assertEqual(resp_exp, 200)
                # print("44444444444444444444")
                passOfResponseCode_500 = assertEqual(resp_exp, 500)
                passOfResponseCode_410 = assertEqual(resp_exp, 410)
                if (passOfResponseCode_500 or passOfResponseCode_410 or body_exp["resources"] == None):
                    print ("SOI cannot be expanded")
                    continue
                elif (passOfResponseCode):
                    RID = body_exp["resources"][0]["resourceId"]
                    if (str(body_exp).find("resourceId") > -1):
                        print ("Resourcd Id : " + str(body_exp["resources"][0]["resourceId"]))
                        orderNumber = orderId
                        config.read('testdata.conf')
                        config.set('order', 'order_number' + orderNo, str(orderNumber))
                        with open('testdata.conf', 'w') as configfile:
                            # print ("55555555555555555555")
                            config.write(configfile)
                        break
                else:
                    print ("Search " + str(j) + " for SID failed. Resource would have been deleted")
        else:
            print ("No Active SIDs found for " + str(provider))
        return SID, RID


    def get_all_tags_data(self, url):
        url = '%s%s' % (self.endpoint, url)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        time.sleep(20)
        logger.info(pprint.pformat(resp))
        roundtrip = time.time() - start
        print (start, roundtrip)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp, roundtrip

    def get_response_data(self, url):
        url = '%s%s' % (self.endpoint, url)
        # status, resp = self.get(url, headers)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        roundtrip = time.time() - start
        print (start, roundtrip)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp, roundtrip

    def get_api_response_time(self, url):
        url = '%s%s' % (self.endpoint, url)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        roundtrip = time.time() - start
        print ("Actual Response Time : " + str(roundtrip))
        data = json.dumps(resp)
        logger.info(data)
        return status, resp, roundtrip

    def get_greenfiled_services(self, url):
        appurl = '%s%s' % (self.endpoint, url)
        print ("Rest URL: " + appurl)
        logger.info("Rest URL:" + appurl)
        status, resp = self.get(appurl, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp


    def post_response_data(self, url, body):
        url = '%s%s' % (self.endpoint, url)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        # print status, resp
        logger.info(pprint.pformat(resp))
        roundtrip = time.time() - start
        print (start, roundtrip)
        data = json.dumps(resp)
        return status, resp, roundtrip


    def cancelOrder(self, orderNumber):
        passed = False
        print ("Canceling order number : " + orderNumber)
        cancelURL = "api/orders/" + orderNumber + "/cancel"
        body = {"orderId": "" + orderNumber + ""}
        print (body)
        resp, body, roundtrip = self.post_New_Operation(cancelURL, body)
        print (resp)
        print (body)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        return passed

    def post_New_Operation(self, url, body):
        url = '%s%s' % (self.endpoint, url)
        print("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        print (json.dumps(body))
        print ("inside post_New_Operation ")
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        # print status, resp
        logger.info(pprint.pformat(resp))
        roundtrip = time.time() - start
        # print start, roundtrip
        data = json.dumps(resp)
        logger.info(data)
        return status, resp, roundtrip

    def getRefIDs(self, provider, teamName):
        providerAccountRefID = ""
        credentialAccountRefID = ""
        searchTeamNameString = "'" + teamName + "'"
        if (str(provider).find("google") > -1):
            provider = "google"
        print
        provider
        url = "cb-credential-service/api/v2.0/accounts/type/asset?limit=10&page=1&sort='ascending'&serviceProviderCode=" + provider + "&view=summary"
        resp, body, roundtrip = self.get_all_tags_data(url)
        if body != None:
            print(len(body))
            for i in range(len(body)):
                if (str(body[i]).find(searchTeamNameString) >= -1):
                    print ("Found the provider account for the team Name")
                    providerAccountRefID = body[i]["accountId"]
                    credentialAccountRefID = body[i]["credentials"][0]["id"]
                    break;
        print ("getRefIDs" +providerAccountRefID)
        print ("getAccRefIDs" +credentialAccountRefID)
        return providerAccountRefID, credentialAccountRefID


    def getContextOfTeam(self, role, teamName):
        context = []
        context_full = []
        print ("Team name :::::: " + str(teamName))
        url = "authorization/v3/teams/" + teamName
        # print("ssssssssssssssssssssss")
        resp, body, roundtrip = self.get_all_tags_data(url)
        # print("hhhhhhhhhhhhhhhhh")
        print (role)
        print (body)
        if body != None:
            print
            "Number of contexts : " + str(len(body["roles"][0]["contexts"]))
        if body != None:
            for i in range(len(body["roles"])):
                newrole = body['roles'][i]['name']
                print (newrole)
                # print(body['roles'][i]['name']).lower()
                print (newrole.lower())
                print (role.lower())
                if ((body['roles'][i]['name']).lower() == role.lower()):
                    j = 0
                    print
                    "Length of contexts matching role " + str(len(body['roles'][i]['contexts']))
                    if (len(body['roles'][i]['contexts']) > 1):
                        for j in range(len(body['roles'][i]['contexts'])):
                            print
                            str(body['roles'][i]['contexts'][j])
                            if (str(body['roles'][i]['contexts'][j]).find("env") > -1 and str(
                                    body['roles'][i]['contexts'][j]).find("app") > -1):
                                context = body['roles'][i]['contexts'][j]
                    else:
                        context = body['roles'][i]['contexts'][j]
                    print
                    context
                    if (str(context).find("env") > -1 and str(context).find("app") > -1):
                        if (str(context['env']).find("env_all") > -1):
                            context['env'] = "env1"
                        else:
                            context['env'] = str(context['env'][0])
                        if (str(context['app']).find("app_all") > -1):
                            context['app'] = "app1"
                        else:
                            context['app'] = str(context['app'][0])
                        context_full = [{
                            "tagValueCode": str(context["org"][0]),
                            "tagType": "org"
                        }, {
                            "tagValueCode": context["env"],
                            "tagType": "env"
                        },
                            {
                                "tagValueCode": context["app"],
                                "tagType": "app"
                            }, {
                                "tagValueCode": str(context["team"][0]),
                                "tagType": "team"
                            }]
                    else:
                        context_full = [{
                            "tagValueCode": str(context["org"][0]),
                            "tagType": "org"
                        }, {
                            "tagValueCode": str(context["team"][0]),
                            "tagType": "team"
                        }]

        return context_full


    def getTeamName(self, role):
        print ("Getting team name")
        config = configparser.ConfigParser()
        config.read('userroles.conf')
        team = config.get(sys.argv[1], role)
        return team

    def approveOrder_v2(self, orderNumber):
        passed = False
        username, apikey = self.getUsernameAPIkey("approver")
        # print "approver username" + str(username)
        # print "approver apikey" + str(apikey)
        apikey = base64.b64decode(apikey)
        headers = {
            "Username": username,
            "Content-Type": "application/json",
            "apikey": apikey
        }
        print ("Approving order number : " + str(orderNumber))
        url = "api/orderWorkFlow/v2"
        body = {
            "orderId": orderNumber,
            "approvalType": ["technical", "financial"],
            "userId": "gravitant321@gmail.com",
            "teamId": ""
        }
        print ("&&&&&&&&&&&&&&&&&&&&& approve order body and header &&&&&&&&&&&&&&&&")
        print (body)
        print ("&&&&&&&&&&&&&&&&&&&&& approve order body and header &&&&&&&&&&&&&&&&")

        # body = {"orderId": orderNumber,"approvalType":["technical","financial"],"userId":"gravitant321@gmail.com","teamId":""}
        resp, body, roundtrip = self.post_New_Operation(url, body)
        print (resp)
        print (body)
        logger.info("API response:" + str(resp))
        passOfResponseCode = assertEqual(resp, 200)
        if (passOfResponseCode):
            passed = True
        return passed

    def getUsernameAPIkey(self, role):
        print ("Getting username and apikey")
        config = configparser.ConfigParser()
        config.read('userroles.conf')
        username = "";
        apikey = ""

        if (role.find("purchaser") > -1):
            username = config.get(sys.argv[1], 'username_purchaser')
            apikey = config.get(sys.argv[1], 'apikey_purchaser')
        elif (role.find("operator") > -1):
            username = config.get(sys.argv[1], 'username_operator')
            apikey = config.get(sys.argv[1], 'apikey_operator')
        elif (role.find("buyer") > -1):
            username = config.get(sys.argv[1], 'username_buyer')
            apikey = config.get(sys.argv[1], 'apikey_buyer')
        elif (role.find("approver") > -1):
            username = config.get(sys.argv[1], 'username_approver')
            apikey = config.get(sys.argv[1], 'apikey_approver')
        elif (role.find("policy") > -1):
            username = config.get(sys.argv[1], 'username_policy')
            apikey = config.get(sys.argv[1], 'apikey_policy')
        elif (role.find("admin") > -1):
            username = sys.argv[4]
            apikey = sys.argv[5]

        return username, apikey

    # def checkForOrderCompletion(self, orderNumber):
    #     string_resp = ""
    #     passed = False
    #     print ("Waiting for (max 20 mins) following order to get completed :" + orderNumber)
    #     inventoryURL = "v2/api/services?page=1&size=10&searchText=testAPI&sortBy=ProvisionDate&sortOrder=desc&filterBy=status:Active"
    #     i = 0
    #     while i <= 20:
    #         time.sleep(4) # Giving some time for order to appear in cart DB
    #         print ("Time now :" + str(time.asctime(time.localtime(time.time()))))
    #         resp, body, roundtrip = self.get_response_data_csv(inventoryURL)
    #         # url = "/v5/api/orders?&searchText="+orderNumber+"&sortBy=createdDate&sortDir=desc&limit=50&offset=0"
    #         url = "api/orderWorkFlow/v2?orderId=" + orderNumber
    #         order_resp, order_body, roundtrip = self.get_all_tags_data(url)
    #         print ("order_body: " + str(order_body))
    #         if (str(order_body).find("No record found") <= -1 and str(order_body).find("this order is not found in cart db") <= -1):
    #             print (order_body["status"])
    #             if (str(order_body["status"]).lower().find("rejected") > -1 or str(order_body["status"]).lower().find(
    #                     "failed") > -1):
    #                 # if (order_body["data"][0]["status"].find ("Rejected")>-1 or order_body["data"][0]["status"].find ("Failed")>-1):
    #                 print ("Order is either Rejected or Failed")
    #                 return False
    #             # print body
    #             print ("provisioning in progress")
    #             if (str(body).find(orderNumber) > -1):
    #                 print ("Order got completed!!")
    #                 passed = True
    #                 return passed
    #         else:
    #             return passed
    #         time.sleep(1 * 60)  # 1 min
    #         i = i + 1
    #     return passed

    def checkForOrderCompletion(self, orderNumber):
        string_resp = ""
        passed = False
        print ("Waiting for (max 20 mins) following order to get completed :" + orderNumber)
        inventoryURL = "v2/api/services?page=1&size=10&searchText=testAPI&sortBy=ProvisionDate&sortOrder=desc&filterBy=status:Active"
        i = 0
        while i <= 20:
            time.sleep(4) # Giving some time for order to appear in cart DB
            print ("Time now :" + str(time.asctime(time.localtime(time.time()))))
            resp, body, roundtrip = self.get_response_data_csv(inventoryURL)
            # url = "/v5/api/orders?&searchText="+orderNumber+"&sortBy=createdDate&sortDir=desc&limit=50&offset=0"
            url = "api/orderWorkFlow/v2?orderId=" + orderNumber
            order_resp, order_body, roundtrip = self.get_all_tags_data(url)
            print ("order_body: " + str(order_body))
            if (str(order_body).find("No record found") <= -1 and str(order_body).find("this order is not found in cart db") <= -1):
                print (order_body["status"])
                if (str(order_body["status"]).lower().find("rejected") > -1 or str(order_body["status"]).lower().find(
                        "failed") > -1):
                    # if (order_body["data"][0]["status"].find ("Rejected")>-1 or order_body["data"][0]["status"].find ("Failed")>-1):
                    print ("Order is either Rejected or Failed")
                    return False
                # print body
                print ("provisioning in progress")
                if (str(body).find(orderNumber) > -1):
                    print ("Order got completed!!")
                    passed = True
                    return passed
            else:
                return passed
            time.sleep(1 * 60)  # 1 min
            i = i + 1
        return passed

    def get_response_data_csv(self, url):
        url = '%s%s' % (self.endpoint, url)
        # status, resp = self.get(url, headers)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        start = time.time()
        status, resp = self.get_csv(url)
        # print resp
        logger.info(pprint.pformat(resp))
        roundtrip = time.time() - start
        print (start, roundtrip)
        return status, resp, roundtrip

    def get_csv(self, url):
        resp = requests.get(url, headers=self.headers, verify=False)
        try:
            output = resp.text
            # resp.raise_for_status()
            return resp.status_code, output
        except ValueError:
            return resp.status_code, None

    def getSIDRID(self, orderNumber, provider):
        passed = False
        sid = "";
        rid = ""
        config.read('testurls.conf')
        assetURL = config.get('urls', 'assetURL')
        componentURL = config.get('urls', 'componentURL')
        print ("Getting service id and resource id for order: " + str(orderNumber))
        resp, body = self.get_greenfield_services_withSearch(assetURL, orderNumber)
        if (str(body).find("SID") > -1):
            sid = body["docs"][0]['SID']
        # Using sid, get the resource id
        try:
            resp, body, roundtrip = self.get_all_tags_data(componentURL + "/" + provider + '/' + sid)
        except (exceptions.ConnectionError):
            print ("Connection exception caught")
        if (str(body).find("name") > -1):
            for i in range(len(body["resources"])):
                # print body["resources"][i]['name']
                # print body["resources"][i]['resourceId']
                if (body["resources"][i]['resourceType'].find("Virtual Machine") > -1):
                    # print body["resources"][i]['name']
                    # body["resources"][i]['resourceId']
                    rid = body["resources"][i]['resourceId']
                    break
        else:
            print ("Resource not found for specified SID")
        return sid, rid

    def get_greenfield_services_withSearch(self, url, searchText):
        appurl = '%s%s&searchText=%s&filterBy=status:Active' % (self.endpoint, url, searchText)
        print ("Rest URL: " + appurl)
        logger.info("Rest URL:" + appurl)
        status, resp = self.get(appurl, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def enableAuthorization(self, body):
        # enable the authorization
        url = '%sauthorization/v1/sysusermgmt' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def generateSystemUserId(self, body):
        # generate a system userId
        url = '%sauthorization/v1/systemusers' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def generateAPIKeyforSystemUserId(self, body,userId):
        # generate a system userId
        url = '%sauthorization/v1/user/key/%s' % (self.endpoint,userId)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def createOrg(self, body):
        # generate a system userId
        url = '%score/authorization/v1/organizations' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def createTeam(self, body):
        # generate a system userId
        url = '%sauthorization/v3/teams' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def assignUsersTeam(self, body):
        # generate a system userId
        url = '%sauthorization/v2/users/teams' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getApikey(self,userId):
        appurl = '%sauthorization/v1/user/key/%s' % (self.endpoint, userId)
        print ("Rest URL: " + appurl)
        logger.info("Rest URL:" + appurl)
        status, resp = self.get(appurl, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def getAccountById_withProviderCreds(self,id,flag,headers):
        url = '%scb-credential-service/api/v2.0/accounts/%s?withProviderCreds=%s' % (self.endpoint,id,flag)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def getAccountById_TSA_withProviderCreds(self,id,flag):
        url = '%scb-credential-service/api/v2.0/accounts/%s?withProviderCreds=%s' % (self.endpoint,id,flag)
        print ("Rest URL: " + url)
        logger.info("Rest URL:" + url)
        status, resp = self.get(url, headers=self.headers)
        data = json.dumps(resp)
        logger.info(data)
        return status, resp

    def postAccountSearch(self, body):
        url = '%scb-credential-service/api/v2.0/accounts/accountSearch' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def postAccountSearch_systemUser(self,body,headers):
        url = '%scb-credential-service/api/v2.0/accounts/accountSearch' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def createAWS_CredRefs(self):
        accessKey=utils.decodeCredential(amazon_accessKey)
        # print(accessKey)
        secretKey=utils.decodeCredential(amazon_secretKey)
        # print(secretKey)
        crefId="amazon-cref-001"
        body = {
            "crefId": crefId,
            "credential":
            {
             "value":{
                    "secretKey":secretKey,
                    "accessKey":accessKey
                    }
                }
            };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createAzure_CredRefs(self):
        # decoded values
        clientId=utils.decodeCredential(azure_clientId)
        secret=utils.decodeCredential(azure_secret)
        subscriptionID=utils.decodeCredential(azure_subscriptionID)
        offerID=utils.decodeCredential(azure_offerID)
        tenantID=utils.decodeCredential(azure_tenantID)
        domain=utils.decodeCredential(azure_domain)
        crefId="azure-cref-asset-001"

        body = {
            "crefId": crefId,
            "credential":
                {
                    "value": {
                    "clientId":clientId,
                    "secret":secret,
                    "subscriptionID":subscriptionID,
                    "offerID":offerID,
                    "tenantID":tenantID,
                    "domain":domain
                    }
                }
        };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createGoogle_CredRefs(self):
        serviceKey=utils.decodeCredential(google_serviceKey)
        projectName=utils.decodeCredential(google_projectName)
        projectId=utils.decodeCredential(google_projectId)
        serviceAccountName=utils.decodeCredential(google_serviceAccountName)
        crefId="google-cref-asset-001"

        body = {
            "crefId": crefId,
            "credential":
                {
                "value": {
                    "serviceKey":serviceKey,
                    "projectName":projectName,
                    "projectId":projectId,
                    "serviceAccountName":serviceAccountName
                    }
                }
        };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createIBMCloud_CredRefs(self):
        username=utils.decodeCredential(ibm_username)
        apikey=utils.decodeCredential(ibm_apikey)
        crefId="ibm-cref-001"

        body = {
            "crefId": crefId,
            "credential":
            {
                "value": {
                    "username": username,
                    "apiKey": apikey
                }
            }
        };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createICD_CredRefs(self):
        username=utils.decodeCredential(icd_username)
        password=utils.decodeCredential(icd_password)
        crefId="icd-cref-001"

        body = {
            "crefId": crefId,
            "credential":
            {
                "value": {
                    "username":username,
                    "password":password
                }
            }
            };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createSnow_CredRefs(self):
        username=utils.decodeCredential(snow_username)
        password=utils.decodeCredential(snow_password)
        crefId="snow-cref-asset-001"

        body = {
            "crefId": crefId,
            "credential":
                {
                    "value": {
                        "username": username,
                        "password": password
                    }
                }
        };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createVRA_CredRefs(self):
        username=utils.decodeCredential(vra_username)
        password=utils.decodeCredential(vra_password)
        crefId="vra-cref-asset-001"

        body = {
            "crefId": crefId,
            "credential":
                {
                    "value": {
                        "username": username,
                        "password": password
                    }
                }
        };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createAzureBilling_CredRefs(self):
        applicationSecret=azureBilling_applicationSecret
        applicationSecret=utils.decodeCredential(applicationSecret)
        crefId="azure-cref-billing-001"
        body = {
            "crefId": crefId,
            "credential":
                {
                    "value": {
                        "applicationSecret":applicationSecret
                    }
                }
        };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createGoogleBilling_CredRefs(self):
        serviceKey=utils.decodeCredential(googlebilling_serviceKey)
        dataSet=utils.decodeCredential(googlebilling_dataSet)
        bucket=utils.decodeCredential(googlebilling_bucket)
        crefId="google-cref-billing-001"

        body = {
            "crefId": crefId,
            "credential":
                {
                "value": {
                    "serviceKey": serviceKey,
                    "Data Set": dataSet,
                    "Bucket": bucket
                    }
                }
            };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createSnowBilling_CredRefs(self):
        username=utils.decodeCredential(snowBilling_username)
        password=utils.decodeCredential(snowBilling_password)
        url=utils.decodeCredential(snowBilling_url)
        crefId="snow-cref-billing-001"

        body = {
            "crefId": crefId,
            "credential":
                {
                    "value": {
                        "username":username,
                        "url": url,
                        "password":password
                    }
                }
        };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createVRABilling_CredRefs(self):
        username=utils.decodeCredential(vraBilling_username)
        password=utils.decodeCredential(vraBilling_password)
        tenant=utils.decodeCredential(vraBilling_tenant)
        crefId="vra-cref-billing-001"

        body = {
            "crefId": crefId,
            "credential":
                {
                "value": {
                    "username":username,
                    "password":password,
                    "tenant": tenant
                    }
                }
        };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createInvalidCredRef_Amazon(self):
        accessKey=utils.decodeCredential(aws_invalid_accessKey)
        secretKey=utils.decodeCredential(aws_invalid_secretKey)
        crefId="amazon-cref-001-invalid"

        body = {
            "crefId": crefId,
            "credential":
                {
                "value":{
                    "secretKey": secretKey,
                    "accesskey":accessKey
                    }
                }
            };
        resp, body = self.postCredentialRefs(body)
        return resp

    def createCredRef_Automation(self):
        accessKey=utils.decodeCredential(aws_testConnection_accessKey)
        secretKey=utils.decodeCredential(aws_testConnection_secretKey)

        body = {
            "crefId": "automationTesting-certificate",
            "credential":
                {
                    "value": {
                        "secretKey": secretKey,
                        "accesskey": accessKey
                    }
                }
        };
        resp, body = self.postCredentialRefs(body)
        return resp

    def deleteSystemuser(self, id):
        url = '%sauthorization/v1/systemusers/%s' % (self.endpoint, id)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.delete(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        return status, resp

    def getAllCredentials(self,id,headers):
        url = '%scb-credential-service/api/v2.0/accounts/%s/credentials' % (self.endpoint, id)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=headers)
        #print "Status is" + status
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def postAuditConfigValues(self, body):
        url = '%score/configuration/v1/configvalues' % (self.endpoint)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.post(url, json.dumps(body), headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getAuditCadf(self):
        url = '%score/audit/api/v2.1/logs?limit=1&format=cadf' % (self.endpoint)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=self.headers)
        #print "Status is" + status
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

    def advanceSearchByActionType_Limit(self, actiontype):
        url = '%score/audit/api/v2.1/logs?searchType=advanced&sortBy=initiatedDate&sort=desc&searchText=&startDate=&endDate=&subcomponent=[]&userId=[]&teamId=[]&component=[]&messageType=[\'%s\']&limit=10'% (self.endpoint, actiontype)
        logger.info("Rest URL:" + url)
        print ("Rest URL: " + url)
        status, resp = self.get(url, headers=self.headers)
        logger.info(pprint.pformat(resp))
        data = json.dumps(resp)
        return status, resp

    def getAccountById_SystemUser(self,id,headers):
        url = '%scb-credential-service/api/v2.0/accounts/%s' % (self.endpoint, id)
        print ("Rest URL: " + url)
        start = time.time()
        status, resp = self.get(url, headers=headers)
        #print "Status is" + status
        data = json.dumps(resp)
        logger.info(resp)
        return status, resp

