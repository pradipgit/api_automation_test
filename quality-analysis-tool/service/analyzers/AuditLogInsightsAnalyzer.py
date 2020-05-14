import pandas as pd
import simplejson as Json
import service.constant as constant
from service.validators.AuditLogValidator import AuditLogValidator
from decimal import *


class AuditLogInsightsAnalyzer():

    def __init__(self, rules, weights, output_file_name):
        self.rules = rules
        self.weights = weights
        self.report_filename = output_file_name

    def generate(self, audit_logs):

        scored_logs = self.validate_and_score(audit_logs)

        insights = self.get_insights_for_report(scored_logs)

        self.write_to_excel(insights)

    def validate_and_score(self, audit_logs):

        audit_message_validator = AuditLogValidator()

        component = []
        sub_component = []

        validation_errors = []
        score = []

        users = []
        teams = []
        comps = []
        sub_comps = []

        for log in audit_logs:
            validation_result = audit_message_validator.validate(log, self.rules)
            score_result, user, team, comp, sub_comp = audit_message_validator.score(validation_result, 1/Decimal(len(self.rules)), self.weights)

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

            json_errors = Json.dumps(validation_result, default=lambda x: x.__dict__)
            validation_errors.append(json_errors)

            continue

        logs = {
            "score": score,
            "component_name": component,
            "sub-component_name": sub_component,
            "users": users,
            "teams": teams,
            "comps": comps,
            "subcomps": sub_comps
        }

        return logs

    def write_to_excel(self, insights):

        columns = ['component_name',
                   '% Valid UserId','% Invalid UserId',
                   '% Valid TeamId','% Invalid TeamId',
                   '% Component-Name Valid','% Component-Name Invalid','% Component-Name Missing',
                   '% SubComponent-Name Valid','% SubComponent-Name Invalid','% SubComponent-Name Missing'
                   ]

        records = pd.DataFrame(insights, columns=columns).style.applymap(self._color_red_or_green)
        sheet_name = 'Insights'

        pd.set_option('display.max_colwidth', 0)
        writer = pd.ExcelWriter(self.report_filename, engine='xlsxwriter')

        records.to_excel(writer, sheet_name=sheet_name)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        cell_format = workbook.add_format({'bold': False})
        cell_format.set_text_wrap()
        cell_format.set_rotation(30)
        cell_format.set_align('center_across')
        cell_format.set_align('vcenter')

        worksheet.set_row(0, 70, cell_format)

        # column styles
        worksheet.set_column('B:B', 40, cell_format, {'level': 1, 'fg_color': '#D7E4BC'})
        worksheet.set_column('C:C', 12)
        worksheet.set_column('D:D', 14)
        worksheet.set_column('E:F', 14)
        worksheet.set_column('G:G', 20)
        worksheet.set_column('H:H', 18)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:N', 18)

        # Write the column headers with the defined format.
        for col_num, value in enumerate(records.columns.values):
            worksheet.write(0, col_num + 1, value)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def get_insights_for_report(self, logs):
        pd.set_option('display.max_colwidth', -1)

        data_frame = pd.DataFrame(logs, columns=['component_name', 'users', 'teams', 'comps', 'subcomps'])
        data_frame = data_frame.replace('', 'unknown', regex=True)

        unique_components = data_frame.component_name.unique()

        insights = []

        for component in unique_components:
            components = data_frame[data_frame["component_name"] == component]
            component_count = len(components)

            percentage_users_valid = self.get_attribute_insights(components, component_count, 'users', 1)
            percentage_users_invalid = self.get_attribute_insights(components, component_count, 'users', 3)

            percentage_teams_valid = self.get_attribute_insights(components, component_count, 'teams', 1)
            percentage_teams_invalid = self.get_attribute_insights(components, component_count, 'teams', 3)

            percentage_comps_missing = self.get_attribute_insights(components, component_count, 'comps', 2)
            percentage_comps_valid = self.get_attribute_insights(components, component_count, 'comps', 1)
            percentage_comps_invalid = self.get_attribute_insights(components, component_count, 'comps', 3)

            percentage_sub_comps_missing= self.get_attribute_insights(components, component_count, 'subcomps', 2)
            percentage_sub_comps_valid = self.get_attribute_insights(components, component_count, 'subcomps', 1)
            percentage_sub_comps_invalid = self.get_attribute_insights(components, component_count, 'subcomps', 3)

            insight = {'component_name': component,
                       '% Valid UserId': percentage_users_valid,
                       '% Invalid UserId': percentage_users_invalid,
                       '% Valid TeamId': percentage_teams_valid,
                       '% Invalid TeamId': percentage_teams_invalid,
                       '% Component-Name Valid': percentage_comps_valid,
                       '% Component-Name Invalid': percentage_comps_invalid,
                       '% Component-Name Missing': percentage_comps_missing,
                       '% SubComponent-Name Valid': percentage_sub_comps_valid,
                       '% SubComponent-Name Invalid': percentage_sub_comps_invalid,
                       '% SubComponent-Name Missing': percentage_sub_comps_missing,
            }

            insights.append(insight)

        return insights

    def get_attribute_insights(self, records,  total_count, property_key, property_value):
        attribute = records[records[property_key] == property_value]
        valid_percentage = (Decimal(len(attribute)) / Decimal(total_count)) * 100

        return round(valid_percentage, 3)

    def _color_red_or_green(self, val):

        color = 'red' if val < 100 else 'green'
        return 'color: %s' % color

