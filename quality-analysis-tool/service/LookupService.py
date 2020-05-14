import service.constant as constant
import json
import os
from service.ManagementService import ManagementService


class LookupService:

    def __init__(self, config):
        self.config = config

    def update_teams_and_users(self, teams, update_to_file):

        teams_lookup = []
        users_lookup = []

        headers = {'apikey': str(self.config['API_KEY']), 'username': str(self.config['API_USERNAME'])}
        management_service = ManagementService(str(self.config['MANAGEMENT_SERVICE_HOST']), (str(self.config['USER_MANAGEMENT_SERVICE_ROUTE'])), headers)

        for team in teams:
            try:
                if team.has_key('teamcode'):
                    teams_lookup.append(str(team['teamcode']))
                    team_users = self.geta_users_for_team(management_service, str(team['teamcode']))
                    users_lookup = users_lookup + team_users
            except UnicodeEncodeError:
                print ('UnicodeEncodeError fot Team, Skipping the record .... ')

        actuals = {}
        actuals[constant.TEAM_ATTRIBUTE] = teams_lookup
        actuals[constant.USER_ATTRIBUTE] = users_lookup

        file_directory = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(file_directory, update_to_file)

        with open(filename, 'w') as outfile:
            json.dump(actuals, outfile)

    def geta_users_for_team(self, service, team_name):
        team_users = []
        users = service.get_users_for_team(team_name)
        if users is not None:
            for user in users:
                try:
                    if user.has_key('userid'):
                        team_users.append(str(user['userid']))
                except AttributeError:
                    print('User Attribute Error for User:' + user)

        return team_users

    def get_teams_and_users(self):
        file_directory = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(file_directory, constant.LOOKUP_FILE_NAME)

        with open(filename) as json_file:
            data = json.load(json_file)

        return data[constant.TEAM_ATTRIBUTE], data[constant.USER_ATTRIBUTE]

    def get_content(self, filename, property_key):
        file_directory = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(file_directory, filename)

        with open(filename) as json_file:
            data = json.load(json_file)

        return data[property_key]

