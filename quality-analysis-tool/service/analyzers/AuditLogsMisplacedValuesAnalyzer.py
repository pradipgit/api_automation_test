import service.constant as constant
import pandas as pd


class AuditLogsMisplacedValuesAnalyzer:

    def __int__(self):
        pass

    def generate(self, audit_logs):
        insights = self.get_insights(audit_logs)

        data_insights = self.prepare_data_for_report(insights)

        return  data_insights

    def get_insights(self, audit_logs):
        users = []
        teams = []
        components = []
        sub_components = []

        for log in audit_logs:
            users.append(log[constant.USER_ATTRIBUTE])
            teams.append(log[constant.TEAM_ATTRIBUTE])
            components.append(log[constant.COMPONENT_ATTRIBUTE])
            sub_components.append(log[constant.SUB_COMPONENT_ATTRIBUTE])

        users_series = pd.Series(users).replace('', 'unknown', regex=True)
        teams_series = pd.Series(teams).replace('', 'unknown', regex=True)
        components_series = pd.Series(components).replace('', 'unknown', regex=True)
        sub_components_series = pd.Series(sub_components).replace('', 'unknown', regex=True)

        try:
            users_in_teams = users_series.isin(teams_series).value_counts()[True]
        except KeyError:
            users_in_teams = 0

        try:
            users_in_components = users_series.isin(components_series).value_counts()[True]
        except KeyError:
            users_in_components = 0

        try:
            teams_in_users = teams_series.isin(users_series).value_counts()[True]
        except KeyError:
            teams_in_users = 0

        try:
            teams_in_components = teams_series.isin(components_series).value_counts()[True]
        except KeyError:
            teams_in_components = 0

        try:
            comp_in_sub_comp = components_series.isin(sub_components_series).value_counts()[True]
        except KeyError:
            comp_in_sub_comp = 0

        try:
            sub_comp_in_comp = sub_components_series.isin(components_series).value_counts()[True]
        except KeyError:
            sub_comp_in_comp = 0

        insight = [len(audit_logs), users_in_teams, users_in_components, teams_in_users, teams_in_components, comp_in_sub_comp, sub_comp_in_comp]

        return insight

    def prepare_data_for_report(self, insights):
        pd.set_option('display.max_colwidth', -1)

        columns = ['Total Number Of Records Analyzed',
                          'UserId appearing in TeamId',
                           'UserId appearing in ComponentId',
                           'TeamId appearing in UserId',
                           'TeamId appearing in ComponentId',
                            'ComponentId appearing in Sub-ComponentId',
                           'Sub-ComponentId appearing in ComponentId']

        data_frame = pd.DataFrame(insights, index=columns)
        return data_frame

