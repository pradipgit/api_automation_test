from unittest import TestCase
from service.validators.AuditLogValidator import  AuditLogValidator
from service.validators.rules.ValidationRules import get_rules

class TestAuditLogValidator(TestCase):

    def test_calculate_score_user_attribute_scenarios(self):
        validator = AuditLogValidator()
        weights = {'user-attr': 3}
        required_attr_error = "must be present"
        single_error = ['must match regex pattern <_sre.SRE_Pattern object at 0x7fe107ada418>']
        property_weight = 0.25

        multiple_error = ['must match regex pattern <_sre.SRE_Pattern object at 0x1b80060>',
                          "must be one of [u'testuser@in.ibm.com', u'cloud.testuser@gmail.com']"]
        key = 'user-attr'

        self.assertEqual(validator.calculate_score(key, single_error, property_weight, weights),
                         (0.08333333333333333, 3))
        self.assertEqual(validator.calculate_score(key, multiple_error, property_weight, weights),
                         (0.16666666666666666, 3))
        self.assertEqual(validator.calculate_score(key, required_attr_error, property_weight, weights),
                         (0, 2))

    def test_calculate_score_component_attribute_scenarios(self):
        validator = AuditLogValidator()
        weights = {'component-attr': 3}
        required_attr_error = "must be present"
        single_error = ['must match regex pattern <_sre.SRE_Pattern object at 0x7fe107ada418>']
        property_weight = 0.25

        key = 'component-attr'

        self.assertEqual(validator.calculate_score(key, single_error, property_weight, weights),
                         (0.08333333333333333, 3))
        self.assertEqual(validator.calculate_score(key, required_attr_error, property_weight, weights),
                         (0, 2))

    def test_calculate_score_sub_component_attribute_scenarios(self):
        validator = AuditLogValidator()
        weights = {'sub-component-attr': 3}
        required_attr_error = "must be present"
        single_error = ['must match regex pattern <_sre.SRE_Pattern object at 0x7fe107ada418>']
        property_weight = 0.25

        key = 'sub-component-attr'

        self.assertEqual(validator.calculate_score(key, single_error, property_weight, weights),
                         (0.08333333333333333, 3))
        self.assertEqual(validator.calculate_score(key, required_attr_error, property_weight, weights),
                         (0, 2))

    def test_calculate_score_team_attribute_scenarios(self):
        validator = AuditLogValidator()
        weights = {'team-attr': 3}
        required_attr_error = "must be present"
        single_error = ['must match regex pattern <_sre.SRE_Pattern object at 0x7fe107ada418>']
        property_weight = 0.25

        multiple_error = ['must match regex pattern <_sre.SRE_Pattern object at 0x1b80060>',
                          "must be one of [u'testuser@in.ibm.com', u'cloud.testuser@gmail.com']"]
        key = 'team-attr'

        self.assertEqual(validator.calculate_score(key, single_error, property_weight, weights),
                         (0.08333333333333333, 3))
        self.assertEqual(validator.calculate_score(key, multiple_error, property_weight, weights),
                         (0.16666666666666666, 3))
        self.assertEqual(validator.calculate_score(key, required_attr_error, property_weight, weights),
                         (0, 2))

    def test_validate_Audit_log_positive_scenario(self):
        validator = AuditLogValidator()

        audit_log = {'user-attr': 'testuser@in.ibm.com', 'team-attr': 'CORETSA', 'component-attr': 'component-', 'sub-component-attr': 'sub-component-'}

        rules = get_rules(['testuser@in.ibm.com', 'cloud.testuser@gmail.com'], ["CORETSA", "TSATEST", "FTest"])

        error = validator.validate(audit_log, rules)

        self.assertEqual(error[0], True, msg='validation status.')

    def test_validate_user_attribute_negative_scenario(self):
        validator = AuditLogValidator()

        audit_log = {'team-attr':'CORETSA', 'component-attr':'component-', 'sub-component-attr':'sub-component-'}

        rules = get_rules(['testuser@in.ibm.com', 'cloud.testuser@gmail.com'], ["CORETSA", "TSATEST", "FTest"])

        error = validator.validate(audit_log, rules)

        self.assertEqual(error[0], False, msg='validation status.')
        self.assertEqual(error[1]['user-attr'], 'must be present', msg='error description.')

    def test_validate_team_attribute_negative_scenario(self):
        validator = AuditLogValidator()

        audit_log = {'user-attr': 'testuser@in.ibm.com', 'component-attr': 'component-', 'sub-component-attr': 'sub-component-'}

        rules = get_rules(['testuser@in.ibm.com', 'cloud.testuser@gmail.com'], ["CORETSA", "TSATEST", "FTest"])

        error = validator.validate(audit_log, rules)

        self.assertEqual(error[0], False, msg='validation status.')
        self.assertEqual(error[1]['team-attr'], 'must be present', msg='error description.')

    def test_validate_component_attribute_negative_scenario(self):
        validator = AuditLogValidator()

        audit_log = {'user-attr': 'testuser@in.ibm.com', 'team-attr': 'CORETSA', 'sub-component-attr': 'sub-component-'}

        rules = get_rules(['testuser@in.ibm.com', 'cloud.testuser@gmail.com'], ["CORETSA", "TSATEST", "FTest"])

        error = validator.validate(audit_log, rules)

        self.assertEqual(error[0], False, msg='validation status.')
        self.assertEqual(error[1]['component-attr'], 'must be present', msg='error description.')

    def test_validate_component_attribute_partially_valid_scenario(self):
        validator = AuditLogValidator()

        audit_log = {'user-attr': 'testuser@in.ibm.com', 'team-attr': 'CORETSA', 'component-attr': 'comp', 'sub-component-attr': 'sub-component-'}

        rules = get_rules(['testuser@in.ibm.com', 'cloud.testuser@gmail.com'], ["CORETSA", "TSATEST", "FTest"])

        error = validator.validate(audit_log, rules)

        self.assertEqual(error[0], False, msg='validation status.')
        self.assertTrue(len(error[1]) >= 1)

    def test_validate_sub_component_attribute_negative_scenario(self):
        validator = AuditLogValidator()

        audit_log = {'user-attr': 'testuser@in.ibm.com', 'team-attr': 'CORETSA', 'component-attr': 'component-'}

        rules = get_rules(['testuser@in.ibm.com', 'cloud.testuser@gmail.com'], ["CORETSA", "TSATEST", "FTest"])

        error = validator.validate(audit_log, rules)

        self.assertEqual(error[0], False, msg='validation status.')
        self.assertEqual(error[1]['sub-component-attr'], 'must be present', msg='error description.')

    def test_validate_sub_component_attribute_partially_valid_scenario(self):
        validator = AuditLogValidator()

        audit_log = {'user-attr': 'testuser@in.ibm.com', 'team-attr': 'CORETSA', 'component-attr': 'comp', 'sub-component-attr': 'sub-'}

        rules = get_rules(['testuser@in.ibm.com', 'cloud.testuser@gmail.com'], ["CORETSA", "TSATEST", "FTest"])

        error = validator.validate(audit_log, rules)

        self.assertEqual(error[0], False, msg='validation status.')
        self.assertTrue(len(error[1]) >= 1)

