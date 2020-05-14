from utils.RestClient import RestClient
from service.LookupService import LookupService

class AuditLogService():

    def __init__(self, host, route, headers=None, body= None):
            self.host = host.strip()
            self.headers = headers
            self.route = route.strip()
            self.body = body

    def get_audit_logs(self):
        
        rest_client = RestClient(self.host, self.route)
        response = RestClient.post(rest_client, self.body, self.headers)
        return response["response"]

    def get_audit_logs_v2(self):
        offset = self.body["query_list"][1]
        limit = self.body["query_list"][2]

        query = "?limit="+str(limit['limit'])+"&page="+str(offset['offSet'])
        route = self.route+query
        rest_client = RestClient(self.host, route)
        response = RestClient.get(rest_client, self.headers)
        return response["response"]