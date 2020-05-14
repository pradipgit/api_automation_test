import requests
import json


class RestClient:
    
    def __init__(self, host, route):
        self.url = host + route

    def post_to_webhook(self, body, headers):
        requests.post(self.url, json=body, headers=headers)

    def post(self, body, headers):
       
        api_response = requests.post(self.url, json=body, headers=headers)
        response = { 
            "response": json.loads(api_response.content),
            "statuscode": api_response.status_code
            }

        return response

    def get(self, headers):
        api_response = requests.get(self.url, headers=headers)

        if api_response.status_code not in (400, 404):
            response = {
                "response": json.loads(api_response.content),
                "statuscode": api_response.status_code
            }
        else:
            response = {
                'response': None,
                "statuscode": api_response.status_code
            }
        return response
