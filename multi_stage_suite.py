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

class MultiTenancy():

    def testsObj(self,appurl, api_key):
        apiclient = api_client.APIClient(appurl, api_key)

         ################## Executing readOnly True testcases ##############################
        tests["prerequisite"] = importlib.import_module("prerequisite.prerequisites_readonly_true").prerequisite(apiclient)
        ###### Rules validate- account & credential

        tests["amazonv2"] = importlib.import_module("account-service-v2.facet-provider.amazon.amazonv2_readonly_true").AmazonTest(apiclient)
        tests["azurev2"] = importlib.import_module("account-service-v2.facet-provider.azure.azurev2_readonly_true").AzureTest(apiclient)
        tests["googlev2"] = importlib.import_module("account-service-v2.facet-provider.google.googlev2_readonly_true").GoogleTest(apiclient)
        tests["ibmv2"] = importlib.import_module("account-service-v2.facet-provider.ibm.ibmv2_readonly_true").IbmTest(apiclient)
        tests["icdv2"] = importlib.import_module("account-service-v2.facet-provider.icd.icdv2_readonly_true").IcdTest(apiclient)
        tests["snowv2"] = importlib.import_module("account-service-v2.facet-provider.snow.snowv2_readonly_true").SnowTest(apiclient)
        tests["vrav2"] = importlib.import_module("account-service-v2.facet-provider.vra.vrav2_readonly_true").VraTest(apiclient)

        # # Feature Tests
        tests["accountAdvanceSearch"] = importlib.import_module("account-service-v2.scenario-ui.account-advance-search.account-advance-search").AccountAdvanceSearch(apiclient)
        tests["accountFilter"] = importlib.import_module("account-service-v2.scenario-ui.account-filter.account-filter").AccountFilter(apiclient)
        tests["accountGet"] = importlib.import_module("account-service-v2.scenario-ui.account-get.account-get").AccountGet(apiclient)
        tests["accountPagination"] = importlib.import_module("account-service-v2.scenario-ui.account-pagination.account-pagination").AccountPagination(apiclient)
        tests["accountPurpose"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose").AccountPurpose(apiclient)
        tests["accountSearch"] = importlib.import_module("account-service-v2.scenario-ui.account-search.account-search").AccountSearch(apiclient)
        tests["accountSort"] = importlib.import_module("account-service-v2.scenario-ui.account-sort.account-sort").AccountSort(apiclient)
        tests["accountTestConnection"] = importlib.import_module("account-service-v2.scenario-ui.test-connection.test-connection_readonly_true").AccountTestConnection(apiclient)
        tests["purposeFilter"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose-filter").AccountPurpose(apiclient)

        #Audit
        tests['auditlogAdvanceSearch'] = importlib.import_module("auditlog.auditlog-advance-search.auditlog-advance-search").AuditlogAdvanceSearch(apiclient)

        tests['AuditLogDownload'] = importlib.import_module(
            "auditlog.auditlog-download.auditlog-download").AuditLogDownload(apiclient)

        tests['AuditLogUI'] = importlib.import_module("auditlog.auditlog-ui.auditlog-ui").AuditLogUI(apiclient)

        ################ ------------- Executing readOnly False testcases ------------- ##############################
        tests["prerequisite_readonlyFalse"] = importlib.import_module("prerequisite.prerequisites").prerequisite(apiclient)
        #v2 accounts
        tests["amazonv2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.amazon.amazonv2").AmazonTest(apiclient)
        tests["azurev2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.azure.azurev2").AzureTest(apiclient)
        tests["googlev2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.google.googlev2").GoogleTest(apiclient)
        tests["ibmv2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.ibm.ibmv2").IbmTest(apiclient)
        tests["icdv2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.icd.icdv2").IcdTest(apiclient)
        tests["snowv2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.snow.snowv2").SnowTest(apiclient)
        tests["vrav2_readonlyFalse"] = importlib.import_module("account-service-v2.facet-provider.vra.vrav2").VraTest(apiclient)


        return tests
