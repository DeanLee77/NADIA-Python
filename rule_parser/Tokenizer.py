from constant.TokenizerMatcherConstant import TokenizerMatcherConstant
from rule_parser.Tokens import Tokens

import re


class Tokenizer:

    # the order of Pattern in the array of 'matchPatterns' is extremely important because some patterns won't work if other patterns are invoked earlier than them
    # especially 'I' pattern. 'I' pattern must come before 'U' pattern, 'Url' pattern must come before 'L' pattern with current patterns.

    match_patterns = tuple(TokenizerMatcherConstant.get_all_matcher())

    token_type = ("S", "Q", "I", "M", "U", "Url", "O", "C", "Ha", "No", "De", "Da", "Id", "L")


    @classmethod
    def get_tokens(cls, text):
        token_string_list = []
        token_list = []
        token_string = ''
        from fact_value.FactValue import FactValue

        if isinstance(text, str):
            text_length = len(text)
        elif isinstance(text, FactValue):
            text_length = len(str(text.get_value()))
            text = str(text.get_value())

        while text_length != 0:
            for i in range(len(cls.match_patterns)):
                regex = re.compile(cls.match_patterns[i])
                match = regex.match(text)
                if match:
                    group = match.group(0)
                    # ignore space tokens
                    if cls.token_type[i] != 'S':
                        token_string_list.append(cls.token_type[i])
                        token_list.append(group.strip())
                        token_string += str(cls.token_type[i])

                    text = text[len(group):text_length].strip()
                    text_length = len(text)
                    break

                if i >= len(cls.match_patterns) - 1:
                    text_length = 0
                    token_string = "WARNING"

        tokens = Tokens(token_list, token_string_list, token_string)

        return tokens

