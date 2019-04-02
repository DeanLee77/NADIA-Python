from node.Node import Node
from node.MetaType import MetaType
import re
from datetime import datetime
from fact_value.FactValue import FactValue
from fact_value.FactValueType import FactValueType
from node.LineType import LineType


class MetadataLine(Node):

    # Meta type pattern list
    # 1. ULU[NoDaMLDe]
    # 2. U[NoDaMLDe]
    # 3. U

    meta_type = None
    name = None

    def initialisation(self, parent_text, tokens):
        self.name = parent_text
        self.set_meta_type(parent_text)

        if self.meta_type == MetaType.FIXED.value:
            pattern = re.compile(r"^(FIXED)(.*)(\s[AS|IS]\s*.*)")
            match = pattern.match(parent_text)

            if match:
                self.variable_name = match.group(2).strip()
                self.set_value(match.group(3).strip(), tokens)
        if self.meta_type == MetaType.INPUT.value:
            pattern = re.compile(r"^(INPUT)(.*)(AS)(.*)[(IS)(.*)]?")
            match = pattern.match(parent_text)

            if match:
                self.variable_name = match.group(2).strip()
                self.set_value(match.group(4).strip(), tokens)

    def set_value(self, value_in_string, tokens):
        token_string_list_size = len(tokens.tokens_string_list)
        last_token_string = tokens.tokens_string_list[token_string_list_size - 1]
        temp_array = re.split(' ', value_in_string)
        temp_str = temp_array[0]

        if self.meta_type == MetaType.FIXED.value:
            if temp_str == "IS":
                if self.is_date(last_token_string):
                    self.value = FactValue.parse(datetime.strptime(temp_array[1], '%d/%m/%Y'), FactValueType.DATE)
                elif self.is_double(last_token_string):
                    self.value = FactValue.parse(float(temp_array[1]), FactValueType.DOUBLE)
                elif self.is_integer(last_token_string):
                    self.value = FactValue.parse(int(temp_array[1]), FactValueType.INTEGER)
                elif self.is_boolean(last_token_string):
                    if temp_array[1].lower() == 'false':
                        self.value = FactValue.parse(False, FactValueType.BOOLEAN)
                    else:
                        self.value = FactValue.parse(True, FactValueType.BOOLEAN)

                elif self.is_hash(last_token_string):
                    self.value = FactValue.parse(temp_array[1], FactValueType.HASH)
                elif self.is_url(last_token_string):
                    self.value = FactValue.parse(temp_array[1], FactValueType.URL)
                elif self.is_guid(last_token_string):
                    self.value = FactValue.parse(temp_array[1], FactValueType.GUID)
            elif temp_str == 'AS':
                if temp_array[1] == 'LIST':
                    self.value = FactValue.parse(list(), FactValueType.LIST)
                else:
                    self.value = FactValue.parse('WARNING', FactValueType.WARNING)

        elif self.meta_type == MetaType.INPUT.value:
            if temp_array:
                # within this case 'DefaultValue' will be set due to the statement format is as follows;
                # 'A AS 'TEXT' IS B'
                # and 'A' is variable, 'TEXT' is a type of variable, and 'B' is a default value.
                # if the type is 'LIST' then variable is a list then the factValue has a default value.

                temp_str_2 = temp_array[2]
                if FactValueType.LIST.value == temp_str:
                    value_list = list()
                    if self.is_date(last_token_string): # temp_str_2 is date value
                        temp_value = FactValue.parse(datetime.strptime(temp_str_2, '%d/%m/%Y'), FactValueType.DATE)
                    elif self.is_double(last_token_string): # temp_str_2 is double value
                        temp_value = FactValue.parse(float(temp_str_2), FactValueType.DOUBLE)
                    elif self.is_integer(last_token_string): # temp_str_2 is integer value
                        temp_value = FactValue.parse(int(temp_str_2), FactValueType.INTEGER)
                    elif self.is_hash(last_token_string): # temp_str_2 is hash value
                        temp_value = FactValue.parse(temp_str_2, FactValueType.HASH)
                    elif self.is_url(last_token_string): # temp_str_2 is URL value
                        temp_value = FactValue.parse(temp_str_2, FactValueType.URL)
                    elif self.is_guid(last_token_string): # temp_str_2 is GUID value
                        temp_value = FactValue.parse(temp_str_2, FactValueType.GUID)
                    elif self.is_boolean(last_token_string): # temp_str_2 is boolean value
                        if temp_str_2.lower() == 'false':
                            temp_value = FactValue.parse(False, FactValueType.BOOLEAN)
                        else:
                            temp_value = FactValue.parse(True, FactValueType.BOOLEAN)
                    else: # temp_str_2 is string value
                        temp_value = FactValue.parse(temp_str_2, FactValueType.STRING)
                    value_list.append(temp_value)
                    self.value = FactValue.parse(value_list, FactValueType.LIST)
                    self.value.set_default_value(temp_value)
                elif FactValueType.TEXT.value == temp_str:
                    self.value = FactValue.parse(temp_str_2, FactValueType.STRING)
                elif FactValueType.DATE.value == temp_str:
                    self.value = FactValue.parse(datetime.strptime(temp_str_2, '%d/%m/%Y'), FactValueType.DATE)
                elif FactValueType.NUMBER.value == temp_str:
                    self.value = FactValue.parse(int(temp_str_2), FactValueType.INTEGER)
                elif FactValueType.DECIMAL.value == temp_str:
                    self.value = FactValue.parse(float(temp_str_2), FactValueType.DECIMAL)
                elif FactValueType.BOOLEAN.value == temp_str:
                    if temp_str_2.lower() == 'true':
                        value = True
                    else:
                        value = False
                    self.value = FactValue.parse(value, FactValueType.BOOLEAN)
                elif FactValueType.URL.value == temp_str:
                    self.value = FactValue.parse(temp_str_2, FactValueType.URL)
                elif FactValueType.HASH.value == temp_str:
                    self.value = FactValue.parse(temp_str_2, FactValueType.HASH)
                elif FactValueType.GUID.value == temp_str:
                    self.value = FactValue.parse(temp_str_2, FactValueType.GUID)
            else:
                # case of the statement does not have value, only contains a type of the variable
                # so that the value will not have any default values
                if FactValueType.LIST.value == temp_str:
                    self.value = FactValue.parse(list(), FactValueType.LIST)
                elif FactValueType.TEXT.value == temp_str or FactValueType.STRING.value == temp_str or FactValueType.URL.value == temp_str\
                        or FactValueType.HASH.value == temp_str or FactValueType.GUID.value == temp_str:
                    self.value = FactValue.parse("", FactValueType.STRING)
                elif FactValueType.DATE.value == temp_str or FactValueType.NUMBER.value == temp_str or FactValueType.INTEGER.value == temp_str\
                        or FactValueType.DECIMAL.value == temp_str or FactValueType.BOOLEAN.value == temp_str:
                    self.value = FactValue.parse(None, None)

    def set_meta_type(self, parent_text):
        for x in MetaType.get_all_meta_type():
            if x.value in parent_text:
                self.meta_type = x

    def get_meta_type(self):
        return self.meta_type

    def get_name(self):
        return self.name

    def get_line_type(self):
        return LineType.META

    def self_evaluate(self, working_memory):
        return FactValue(None, None)
