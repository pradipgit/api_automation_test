# importing the required libraries
import requests 
import json
import uuid
import time
import constants

def callCertificateApis(thread_id, uuid_arg, tenant):
    postCertificateApiUrl = "/certificaterefs"
    certificateApiUrl = "/certificaterefs/" + uuid_arg
    put_cred = {
        'crefId': uuid_arg,
        'certificate': {
            "value": {
                "access_key": "0000000000000" + str(thread_id),
                "secret_key": "0000000000000" + str(thread_id)
            }
        }
    }
    post_cred = {
        'crefId': uuid_arg,
        'certificate': {
            'value' : {
                "access_key": "354634634564" + str(thread_id),
                "secret_key": "lkjasdlkfjalksdj" + str(thread_id)
            }
        }
    }
    addMasterKey(tenant)
    callPostApi(tenant, uuid_arg, thread_id, post_cred, postCertificateApiUrl)
    callGetApi(tenant, uuid_arg, thread_id, post_cred, certificateApiUrl)
    callPutApi(tenant, uuid_arg, thread_id, put_cred, certificateApiUrl)
    callGetApi(tenant, uuid_arg, thread_id, put_cred, certificateApiUrl)
    callDeleteApi(tenant, uuid_arg, certificateApiUrl)

def callCredentialApis(thread_id, uuid_arg, tenant):
    postApiUrl = "/credentialrefs" 
    apiUrl = "/credentialrefs/" + uuid_arg
    put_cred = {
        'crefId': uuid_arg,
        'credential': {
            "value": {
                "access_key": "0000000000000" + str(thread_id),
                "secret_key": "0000000000000" + str(thread_id)
            }
        }
    }
    post_cred = {
        'crefId': uuid_arg,
        'credential': {
            'value' : {
                "access_key": "354634634564" + str(thread_id),
                "secret_key": "lkjasdlkfjalksdj" + str(thread_id)
            }
        }
    }
    addMasterKey(tenant)
    callPostApi(tenant, uuid_arg, thread_id, post_cred, postApiUrl)
    callGetApi(tenant, uuid_arg, thread_id, post_cred, apiUrl)
    callPutApi(tenant, uuid_arg, thread_id, put_cred, apiUrl)
    callGetApi(tenant, uuid_arg, thread_id, put_cred, apiUrl)
    callDeleteApi(tenant, uuid_arg, apiUrl)

def serviceCallIntegration(thread_id, uuid_arg, tenant):
    print(thread_id)

    callCredentialApis(thread_id, uuid_arg, tenant)
    callCertificateApis(thread_id, uuid_arg, tenant)

def addMasterKey(tenant):
    print("Adding master key")
    headers = { 'Content-Type':'application/json', 'tenant-uuid' : tenant}
    body={
        "key": "55HNZ05V3XILSJN7DKZJ3P2XL5LMY7QP"
    }
    # sending add master key request and saving response as response object 
    res =requests.post(url = constants.MONGO_VAULT_URL, json = body, headers = headers)
    print(res.json())

def compareRespose(response, api_response):
    return response == api_response

def callPostApi(tenant, uuid, thread_id, payload, apiUrl):
    print("Inside POST api call")
    # defining the api-endpoint 
    API_ENDPOINT = constants.MONGO_VAULT_ADAPTER_URL + apiUrl

    data = {
        "isReadOnly": "false",
        "vault_adapter_url": "http://cb-mongo-vault-adapter:5880",
        "vault_endpoint_url": "http://cb-mongo-vault:8220"
    }

    headers = { 'vaultConfig' : json.dumps(data), 'tenant-uuid' : tenant}

    # sending POST request and saving response as response object 
    POST_RES = requests.post(url = API_ENDPOINT, json = payload, headers = headers) 
    # extracting response text 
    print("Result for POST is :%s ", str(POST_RES.json()))
    if payload.get('credential'):
        assert (compareRespose(uuid, POST_RES.json()["credrefId"]) and compareRespose(200, POST_RES.json()['status_code']))
    else:
        assert (compareRespose(uuid, POST_RES.json()["crefId"]) and compareRespose(200, POST_RES.json()['status_code']))

def callPutApi(tenant, uuid, thread_id, payload, apiUrl):
    print("Inside PUT api call")
    # defining the api-endpoint
    API_ENDPOINT = constants.MONGO_VAULT_ADAPTER_URL + apiUrl
    data = {
        "isReadOnly": "false",
        "vault_adapter_url": "http://cb-mongo-vault-adapter:5880",
        "vault_endpoint_url": "http://cb-mongo-vault:8220"
    }

    headers = { 'vaultConfig' : json.dumps(data), 'tenant-uuid' : tenant}

    # sending PUT request and saving response as response object 
    putRes = requests.put(url = API_ENDPOINT, json = payload, headers = headers, params = uuid) 

    # extracting response text 
    print("Result for PUT is :%s ", str(putRes.json())) 
    if payload.get('credential'):
        assert (compareRespose(uuid, putRes.json()["credrefId"]) and compareRespose(200, putRes.json()['status_code']))
    else:
        assert (compareRespose(uuid, putRes.json()["crefId"]) and compareRespose(200, putRes.json()['status_code']))

def callGetApi(tenant, uuid, thread_id, payload, apiUrl):
    print("Inside GET api call")
    # defining the api-endpoint
    API_ENDPOINT = constants.MONGO_VAULT_ADAPTER_URL + apiUrl
    data = {
        "isReadOnly": "false",
        "vault_adapter_url": "http://cb-mongo-vault-adapter:5880",
        "vault_endpoint_url": "http://cb-mongo-vault:8220"
    }

    headers = { 'vaultConfig' : json.dumps(data), 'tenant-uuid' : tenant}

    # sending GET request and saving response as response object 
    getRes = requests.get(url = API_ENDPOINT, headers = headers) 

    # extracting response text 
    print("Result for GET is :%s ", str(getRes.json()))
    if payload.get('credential'):
        assert (compareRespose( payload["credential"]["value"], getRes.json()["credential"]["value"]) and compareRespose(200, getRes.json()['status_code']))
    else:
        assert (compareRespose( payload["certificate"]["value"], getRes.json()["certificate"]["value"]) and compareRespose(200, getRes.json()['status_code']))

def callDeleteApi(tenant, uuid, apiUrl):
    print("Inside DELETE api call")
    # defining the api-endpoint
    API_ENDPOINT = constants.MONGO_VAULT_ADAPTER_URL + apiUrl

    data = {
        "isReadOnly": "false",
        "vault_adapter_url": "http://cb-mongo-vault-adapter:5880",
        "vault_endpoint_url": "http://cb-mongo-vault:8220"
    }

    headers = { 'vaultConfig' : json.dumps(data), 'tenant-uuid' : tenant}

    # sending DELETE request and saving response as response object 
    deleteRes = requests.delete(url = API_ENDPOINT, headers = headers) 

    # extracting response text 
    print("Result for DELETE is :%s ", str(deleteRes.text))
    assert compareRespose(True, deleteRes.ok)