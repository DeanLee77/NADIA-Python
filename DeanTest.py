from fact_value.FactValueType import FactValueType
from node.MetaType import MetaType
from constant.TokenizerMatcherConstant import TokenizerMatcherConstant
from rule_parser.TokenStringDictionary import TokenStringDictionary
import re
from rule_parser.Tokenizer import Tokenizer
from rule_parser.Tokens import Tokens
from datetime import *
from fact_value.FactValue import FactValue
from node.ValueConclusionLine import ValueConclusionLine



class DeanTest:

    if __name__ == "__main__":
        # value_type = FactValueType.BOOLEAN
        # print(isinstance(value_type, FactValueType))
        # first_fact_value = FactValue.parse(True, value_type)
        # second_fact_value = FactValue.parse('fact value', FactValueType.STRING)
        # print(first_fact_value.get_value_type())
        # print(second_fact_value.get_value())
        # print(TokenizerMatcherConstant.LOWER_MATCHER.value)
        p = re.compile(TokenizerMatcherConstant.LOWER_MATCHER.value)
        sampleStr = 'this- is REGULAR Expression String'
        m = p.search(sampleStr)
        print(len(m.groups()))
        print(m.group(1))
        # print(m.group(0))
        # print(m.group(0).strip())
        # print(sampleStr[:5])

        print(MetaType.get_all_meta_type())
        for x in MetaType.get_all_meta_type():
            print(x.value)

        print(list(TokenStringDictionary.get_all_key_and_values().keys())[0])
        temp_list = [1, 2, 3, 4, 5]
        print(len(list(filter(lambda value: value > 3, temp_list))))
        print(list(temp_list))

        pattern = re.compile(r'[-+/*()?:;,.""](\s*)')
        string = 'number of drinks the person consumes a week IS CALC ( number of drinks the person consumes an hour * hours of drinks a day * (5-1))'
        token = Tokenizer.get_tokens(string)
        print(token.tokens_string_list[2])

        date_pattern = re.compile(r'([0-2]?[0-9]|3[0-1])/(0?[0-9]|1[0-2])/([0-9][0-9])?[0-9][0-9]|([0-9][0-9])?[0-9][0-9]/(0?[0-9]|1[0-2])/([0-2]?[0-9]|3[0-1])')
        newString = '12/12/2018 - 11/11/2001'
        new_string = 'arerewqrew qw qwerwqe '
        matcher = date_pattern.finditer(newString)
        if matcher:
            for x in matcher:
                print(x.group())
                print(datetime.strptime(x.group(), '%d/%m/%Y'))

        while date_pattern.search(newString):
            print(date_pattern.search(newString).group())
            newString = newString.replace(date_pattern.search(newString).group(), '')

        li = [1, 2.1212, 4, 6, 9, 11, 12, 14]
        fv = FactValue(li, FactValueType.LIST)
        print(fv.get_value())
        fv = FactValue(True, FactValueType.BOOLEAN)
        print(fv.get_value())
        tokens = Tokenizer.get_tokens(new_string)
        valueNode = ValueConclusionLine(new_string, tokens)
        factValue = valueNode.get_fact_value()
        fv2 = FactValue(factValue)
        print("fact value: "+valueNode.get_variable_name())
        int_var = 1
        string_var = '123'
        print(isinstance(True, bool))
        print(TokenStringDictionary.find_fact_value_type(Tokenizer.get_tokens(str(True)).tokens_string))
        print('here')
        print(list(filter(lambda item: item > 10 or item < 5, li)))

        two_d_array = [[0 for i in range(5)] for x in range(6)]
        two_d_array[0][1] = 2
        two_d_array[0][4] = 5
        two_d_array[1][2] = 3
        print("two_d_array len: "+str(len(two_d_array)))
        li.pop(2)
        print("after pop")
        print(li)
