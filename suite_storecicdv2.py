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

class StoreCicdTestSuite():

    def testsObj(self,appurl, api_key):
        apiclient = api_client.APIClient(appurl, api_key)

         ################## Executing readOnly True testcases ##############################
        tests["prerequisite_readonly_true"] = importlib.import_module("prerequisite.prerequisites_readonly_true").prerequisite(apiclient)
        ###v2 accounts
        tests["amazonv2_readonly_true"] = importlib.import_module("account-service-v2.facet-provider.amazon.amazonv2_readonly_true").AmazonTest(apiclient)
        tests["azurev2_readonly_true"] = importlib.import_module("account-service-v2.facet-provider.azure.azurev2_readonly_true").AzureTest(apiclient)
        tests["googlev2_readonly_true"] = importlib.import_module("account-service-v2.facet-provider.google.googlev2_readonly_true").GoogleTest(apiclient)
        tests["ibmv2_readonly_true"] = importlib.import_module("account-service-v2.facet-provider.ibm.ibmv2_readonly_true").IbmTest(apiclient)
        tests["icdv2_readonly_true"] = importlib.import_module("account-service-v2.facet-provider.icd.icdv2_readonly_true").IcdTest(apiclient)
        tests["snowv2_readonly_true"] = importlib.import_module("account-service-v2.facet-provider.snow.snowv2_readonly_true").SnowTest(apiclient)
        tests["vrav2_readonly_true"] = importlib.import_module("account-service-v2.facet-provider.vra.vrav2_readonly_true").VraTest(apiclient)

        # Feature Tests
        tests["accountGet_readonly_true"] = importlib.import_module("account-service-v2.scenario-ui.account-get.account-get").AccountGet(apiclient)
        tests["accountPurpose_readonly_true"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose").AccountPurpose(apiclient)
        tests["purposeFilter_readonly_true"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose-filter").AccountPurpose(apiclient)

        # Currency
        tests["currencyConversion_readonly_true"] = importlib.import_module("Currency.currency").Currency(apiclient)
        #### Vault
        tests["vaultOnboarding_readonly_true"] = importlib.import_module("account-service-v2.scenario-onboarding.external-vault-onboarding.external-vault-onboarding").ExternalVaultOnboarding(apiclient)
        #Audit
        tests['AuditLogArchivePolicy_readonly_true'] = importlib.import_module("auditlog.auditlog-archive-policy.auditlog-archive-policy").AuditLogArchivePolicy(apiclient)


        # # ################### ------------- Executing readOnly False testcases ------------- ##############################
        #
        tests["prerequisite"] = importlib.import_module("prerequisite.prerequisites").prerequisite(apiclient)
        #v2 accounts
        tests["amazonv2"] = importlib.import_module("account-service-v2.facet-provider.amazon.amazonv2").AmazonTest(apiclient)
        tests["azurev2"] = importlib.import_module("account-service-v2.facet-provider.azure.azurev2").AzureTest(apiclient)
        tests["googlev2"] = importlib.import_module("account-service-v2.facet-provider.google.googlev2").GoogleTest(apiclient)
        tests["ibmv2"] = importlib.import_module("account-service-v2.facet-provider.ibm.ibmv2").IbmTest(apiclient)
        tests["icdv2"] = importlib.import_module("account-service-v2.facet-provider.icd.icdv2").IcdTest(apiclient)
        tests["snowv2"] = importlib.import_module("account-service-v2.facet-provider.snow.snowv2").SnowTest(apiclient)
        tests["vrav2"] = importlib.import_module("account-service-v2.facet-provider.vra.vrav2").VraTest(apiclient)

        # Feature Tests
        # tests["accountCredential"] = importlib.import_module("account-service-v2.scenario-ui.account-credential.account-credential_cicdV2").AccountCredential(apiclient)
        tests["accountGet"] = importlib.import_module("account-service-v2.scenario-ui.account-get.account-get").AccountGet(apiclient)
        tests["accountPurpose"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose").AccountPurpose(apiclient)
        tests["purposeFilter"] = importlib.import_module("account-service-v2.scenario-ui.account-purpose.account-purpose-filter").AccountPurpose(apiclient)

        ## Currency
        tests["currencyConversion"] = importlib.import_module("Currency.currency").Currency(apiclient)
        #### Vault
        tests["vaultOnboarding"] = importlib.import_module("account-service-v2.scenario-onboarding.external-vault-onboarding.external-vault-onboarding").ExternalVaultOnboarding(apiclient)
        #Audit
        tests['AuditLogArchivePolicy'] = importlib.import_module("auditlog.auditlog-archive-policy.auditlog-archive-policy").AuditLogArchivePolicy(apiclient)



        return tests
