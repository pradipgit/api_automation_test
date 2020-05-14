#!/bin/bash
#
# Copyright : IBM Corporation 2017, 2017
#
set -o nounset
set -o pipefail
set -o errexit

echo "[params]
post_to_bot = true
slack_result_channel = cldmx-core-testresult
slack_url = $SLACK_URL
token_name = $TOKEN_NAME
response_time = 3
thread_count = 1
test_object_name_in_suite = amazonv1
test_case = all
username = vijetkum@in.ibm.com
username_mt = 5df72e9c2214d9a3913baa11
cbqacorexapikey = $CB_QA_COREX_API_KEY
apikey = $NAMESPACE
minikubeapikey = $CB_QA_COREX_API_KEY
mtapikey = $CB_QA_COREX_API_KEY
premaster_apikey = $CB_QA_COREX_API_KEY
store_cicd_apikey = $STORE_CICD_V2_API_KEY

[param]
random_code_purpose = test1
random_code_purpose2 = test2

[urls]
asseturl = v2/api/services?page=1&size=10
operationurl = v2.0/operation
accessoperationurl = /catalog/v3/providers/softlayer/services/VIRTUALMACHINE_SERVICE
operationhistoryurl = /v2.0/operation
inventoryurlv3 = /v3/api/inventory/download
auditurl = /core/v2/audit/query
healthurl = /v2.0/operations/health
resourcestateurl = v2.0/resource
deleteurl = v2/api/services/deleteservices
auditpropertiesurl = /budgetmanagement/v1/budgetaryunits
viewbudgetpropertiesurl = /budgetmanagement/v1/serviceInstanceName/budget
viewpropertiesurl = /v2/api/services?page=1&size=10
componenturl = v3/api/services
order_historyurl = v3/api/order_history
orderurl = orders/v1/submit
importurl = /v3/api/inventory/import
listordersurl = /api/orders
viewpropertyurl = v2/api/services
editsoiurl = v3/api/services/
uploadfileurl = /inventory/v1/upload
importfileurl = /inventory/v1/import
importsettingsurl = /inventory/v1/import/setting
registryoperationsurl = /inventory/v1/operation
operationregistryurl = /inventory/v3/operations/definition
registryurl = /inventory/v3/operations/registry/?page=1&size=10&getAll='no'&filter=[{'field':'resourceType', 'value':'soc'}]
operationrequesturl = /inventory/v3/operations
operationconfigurl = /inventory/v1/registry/operations/opId/configs
extoperationurl = /inventory/v3/operations
operationsorderstatusurl = /inventory/v3/operations
asseturl_invalid_version = /api12/services?page=1&size=10
operationurl_invalid_version = /v2.0.1.0/operation
operationhistoryurl_invalid_version = /v2.0.1.0/operation
inventoryurlv3_invalid = /v3/api/inventory/download/invalid
auditurl_invalid_version = /core/v2.100.1.0/audit/query
healthurl_invalid_version = /v2.100.1.0/operations/health
resourcestateurl_invalid_version = /v1.0.1.1/resource
deleteurl_invalid_version = /v2/api/services/deleteservices1
viewpropertiesurl_invalid_version = /v2.100.z/api/services?page=1&size=1
viewpropertiesurl_invalid = /v2/api/services?123page=1&size=10&searchText=&sortBy=ProvisionDate&sortOrder=desc&filterBy=status:Active
componenturl_invalid_version = /v3.3.1/api/services
order_history_invalidurl = /v2/api/order_history/invalid
import_invalidurl = /v33/api123/inventory/import/incorrect
viewpropertyurl_invalidurl = /v2.5/api/services
asseturl_invalidurl = /api/services
registryoperationsurl_invalid_version = /inventory/v1.0.2/operation
registryoperations_invalidurl = /inventory/v1/
operationregistryurl_invalidurl = /inventory/v3/operations/definition?type=SOL
operationregistryurl_invalid_version = /inventory/v33.1/operations/definition
registryurl_invalid_version = /inventory/v1/operations/registry/?page=1&size=10&getAll='no'&filter=[{'field':'resourceType', 'value':'soc'}]
registryurl_invalidurl = /inventory/v3/operations/resource/registry/?page=1&size=10&getAll='no'&filter=[{'field':'resourceType', 'value':'soc'}]
operationrequesturl_invalidversion = /inventory/v3.1/operations
operationrequesturl_invalidurl = /inventory/resource/v3.1/operations
operationconfigurl_invalidversion = /inventory/v3/registry/operations/opId/configs
operationconfigurl_invalidurl = /inventory/v1/registry/operations/opId/configs123
extoperationurl_invalidurl = /inventory/v1/registry/operations/opId/configs123
extoperationurl_invalidversion = /inventory/v1/registry/operations/opId/configs12321331
operationsorderstatusurl_invalidversion = /inventory/v1/operations

[defect]
open_defects =

[authorization]
username1 = vijetkum@in.ibm.com
apikey1 = $AUTH_API_KEY1
username_systemuser = vijethkumarbs
username_systemuser_cicd = vijethkumarbs_cicd
apikey_systemuser = $AUTH_API_KEY_SYSTEM_USER
apikey_systemuser_cicd = $AUTH_API_KEY_SYSTEM_USER

[aws]
accesskey = $AWS_ACCESSKEY
secretkey = $AWS_SECRETKEY
s3bucket = $AWS_S3_BUCKET

[azure]
clientid = $AZURE_CLIENTID
secret = $AZURE_SECRET
subscriptionid = $AZURE_SUBSCRIPTION
offerid = $AZURE_OFFERID
tenantid = $AZURE_TENANTID
domain = $AZURE_DOMAIN

[google]
servicekey = $GOOGLE_SERVICEKEY
projectname = $GOOGLE_PROJECT_NAME
projectid = $GOOGLE_PROJECT_ID
serviceaccountname = $GOOGLE_SERVICE_ACCOUNT_NAME
bucket = $AWS_S3_BUCKET

[ibm]
username = $IBM_USER_NAME
apikey = $IBM_API_KEY

[icd]
username = $ICD_USER_NAME
password = $ICD_PASSWORD
url = $ICD_URL

[snow]
username = $SNOW_USER_NAME
password = $SNOW_PASSWORD

[vra]
username = $VRA_USER_NAME
password = $VRA_PASSWORD

[azureBilling]
applicationsecret = $AZURE_BILLING_APPLICATION_SECRETS

[googlebilling]
servicekey = $GOOGLE_SERVICEKEY
dataset = $GOOGLE_PROJECT_NAME
bucket = $AWS_S3_BUCKET

[snowBilling]
username = $SNOW_USER_NAME
password = $SNOW_PASSWORD
url = $ICD_URL
version = $VERSION_TEST

[vraBilling]
username = $SNOW_USER_NAME
password = $SNOW_PASSWORD
tenant = $SNOW_USER_NAME
endpointversion = $VERSION_TEST
url = $ICD_URL

[awsInvalid]
accesskey = $SNOW_USER_NAME
secretkey = $SNOW_PASSWORD

[awsTestConnection]
accesskey = $AWS_ACCESSKEY
secretkey = $AWS_SECRETKEY

[vault]
vault_adapter_url = $VAULT_ADAPTER_URL
vault_endpoint_url = $VAULT_ENDPOINT_URL

[order]
order_number1 = 4OWXN9Z8
order_number2 = ENLW6PRA
order_number3 = DHAHR9G3
order_number4 = VYA2CZT8
order_numbervraviewer = DTDUD7KO
order_numbervraoperations = 2HYCS6RK
order_numbervracrud = D9PZRLHI

[orderstatus]
order_number1_status = completed
order_number2_status = completed
order_number3_status = notfound
order_number4_status = notfound
order_numbervraviewer_status = notfound
order_numbervraoperations_status = completed
order_numbervracrud_status = completed

[resources]
service_id1 = da6db7167d5ce4cb300e2c6cb6365e32
resource_id1 = 9f638c6e-4f17-4112-bddc-b54b6563012b
service_id2 = aa91794568d30d709c77b2e7f616f37e
resource_id2 = d2273965-d4c2-4781-a682-e212a3e8809b
service_id3 = notfound
resource_id3 = notfound
service_id4 = notfound
resource_id4 = notfound
service_id5 = notfound
resource_id5 = notfound
provider = vra
neg_tests_soi_delete_sid = 9733dd16761b8f86a4581499c9028694
neg_tests_soi_delete_sid2 = 8733dd16761b8f86a4581499c9028694
service_id6 = f4723efaed73ba2d45d4e6b730ba8328
resource_id6 = 2c37947c-483d-495f-860d-408bed87e916
service_id7 = f4723efaed73ba2d45d4e6b730baa013
resource_id7 = eb17295d-bee1-43c2-b8e7-849a882f6818
service_id10 = BHFE20NWTE
service_id12 = 0WQSD7Z793
resource_id12 = ap-northeast-1
service_id11 = WDG0GX1VR1
resource_id11 = 7bd72d48-acd9-49a3-9a9f-2cf98ae03d79
service_id13 = 6CPW7V91TB
resource_id13 = 64caccf3-b508-41e7-92ed-d7ed95b32621
service_id14 = AGTYDC1G0X
resource_id14 = VirtualMachine$$~$$ttestfasdfasc1$$~$$testresoirce" > testdata1.conf


cp testdata1.conf /cam-core-api-automation/testdata.conf

python auto_run.py ${NAMESPACE} ${BUILDVERSION}
#to run the quality analysis tool
#cd quality-analysis-tool
#python -m pip install --user virtualenv
#python -m virtualenv env
#source env/bin/activate
#pip install -r requirements.txt
#python ReportGenerator.py ${NAMESPACE}
