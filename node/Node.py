from abc import ABCMeta
import abc
from fact_value.FactValue import FactValue
from fact_value.FactValueType import FactValueType
from rule_parser.TokenStringDictionary import TokenStringDictionary
import re


class Node(metaclass=ABCMeta):

    static_node_id = 0
    node_id = None
    node_name = None
    node_line = None
    variable_name = None
    value = None
    tokens = None

    @classmethod
    def get_static_node_id(cls):

        return cls.static_node_id

    @classmethod
    def increment_static_node_id(cls):
        cls.static_node_id += 1

    def __init__(self, parent_text, tokens):
        self.node_id = self.get_static_node_id()
        self.increment_static_node_id()
        self.tokens = tokens

        self.initialisation(parent_text, tokens)

    @abc.abstractmethod
    def initialisation(self, parent_text, tokens): pass

    @abc.abstractmethod
    def get_line_type(self): pass

    @abc.abstractmethod
    def self_evaluate(self, working_memory): pass

    def set_node_line(self, node_line):
        self.node_line = node_line

    def get_node_line(self):
        return self.node_line

    def get_node_id(self):
        return self.node_id

    def get_node_name(self):
        return self.node_name

    def get_tokens(self):
        return self.tokens

    def get_variable_name(self):
        return self.variable_name

    def set_node_variable(self, new_variable_name):
        self.variable_name = new_variable_name

    def get_fact_value(self):
        return self.value

    def set_value(self, last_token_string, last_token=None):

        if last_token is None:
            self.value = last_token_string
        else:
            if not re.match(r"C|L|M|U", last_token_string, re.IGNORECASE):
                self.value = FactValue(last_token, TokenStringDictionary.find_fact_value_type(last_token_string))
            else:
                fact_value_type = TokenStringDictionary.find_fact_value_type(last_token)
                if fact_value_type is FactValueType.BOOLEAN:
                    if re.match(r"false", last_token, re.IGNORECASE):
                        self.value = FactValue(False, fact_value_type)
                    elif re.match(r"true", last_token, re.IGNORECASE):
                        self.value = FactValue(True, fact_value_type)
                else:
                    if re.match(r"(^[\'\"])(.*)([\'\"]$)", last_token, re.IGNORECASE):
                        self.value = FactValue(last_token, FactValueType.DEFI_STRING)
                    else:
                        self.value = FactValue(last_token, FactValueType.STRING)

    def is_boolean(self, string):

        if re.match(r"[FfAaLlSsEe]", string, re.IGNORECASE):
            return False
        else:
            return True

    def is_integer(self, string):
        return "No" == string

    def is_double(self, string):
        return "De" == string

    def is_date(self, string):
        return "Da" == string

    def is_url(self, string):
        return "Url" == string

    def is_hash(self, string):
        return "Ha" == string

    def is_guid(self, string):
        return "Id" == string

