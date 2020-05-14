from validator import Required, Not, Truthy, Blank, Range, Equals, In, validate, Pattern, Length
import re
import service.constant as constant

name_regex = re.compile(
    "^[a-z0-9_-]{3,15}$",
    re.IGNORECASE
)

userid_regex = re.compile(
      # dot-atom
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+"
    r"(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"
    # quoted-string
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|'
    r"""\\[\001-\011\013\014\016-\177])*"$)""",
    re.IGNORECASE
)

teamid_regex = re.compile(
    r"^(?:[a-zA-Z0-9]+-){2,2}[a-zA-Z0-9]+$",
    re.IGNORECASE
)

component_regex = re.compile(
    r"\bcomponent-"
)

subcomponent_regex = re.compile(
    r"\bsub-component-"
)

weights = {
    "user-attr":3,
    "team-attr":3,
    "component-attr":3,
    "sub-component-attr":3
}


def get_rules(valid_users_list, valid_teams_list):
    # Audit log attributes needs to meet the following rules.
    rules = {
        constant.USER_ATTRIBUTE: [Required, In(valid_users_list), Length(5, maximum=100)],
        constant.TEAM_ATTRIBUTE: [Required, In(valid_teams_list), Length(5, maximum=100)],
        constant.COMPONENT_ATTRIBUTE:[Required, Length(5, maximum=100), Pattern(name_regex)],
        constant.SUB_COMPONENT_ATTRIBUTE:[Required, Length(5, maximum=100), Pattern(name_regex)]
    }

    return rules


def get_weights():
    return weights
