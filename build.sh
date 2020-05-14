#!/bin/bash
#
#Link with Gocd Pipeline https://github.ibm.com/CloudBroker/gocd/blob/master/pipeline/qa/dal10/cb-qa-corex.gopipeline.json
#
set -o errexit
set -o nounset
namespace=$3
buildverison=$4
docker -v
docker ps -a | grep 'cam-core-api-automation' | awk '{print $1}' | xargs --no-run-if-empty docker rm -f
docker login -u "$1" -p "$2" ibmcb-docker-local.artifactory.swg-devops.com
docker pull ibmcb-docker-local.artifactory.swg-devops.com/cam-core-api-automation
docker run --rm -e "NAMESPACE=$namespace" -e "BUILDVERSION=$buildverison" -e CB_QA_COREX_API_KEY=$5 -e TOKEN_NAME=$6 -e AUTH_API_KEY1=$7 -e AUTH_API_KEY_SYSTEM_USER=$8 -e AWS_ACCESSKEY=$9 -e AWS_SECRETKEY=${10} -e AWS_S3_BUCKET=${11} -e AZURE_CLIENTID=${12} -e AZURE_SECRET=${13} -e AZURE_SUBSCRIPTION=${14} -e AZURE_OFFERID=${15} -e AZURE_TENANTID=${16} -e AZURE_DOMAIN=${17} -e GOOGLE_SERVICEKEY=${18} -e GOOGLE_PROJECT_NAME=${19} -e GOOGLE_PROJECT_ID=${20} -e GOOGLE_SERVICE_ACCOUNT_NAME=${21} -e IBM_USER_NAME=${22} -e IBM_API_KEY=${23} -e ICD_USER_NAME=${24} -e ICD_PASSWORD=${25} -e ICD_URL=${26} -e SNOW_USER_NAME=${27} -e SNOW_PASSWORD=${28} -e VRA_USER_NAME=${29} -e VRA_PASSWORD=${30} -e AZURE_BILLING_APPLICATION_SECRETS=${31} -e VERSION_TEST=${32} -e VAULT_ADAPTER_URL=${33} -e VAULT_ENDPOINT_URL=${34} -e SLACK_URL=${35} -e STORE_CICD_V2_API_KEY=${36} --name cam-core-api-automation ibmcb-docker-local.artifactory.swg-devops.com/cam-core-api-automation