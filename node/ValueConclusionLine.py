from node.Node import Node
from node.LineType import LineType
from fact_value.FactValue import FactValue
from fact_value.FactValue import FactValue
from rule_parser.Tokens import Tokens


class ValueConclusionLine(Node):

    # ValueConclusionLine format is as follows;
    # 1. 'A-statement IS B-statement';
    # 2. 'A-item name IS IN LIST: B-list name'; or
    # 3. 'A-statement'(plain statement line) including statement of 'A' type from a child node of ExprConclusionLine type which are 'NEEDS' and 'WANTS'.
    # When the inference engine reaches at a ValueConclusionLine and needs to ask a question to a user,
    # Hence, the question can be from either variableName or ruleName, and a result of the question will be inserted into the workingMemory.
    # However, when the engine reaches at the line during forward-chaining then the key for the workingMemory will be a ruleName,
    # and value for the workingMemory will be set as a result of propagation.
    #
    # If the rule statement is in a format of 'A-statement' then a default value of variable 'value' will be set as 'false'

    is_plain_statement_format = None

    def __init__(self, node_text, tokens):
        super().__init__(node_text, tokens)

    def initialisation(self, node_text: str, tokens: Tokens):
        token_string_list_size = len(tokens.tokens_string_list) # tokens.tokensStringList.size is same as tokens.tokensList.size
        self.is_plain_statement_format = len(list(filter(lambda c: 'IS' in c, tokens.tokens_list))) == 0 # this will exclude 'IS' and 'IS IN  LIST:' within the given 'tokens'

        if not self.is_plain_statement_format:      # the line must be a parent line in this case other than a case of the rule contains 'IS IN LIST:'
            self.variable_name = node_text[:node_text.index('IS')].strip()
            last_token = tokens.tokens_list[token_string_list_size - 1]
        else:      # this is a case of that the line is in a 'A-statement' format
            self.variable_name = node_text
            last_token = 'False'
        self.node_name = node_text
        last_token_string = tokens.tokens_string_list[token_string_list_size - 1]
        self.set_value(last_token_string, last_token)

    def get_is_plain_statement(self) -> bool:
        return self.is_plain_statement_format

    def get_line_type(self) -> LineType:
        return LineType.VALUE_CONCLUSION

    def self_evaluate(self, working_memory: dict) -> FactValue:
        # Negation and Known type are a part of dependency
        # hence, only checking its variableName value against the workingMemory is necessary.
        # type is as follows;
        #  1. the rule is a plain statement
        #  2. the rule is a statement of 'A IS B'
        #  3. the rule is a statement of 'A IS IN LIST: B'
        #  4. the rule is a statement of 'needs(wants) A'. this is from a child node of ExprConclusionLine type

        if not self.is_plain_statement_format:
            if len(list(filter(lambda c: c == 'IS', list(self.tokens.tokens_list)))) > 0:
                fv = self.value
            elif len(list(filter(lambda c: c == 'IS IN LIST', list(self.tokens.tokens_list)))):
                line_value = False
                list_name = self.get_fact_value().get_value()
                if working_memory[list_name] is not None:
                    variable_value_from_working_memory = working_memory[self.variable_name]
                    if variable_value_from_working_memory is not None:
                        line_value = \
                            len(list(filter(lambda fact_value: fact_value.get_value() == variable_value_from_working_memory.get_value(),
                                   working_memory[list_name].get_value()))) > 0
                    else:
                        line_value = \
                           len(list(filter(lambda fact_value: self.variable_name == fact_value.get_value(),
                                  working_memory[list_name].get_value()))) > 0
                fv = FactValue.parse(line_value)

            return fv
