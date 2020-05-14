from service.validators.AuditLogValidator import AuditLogValidator
import pandas as pd
import simplejson as Json
from decimal import *


class AuditLogSummaryAnalyzer:

    def __init__(self, rules, weights):
        self.rules = rules
        self.weights = weights

    def generate(self, audit_logs):

        scored_logs = self.validate_and_score(audit_logs)

        formatted_logs = self.prepare_data_for_report(scored_logs)

        return formatted_logs


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
        count = []

        for log in audit_logs:
            validation_result = audit_log_validator.validate(log, self.rules)
            score_result, user, team, comp, subcomp = audit_log_validator.score(validation_result, 1/Decimal(len(self.rules)), self.weights)

            score.append(round(score_result, 2))
            users.append(user)
            teams.append(team)
            comps.append(comp)
            sub_comps.append(subcomp)

            if log.has_key("component-attr"):
                component.append(log["component-attr"])
            else:
                component.append('')

            if log.has_key("sub-component-attr"):
                sub_component.append(log["sub-component-attr"])
            else:
                sub_component.append('')

            error = Json.dumps(validation_result, default=lambda x: x.__dict__)
            validation_errors.append(error)

            count.append(1)

            continue

        logs = {
            "score": score,
            "component_name": component,
            "users": users,
            "teams": teams,
            "comps": comps,
            "subcomps": sub_comps,
            "records": count,
            "total_count": len(audit_logs)
        }

        return logs

    @staticmethod
    def prepare_data_for_report(logs):
        pd.set_option('display.max_colwidth', -1)

        data_frame = pd.DataFrame(logs, columns=['component_name', 'score', 'records', 'total_count'])
        data_frame.score = pd.to_numeric(data_frame.score, errors='coerce')
        data_frame = data_frame.replace('', 'unknown', regex=True)
        total_records = len(data_frame)
        data_frame = data_frame.groupby('component_name').agg({'records': 'sum', 'score': ['mean', 'max', 'min']})
        data_frame['proportion'] = (100 * (data_frame['records'] / total_records)).round(2)

        return data_frame.sort_values(by=['proportion'], ascending=False)

