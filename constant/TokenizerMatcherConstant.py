from enum import Enum


class TokenizerMatcherConstant(Enum):

    SPACE_MATCHER = r"^\s+"
    QUOTED_MATCHER = r"^([\"\“])(.*)([\"\”])(\.)*"
    ITERATE_MATCHER = r"^(ITERATE:(\s*)LIST OF)(.)"
    MIXED_MATCHER = r"^([A-Z][a-z-'’,\.\s]+)+"
    UPPER_MATCHER = r"^([:'’,\.A-Z_\s]+(?![a-z]))"
    URL_MATCHER = r"^(ht|f)tps?\\:([0-9a-zA-Z]|[0-9a-fA-F]|[\t\n\x08\f\r])*$"
    OPERATOR_MATCHER = r"^([<>=]+)"
    CALCULATION_MATCHER = r"^(\()([\s|\d+(?!/.)|\w|\W]*)(\))"
    HASH_MATCHER = r"^([-]?)([0-9a-f]{10,}$)(?!\\-)*"
    NUMBER_MATCHER = r"^(\d+)(?!/|\.|\d)+"
    DECIMAL_NUMBER_MATCHER = r"^([\d]+\.\d+)(?!\d)"
    DATE_MATCHER = r"^([0-2]?[0-9]|3[0-1])/(0?[0-9]|1[0-2])/([0-9][0-9])?[0-9][0-9]|^([0-9][0-9])?[0-9][0-9]/(0?[0-9]|1[0-2])/([0-2]?[0-9]|3[0-1])"
    GUID_MATCHER = r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}"
    LOWER_MATCHER = r"^([a-z\-'’,\.\s]+(?!\d))"

    @staticmethod
    def get_all_matcher():
        return list(map(lambda x: x.value, TokenizerMatcherConstant))

    @staticmethod
    def get_all_enums():
        return list(map(lambda c: c, TokenizerMatcherConstant))
