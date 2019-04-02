from rule_parser.Tokenizer import Tokenizer
from rule_parser.TokenStringDictionary import TokenStringDictionary
from fact_value.FactValueType import FactValueType


class FactValue:

    value_type = None # type of this variable is FactValueType
    value = None      # type of this variable is vary. it could be string, int, float, list, dict, bool,
    default_value = None

    def __init__(self, value=None, value_type=None):
        if (value is not None) and (value_type is not None):
            self.value_type = value_type
            self.value = value
        elif value is not None:
            if isinstance(value, FactValue):
                self.value = value.get_value()
                self.value_type = value.get_value_type()
            elif isinstance(value, bool):
                self.value = value
                self.value_type = FactValueType.BOOLEAN
            else:
                self.value = value
                self.value_type = TokenStringDictionary.find_fact_value_type(Tokenizer.get_tokens(value).tokens_string)

    def set_value(self, value):
        self.value = value

    def set_value_type(self, value_type):
        self.value_type = value_type

    def get_value(self):
        return self.value

    def get_value_type(self):
        return self.value_type

    def set_default_value(self, default_value):
        self.default_value = default_value

    def get_default_value(self):
        return self.default_value
