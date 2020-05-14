import pandas as pd
import simplejson as Json
import service.constant as constant
from service.validators.AuditLogValidator import AuditLogValidator
from decimal import *


class AuditLogCorrectnessReportAnalyzer:

    def __init__(self, rules, weights):
        self.rules = rules
        self.weights = weights

    def generate(self, audit_logs):

        scored_logs = self.validate_and_score(audit_logs)

        formatted_logs = self.get_short_insights_for_report(scored_logs)

        ds_logs = self.prepare_data_for_report(formatted_logs)

        return ds_logs

    def validate_and_score(self, audit_logs):

        audit_log_validator = AuditLogValidator()

        component = []
        sub_component = []

        validation_errors = []
        score = []

        users = []
        teams = []
        comps = []
        sub_comps = []
        actions = []

        for log in audit_logs:
            validation_result = audit_log_validator.validate(log, self.rules)
            score_result, user, team, comp, sub_comp = audit_log_validator.score(validation_result, 1/Decimal(len(self.rules)), self.weights)

            score.append(round(score_result, 2))
            users.append(user)
            teams.append(team)
            comps.append(comp)
            sub_comps.append(sub_comp)

            if log.has_key(constant.COMPONENT_ATTRIBUTE):
                component.append(log[constant.COMPONENT_ATTRIBUTE])
            else:
                component.append('')

            if log.has_key(constant.SUB_COMPONENT_ATTRIBUTE):
                sub_component.append(log[constant.SUB_COMPONENT_ATTRIBUTE])
            else:
                sub_component.append('')

            if log.has_key(constant.ACTION_ATTRIBUTE):
                actions.append(log[constant.ACTION_ATTRIBUTE])
            else:
                actions.append('')

            json_errors = Json.dumps(validation_result, default=lambda x: x.__dict__)
            validation_errors.append(json_errors)

            continue

        logs = {
            "users": users,
            "teams": teams,
            "comps": comps,
            "subcomps": sub_comps,
            "actions": actions
        }

        return logs

    def get_short_insights_for_report(self, logs):
        pd.set_option('display.max_colwidth', -1)

        data_frame = pd.DataFrame(logs, columns=['users', 'teams', 'comps', 'subcomps', 'actions'])
        data_frame = data_frame.replace('', 'unknown', regex=True)

        valid_users = data_frame[data_frame['users'] == 1]
        invalid_users = data_frame[data_frame['users'] == 3]

        valid_teams = data_frame[data_frame['teams'] == 1]
        invalid_teams = data_frame[data_frame['teams'] == 3]

        missing_components = data_frame[data_frame['comps'] == 2]
        valid_components = data_frame[data_frame['comps'] == 1]
        invalid_components = data_frame[data_frame['comps'] == 3]

        missing_subcomponents = data_frame[data_frame["subcomps"] == 2]
        valid_subcomponents = data_frame[data_frame['subcomps'] == 1]
        invalid_subcomponents = data_frame[data_frame['subcomps'] == 3]

        missing_actions = data_frame[data_frame["actions"] == 'NAN']
        actions = data_frame.actions.unique()

        insight = [len(invalid_users),
                   len(invalid_teams),
                   len(invalid_components), len(missing_components),
                   len(invalid_subcomponents),len(missing_subcomponents),
                   len(missing_actions), len(actions)]

        return insight

    def prepare_data_for_report(self, logs):
        pd.set_option('display.max_colwidth', -1)

        columns = ['Logs with Invalid UserId',
                   'Audit-Logs with Invalid TeamId',
                   'Audit-Logs with Invalid Component-Name', 'Logs with Missing Component-Name',
                   'Audit-Logs with Invalid SubComponent-Name', 'Logs with Missing SubComponent-Name',
                   'Audit-Logs with Missing Actions', 'Number of Unique Actions']

        data_frame = pd.DataFrame(logs,   index=columns)
        return data_frame