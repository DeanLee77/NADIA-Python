from node.Node import Node
from rule_parser.Tokens import Tokens
import re
from node.LineType import LineType
from fact_value.FactValueType import FactValueType
from fact_value.FactValue import FactValue
from datetime import datetime


class ComparisonLine(Node):

    operator_string = None
    lhs = None
    rhs = None

    def __init__(self, child_text: str, tokens: Tokens):
        super().__init__(child_text, tokens)

    def initialisation(self, child_text, tokens):
        self.node_name = child_text
        # In 'eval' engine '=' operator means assigning a value, hence if the operator is '=' then it needs to be replaced with '=='.
        operator_index = tokens.tokens_string_list.index("O")
        if tokens.tokens_list[operator_index] == "=":
            self.operator_string = "=="
        else:
            self.operator_string = tokens.tokens_list[operator_index]

        self.variable_name = re.split(tokens.tokens_list[operator_index], child_text)[0].strip()
        self.lhs = self.variable_name
        tokens_string_list_size = len(tokens.tokens_string_list)
        last_token = tokens.tokens_list[tokens_string_list_size - 1]
        last_token_string = tokens.tokens_string_list[tokens_string_list_size - 1]
        self.set_value(last_token_string, last_token)
        self.rhs = self.value

    def get_rule_name(self):
        return self.node_name

    def get_lhs(self):
        return self.lhs

    def get_rhs(self):
        return self.rhs

    def get_line_type(self):
        return LineType.COMPARISON

    def self_evaluate(self, working_memory):
        # Negation type can only be used for this line type

        if self.variable_name in working_memory:
            working_memory_lhs_value = working_memory[self.variable_name]

        rhs_value_in_string = self.rhs.get_value()
        if rhs_value_in_string in working_memory:
            working_memory_rhs_value = working_memory[rhs_value_in_string]
        else:
            working_memory_rhs_value = self.get_rhs()

        # There will NOT be the case of that workingMemoryRhsValue is null because the node must be in following format;
        # - A = 12231 (int or double)
        # - A = Adam sandler (String)
        # - A = 11/11/1977 (Date)
        # - A = 123123dfae1421412aer(Hash)
        # - A = 1241414-12421312-142421312(UUID)
        # - A = true(Boolean)
        # - A = www.aiBrain.com(URL)
        # - A = B(another variable)

        # if it is about date comparison then string of 'script' needs rewriting
        if ((working_memory_lhs_value is not None) and (working_memory_lhs_value.get_fact_value_type() == FactValueType.DATE)) or\
            ((working_memory_rhs_value is not None) and (working_memory_rhs_value.get_value_type() == FactValueType.DATE)):
            if self.operator_string == ">":
                return_value = datetime.strptime(working_memory_lhs_value, "%d/%m/%Y") > datetime.strptime(working_memory_rhs_value, "%d/%m/%Y")
            elif self.operator_string == ">=":
                return_value = datetime.strptime(working_memory_lhs_value, "%d/%m/%Y") >= datetime.strptime(working_memory_rhs_value, "%d/%m/%Y")
            elif self.operator_string == "<":
                return_value = datetime.strptime(working_memory_lhs_value, "%d/%m/%Y") < datetime.strptime(working_memory_rhs_value, "%d/%m/%Y")
            elif self.operator_string == "<=":
                return_value = datetime.strptime(working_memory_lhs_value, "%d/%m/%Y") <= datetime.strptime(working_memory_rhs_value, "%d/%m/%Y")
            elif self.operator_string == "==":
                return_value = datetime.strptime(working_memory_lhs_value, "%d/%m/%Y") == datetime.strptime(working_memory_rhs_value, "%d/%m/%Y")

        elif (working_memory_lhs_value is not None) and\
                ((working_memory_lhs_value.get_fact_value_type == FactValueType.DECIMAL) or (working_memory_lhs_value.get_fact_value_type() == FactValueType.DOUBLE)\
                        or (working_memory_lhs_value.get_fact_value_type() == FactValueType.INTEGER) or (working_memory_lhs_value.get_fact_value_type() == FactValueType.NUMBER)):

            script = working_memory_lhs_value.get_value() + self.operator_string + working_memory_rhs_value.get_value()
        else:
            if (working_memory_rhs_value is not None) and (working_memory_lhs_value is not None):
                script = "'"+str(working_memory_lhs_value.get_value())+"'"+self.operator_string+"'"+str(working_memory_rhs_value())+"'"

        if (working_memory_rhs_value is not None) and (working_memory_lhs_value is not None):
            return FactValue(eval(script))
