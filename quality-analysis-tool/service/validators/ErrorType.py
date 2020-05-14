from enum import Enum

class ErrorType(Enum):
    VALID = 1
    MISSING = 2
    PARTIAL = 3

class ErrorDescription:
    def __init__(self, user, team, comp, subcomp):
        self.user = user
        self.team = team
        self.comp = comp
        self.subcomp = subcomp