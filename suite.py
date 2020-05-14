import importlib
import configparser
import api_client
import utils
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import time
import sys
from collections import OrderedDict

tests = OrderedDict()

class TestSuite():

    # def __init__(self,appurl,api_key):
    #     self.appurl = appurl
    #     self.api_key=api_key


    def testsObj(self,appurl, api_key):
        apiclient = api_client.APIClient(appurl, api_key)

         ############### Executing readOnly True testcases ##############################
        tests["prerequisite"] = importlib.import_module("prerequisite.prerequisites_readonly_true").prerequisite(apiclient)
        ##### Rules validate- account & credential
        tests["ruleValidate"] = importlib.import_module("account-service-v2.rules-api.rule-validation").RuleValidation(apiclient, appurl)
        tests["ruleAPI"] = importlib.import_module("account-service-v2.rules-api.rules-api").RulesAPI(apiclient)
        ##v2 accounts
        tests["amazonv2"] = importlib.import_module("account-service-v2.facet-provider.amazon.amazonv2_readonly_true").AmazonTest(apiclient)
        tests["azurev2"] = importlib.import_module("account-service-v2.facet-provider.azure.azurev2_readonly_true").AzureTest(apiclient)
        tests["googlev2"] = importlib.import_module("account-service-v2.facet-provider.google.googlev2_readonly_true").GoogleTest(apiclient)
        tests["ibmv2"] = importlib.import_module("account-service-v2.facet-provider.ibm.ibmv2_readonly_true").IbmTest(apiclient)
        tests["icdv2"] = importlib.import_module("account-service-v2.facet-provider.icd.icdv2_readonly_true").IcdTest(apiclient)
        tests["snowv2"] = importlib.import_module("account-service-v2.facet-provider.snow.snowv2_readonly_true").SnowTest(apiclient)
        tests["vrav2"] = importlib.import_module("account-service-v2.facet-provider.vra.vrav2_readonly_true").VraTest(apiclient)

        # # Feature Tests
        tests["accountAdvanceSearch"] = importlib.import_module("account-service-v2.scenario-ui.account-advance-search.account-advance-search").AccountAdvanceSearch(apiclient)
        tests["accountCredential"] = importlib.import_module("account-service-v2.scenario-ui.account-credential.account-credential").AccountCredential(apiclient)
        tests["accountFilter"] = importlib.import_module("account-service-v2.scenario-ui.account-filter.account-filter").AccountFilter(apiclient)
        tests["accountGet"] = importlib.import_module("account-service-v2.scenario-ui.account-get.account-get").AccountGet(apiclient)
        tests["accountPagination"] = importlib.import_module("account-service-v2.scenario-ui.account-pagination.account-pagination").AccountPagination(apiclient)
        tests["accountPurpose"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose").AccountPurpose(apiclient)
        tests["accountSearch"] = importlib.import_module("account-service-v2.scenario-ui.account-search.account-search").AccountSearch(apiclient)
        tests["accountSort"] = importlib.import_module("account-service-v2.scenario-ui.account-sort.account-sort").AccountSort(apiclient)
        tests["accountTestConnection"] = importlib.import_module("account-service-v2.scenario-ui.test-connection.test-connection_readonly_true").AccountTestConnection(apiclient)
        tests["purposeFilter"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose-filter").AccountPurpose(apiclient)

        # Currency
        tests["currencyConversion"] = importlib.import_module("Currency.currency").Currency(apiclient)
        # #### Vault
        tests["vaultOnboarding"] = importlib.import_module("account-service-v2.scenario-onboarding.external-vault-onboarding.external-vault-onboarding").ExternalVaultOnboarding(apiclient)
        #Audit

        tests['AuditLogUI'] = importlib.import_module("auditlog.auditlog-ui.auditlog-ui").AuditLogUI(apiclient)
        tests['auditlogAdvanceSearch'] = importlib.import_module("auditlog.auditlog-advance-search.auditlog-advance-search").AuditlogAdvanceSearch(apiclient)
        tests['AuditLogArchivePolicy'] = importlib.import_module(
            "auditlog.auditlog-archive-policy.auditlog-archive-policy").AuditLogArchivePolicy(apiclient)

        tests['AuditLogArchive'] = importlib.import_module(
            "auditlog.auditlog-archive.auditlog-archive").AuditLogArchive(apiclient)

        tests['AuditLogDownload'] = importlib.import_module(
            "auditlog.auditlog-download.auditlog-download").AuditLogDownload(apiclient)

        tests['latest_codeChanges'] = importlib.import_module("latestApiChanges.latestcodechanges_readonly_true").lastetCodeChanges(
            apiclient)

        tests['validate_result'] = importlib.import_module("account-service-v2.validation-results.validation-result-post").ValidationResult(apiclient)
        # store credential validation result
        tests['ValidationResultTest'] = importlib.import_module("account-service-v2.rules-api.credential-val-result.validation-result").ValidationResultTest(apiclient)
        tests['ValidationResultGetTest'] = importlib.import_module("account-service-v2.validation-result-api.validation-result-get").ValidationResultGetTest(apiclient)
        ################## ------------- Executing readOnly False testcases ------------- ##############################
        tests["prerequisite_readonlyFalse"] = importlib.import_module("prerequisite.prerequisites").prerequisite(apiclient)
        ##v2 accounts
        tests["amazonv2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.amazon.amazonv2").AmazonTest(apiclient)
        tests["azurev2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.azure.azurev2").AzureTest(apiclient)
        tests["googlev2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.google.googlev2").GoogleTest(apiclient)
        tests["ibmv2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.ibm.ibmv2").IbmTest(apiclient)
        tests["icdv2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.icd.icdv2").IcdTest(apiclient)
        tests["snowv2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.snow.snowv2").SnowTest(apiclient)
        tests["vrav2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.vra.vrav2").VraTest(apiclient)

        # Feature Tests
        tests["accountAdvanceSearch_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.account-advance-search.account-advance-search").AccountAdvanceSearch(apiclient)
        tests["accountCredential_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.account-credential.account-credential").AccountCredential(apiclient)
        tests["accountFilter_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.account-filter.account-filter").AccountFilter(apiclient)
        tests["accountGet_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.account-get.account-get").AccountGet(apiclient)
        tests["accountPagination_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.account-pagination.account-pagination").AccountPagination(apiclient)
        tests["accountPurpose_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose").AccountPurpose(apiclient)
        tests["accountSearch_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.account-search.account-search").AccountSearch(apiclient)
        tests["accountSort_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.account-sort.account-sort").AccountSort(apiclient)
        tests["accountTestConnection_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.test-connection.test-connection").AccountTestConnection(apiclient)
        tests["purposeFilter_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose-filter").AccountPurpose(apiclient)

        tests['auditlogAdvanceSearch_readonlyFalse'] = importlib.import_module("auditlog.auditlog-advance-search.auditlog-advance-search").AuditlogAdvanceSearch(apiclient)
        tests['AuditLogUI_readonlyFalse'] = importlib.import_module("auditlog.auditlog-ui.auditlog-ui").AuditLogUI(apiclient)
        tests['AuditLogDownload_readonlyFalse'] = importlib.import_module("auditlog.auditlog-download.auditlog-download").AuditLogDownload(apiclient)
        #### Vault
        tests["vaultOnboarding_readonlyFalse"] = importlib.import_module("account-service-v2.scenario-onboarding.external-vault-onboarding.external-vault-onboarding").ExternalVaultOnboarding(apiclient)
        tests['latest_codeChanges_readonlyFalse'] = importlib.import_module("latestApiChanges.latestcodechanges").lastetCodeChanges(apiclient)
        tests['system_user'] = importlib.import_module("systemuser.systemuser").systemuser(apiclient)


        ##E2E Test cases
        # tests["vrav2"] = importlib.import_module("account-service-v2.scenario-integration.inventory-integration.vrae2e").VRA_Tests(apiclient)
        # tests["amazone2e"] = importlib.import_module("account-service-v2.scenario-integration.inventory-integration.amazone2e").Amazon_Tests(apiclient)
        # tests["softlayere2e"] = importlib.import_module("account-service-v2.scenario-integration.inventory-integration.softlayere2e").Softlayer_Tests(apiclient)
        # tests["azuree2e"] = importlib.import_module("account-service-v2.scenario-integration.inventory-integration.azuree2e").AZURE_Tests(apiclient)


        return tests
