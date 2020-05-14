from validator import Required, Not, Truthy, Blank, Range, Equals, In, validate, Pattern, Length
import service.constant as constant
import re

alpha_numeric_regex = re.compile(
    r"^(?:[a-zA-Z0-9]+-){2,2}[a-zA-Z0-9]+$",
    re.IGNORECASE
)


def get_rules(valid_users_list, valid_teams_list, valid_component_list, valid_sub_component_list):
    # Audit log attributes needs to meet the following rules.
    rules = {
        constant.USER_ATTRIBUTE: [Required, In(valid_teams_list)],
        constant.TEAM_ATTRIBUTE: [Required, In(valid_users_list)],
        constant.COMPONENT_ATTRIBUTE:[Required, In(valid_sub_component_list)],
        constant.SUB_COMPONENT_ATTRIBUTE:[Required, Pattern(alpha_numeric_regex), Not(In(valid_component_list))]
    }

    return rules