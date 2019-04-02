from node.Node import Node
import re
from node.LineType import LineType
from fact_value.FactValue import FactValue
from fact_value.FactValueType import FactValueType
from datetime import datetime
from rule_parser.Tokenizer import Tokenizer
from rule_parser.Tokens import Tokens


class ExprConclusionLine(Node):

    equation: FactValue = None

    dateFormatter = '%d/%m/%Y'

    def __init__(self, parent_text: str, tokens: Tokens):
        super().__init__(parent_text, tokens)

    def initialisation(self, parent_text: str, tokens: Tokens):
        self.node_name = parent_text
        temp_array = re.split("IS CALC", parent_text)
        self.variable_name = temp_array[0].strip()
        index_of_c_in_tokens_string_list = tokens.tokens_string_list.index('C')
        self.set_value(tokens.tokens_string_list[index_of_c_in_tokens_string_list].strip(),
                       tokens.tokens_list[index_of_c_in_tokens_string_list].strip())
        self.equation = self.value

    def get_equation(self) -> FactValue:
        return self.equation

    def set_equation(self, equation):
        self.equation = equation

    def get_line_type(self) -> LineType:
        return LineType.EXPR_CONCLUSION

    def self_evaluate(self, working_memory: dict) -> FactValue:
        # calculation can only handle int, double(long) and difference in years between two dates at the moment.
        # if difference in days or months is required then new 'keyword'
        # must be introduced such as 'Diff Years', 'Diff Days', or 'Diff Months'

        equation_in_string = self.equation.get_value()
        pattern = re.compile(r'[-+/*()?:;,.""](\s*)')
        date_pattern = re.compile(r'([0-2]?[0-9]|3[0-1])/(0?[0-9]|1[0-2])/([0-9][0-9])?[0-9][0-9]|\
                                  ([0-9][0-9])?[0-9][0-9]/(0?[0-9]|1[0-2])/([0-2]?[0-9]|3[0-1])')

        # logic for this is as follows;
        #  1. replace all variables with actual values from 'workingMemory'
        #  2. find out if equation is about date (difference in years) calculation or not
        #  3. if it is about date then convert all relevant date-in-string to datetime then calculate
        #  3-1. if it is about int or double(long) then use plain Javascript

        script = equation_in_string
        temp_script = script

        if pattern.match(equation_in_string):
            temp_array = re.split(pattern, equation_in_string)
            temp_array_length = len(temp_array)
            temp_item = ''

            for i in range(temp_array_length):
                temp_item = temp_array[i].strip()
                if (len(temp_item) != 0) and (temp_item in dict(working_memory)) \
                        and (dict(working_memory)[temp_item] is not None):
                    temp_fact_value: object = working_memory[temp_item]
                    if temp_fact_value.get_value_type() == FactValueType.DATE:
                        # below line is temporary solution.
                        # Within next iteration it needs to be that
                        # this node should take dateFormatter for its constructor to determine which date format it needs
                        temp_str =  datetime.strptime(temp_fact_value.get_value(), self.dateFormatter)
                        temp_script = temp_script.replace(temp_item, temp_str)
                    else:
                        temp_script = temp_script.replace(temp_item, working_memory[temp_item].get_value())

        date_matcher = date_pattern.finditer(temp_script)
        if date_matcher:
            date_array = []
            for x in date_matcher:
                date_time = datetime.strptime(x.group(), '%d/%m/%Y')
                date_array.append(date_time)

            if len(date_array) > 0:
                result = (date_array[0] - date_array[1]).days/365.2
            else:
                result = eval(temp_script)

            check_tokens = Tokenizer.get_tokens(result).tokens_string
            if check_tokens == 'NO':
                return_value = FactValue.parse(int(result))
            elif check_tokens == 'DE':
                return_value = FactValue.parse(float(result))
                # there is no function for outcome to be a date at the moment
                # E.g.The determination IS CALC(enrollment date + 5 days)
            else:
                return_value = FactValue.parse(result)

        return return_value


