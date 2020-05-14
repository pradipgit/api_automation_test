from utils.RestClient import RestClient


class ManagementService:

    def __init__(self, host, route, headers=None):
        self.host = host.strip()
        self.headers = headers
        self.route = route.strip()

    def get_teams(self):
        rest_client = RestClient(self.host, self.route)
        response = RestClient.get(rest_client, headers=self.headers)
        return response["response"]

    def get_users_for_team(self, team):
        route = self.route+"/"+team
        rest_client = RestClient(self.host, route)
        response = RestClient.get(rest_client, headers= self.headers)
        return response["response"]

