from validator import validate
import service.constant as constant

class ErrorDescription:
    def __init__(self, user, team, comp, sub_comp):
        self.user = user
        self.team = team
        self.comp = comp
        self.sub_comp = sub_comp


class AuditLogValidator:

    def __init__(self):
        pass

    @staticmethod
    def validate(audit_log, rules):

        return validate(rules, audit_log)

    def score(self, audit_log, property_weight, weights):

        attribute_errors = len(audit_log.errors)
        score = 1 - (attribute_errors * property_weight)

        user = 1
        team = 1
        comp = 1
        sub_comp = 1

        for key, value in audit_log.errors.iteritems():

            if key == constant.USER_ATTRIBUTE:
                rule_score, error_type = self.calculate_score(constant.USER_ATTRIBUTE, value, property_weight, weights)
                score += rule_score
                user = error_type

            if key == constant.TEAM_ATTRIBUTE:
                rule_score, error_type = self.calculate_score(constant.TEAM_ATTRIBUTE, value, property_weight, weights)
                score += rule_score
                team = error_type

            if key == constant.COMPONENT_ATTRIBUTE:
                rule_score, error_type = self.calculate_score(constant.COMPONENT_ATTRIBUTE, value, property_weight, weights)
                score += rule_score
                comp = error_type

            if key == constant.SUB_COMPONENT_ATTRIBUTE:
                rule_score, error_type = self.calculate_score(constant.SUB_COMPONENT_ATTRIBUTE, value, property_weight, weights)
                score += rule_score
                sub_comp = error_type

            continue

        return score*10, user, team, comp, sub_comp

    @staticmethod
    def calculate_score(key, errors, property_weight, weights):

        rule_errors = len(errors)
        rule_weight = property_weight / weights[key]
        rule_score = rule_weight * rule_errors

        if errors == "must be present":
            return 0, 2

        elif rule_errors >= 1:
            return rule_score, 3

        else:
            return rule_score, 1


