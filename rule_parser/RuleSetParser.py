from rule_parser import IScanFeeder
from node.NodeSet import NodeSet
from node.LineType import LineType
from rule_parser.Tokenizer import Tokenizer
from rule_parser.Tokens import Tokens
from constant.LineMatcherConstant import LineMatcherConstant
from node.MetadataLine import MetadataLine
from node.ValueConclusionLine import ValueConclusionLine
from node.ExprConclusionLine import ExprConclusionLine
from node.ComparisonLine import ComparisonLine
from fact_value.FactValue import FactValue
from fact_value.FactValueType import FactValueType
from node.DependencyType import DependencyType
from node.Dependency import Dependency
from node.MetaType import MetaType
import re

class RuleSetParser(IScanFeeder):
    #meta_pattern_matcher = r"(^U)([MLU]*)([(No)(Da)ML(De)(Ha)(U(rl)?)(Id)]*$)"
    #value_conclusion_matcher = r"(^[LM]+)(U)?([MLQ(No)(Da)(De)(Ha)(Url)(Id)]*$)(?!C)"
    #expression_conclusion_matcher = r"(^[LM(Da)]+)(U)(C)"
    #comparision_matcher = r"(^[MLU(Da)]+)(O)([MLUQ(No)(Da)(De)(Ha)(Url)(Id)]*$)"
    #iterate_matcher = r"(^[MLU(No)(Da)]+)(I)([MLU]+$)"
    #warning_matcher = r"WARNING"

    match_types = LineType.get_all_values()
    node_set = NodeSet()
    dependency_list = []

    def handle_parent(self, parent_text, line_number):

        data = self.node_set.get_node_dictionary()[parent_text];

        if data is None:
            tokens = Tokenizer.get_tokens(parent_text)
            line_match_patterns = [LineMatcherConstant.META_PATTERN_MATCHER, LineMatcherConstant.VALUE_CONCLUSION_MATCHER,
                                   LineMatcherConstant.EXPRESSION_CONCLUSION_MATCHER, LineMatcherConstant.WARNING_MATCHER]

            for i in range(len(line_match_patterns)):
                pattern = re.compile(line_match_patterns[i])
                match = pattern.match(tokens.tokens_string)
                if match:
                    if i == 3: # warning matcher
                        handle_warning(parent_text)
                    elif i == 0: # meta matcher
                        data = MetadataLine(parent_text, tokens)
                        if data.get_fact_value().get_value() == 'WARNING':
                            handle_warning(parent_text)
                    elif i == 1: # value conclusion matcher
                        data = ValueConclusionLine(parent_text, tokens)
                        if (len(match.groups()) == 2 and match.group(2) is not None)\
                            or (tokens.tokens_string == 'L' or tokens.tokens_string == 'LM' or tokens.tokens_string == 'ML' or tokens.tokens_string == 'M'):
                            variable_name = data.get_variable_name()
                            temp_node = data

                            # following lines are to look for any nodes having a its nodeName with any operators due to the reason that
                            # the node could be used to define a node previously used as a child node for other nodes

                            possible_parent_node_key_list = list(filter(lambda key: re.search(r"(.+)?(\s[<>=]+\s?)?("+variable_name+")(\s[<>=]+)*(.(?!(IS)))*(.*(IS IN LIST).*)*", key), self.node_set.get_node_dictionary().keys()))
                            if len(possible_parent_node_key_list) > 0:
                                for item in possible_parent_node_key_list:
                                    self.dependency_list.append(Dependency(self.node_set.get_node_dictionary()[item], temp_node, DependencyType.get_or()))  # Dependency Type: OR

                            if data.get_fact_value().get_value() == 'WARNING':
                                handle_warning(parent_text)

                    elif i == 2: # expr conclusion matcher
                        data = ExprConclusionLine(parent_text, tokens)
                        variable_name = data.get_variable_name()
                        temp_node = data

                        # following lines are to look for any nodes having a its nodeName with any operators due to the reason that
                        # the exprConclusion node could be used to define another node as a child node for other nodes if the variableName of exprConclusion node is mentioned somewhere else.
                        # However, it is excluding nodes having 'IS' keyword because if it has the keyword then it should have child nodes to define the node otherwise the entire rule set has NOT been written in correct way

                        possible_parent_node_key_list = list(filter(lambda key: re.match(r"(.+)?(\\s[<>=]+\\s?)?(" + variable_name + ")(\\s[<>=]+)*(.(?!(IS)))*(.*(IS IN LIST).*)*", key), self.node_set.get_node_dictionary().keys()))
                        if len(possible_parent_node_key_list) > 0:
                            for item in possible_parent_node_key_list:
                                self.dependency_list.append(Dependency(self.node_set.get_node_dictionary()[item], temp_node, DependencyType.get_or())) # Dependency Type: OR

                        if data.get_fact_value().get_value() == 'WARNING':
                            handle_warning(parent_text)

                    else:
                        handle_warning(parent_text)

                data.set_node_line(line_number)

                if data.get_line_type() == LineType.META:
                    if data.get_meta_type() == MetaType.INPUT:
                        self.node_set.get_input_dictionary()[data.get_variable_name()] = data.get_fact_value()
                    elif data.get_meta_type() == MetaType.FIXED:
                        self.node_set.get_fact_dictionary()[data.get_variable_name()] = data.get_fact_value()
                    else:
                        self.node_set.get_node_dictionary()[data.get_node_name()] = data
                        self.node_set.get_node_id_dictionary()[data.get_node_id()] = data.get_node_name()

                break

    def handle_child(self, parent_text, child_text, first_Key_words_group, line_number):

        # the reason for using '*' at the last group of pattern within comparison is that
        # the last group contains No, Da, De, Ha, Url, Id.
        # In order to track more than one character within the square bracket of last group '*'(Matches 0 or more occurrences of the preceding expression) needs to be used.

        dependency_type = 0


        if re.match(r"(ITEM)(.*)", child_text): # is 'ITEM' child line
            if not re.match(r"(.*)(AS LIST)", parent_text):
                handle_warning(child_text)
                return

            # is an indented item child
            child_text = child_text.replace("ITEM", "", 1).strip()
            if re.match(r"^(INPUT)(.*)", parent_text):
                meta_type = MetaType.INPUT
            elif re.match(r"^(FIXED)(.*)", parent_text):
                meta_type = MetaType.FIXED
            handle_list_item(parent_text, child_text, meta_type)
        else:  # is 'A-statement', 'A IS B', 'A <= B', or 'A IS CALC (B * C)' child line
            if re.match(r"^(AND\\s?)(.*)", first_Key_words_group):
                dependency_type = handle_not_known_man_opt_pos(first_Key_words_group, DependencyType.get_and()) # 8 - AND | 1 - KNOWN? 2 - NOT? 64 - MANDATORY? 32 - OPTIONALLY? 16 - POSSIBLY?
            elif re.match(r"^(OR\\s?)(.*)", first_Key_words_group):
                dependency_type = handle_not_known_man_opt_pos(first_Key_words_group, DependencyType.get_or()) # 4 - OR | 1 - KNOWN? 2 - NOT? 64 - MANDATORY? 32 - OPTIONALLY? 16 - POSSIBLY?
            elif re.match(r"^(WANTS)", first_Key_words_group):
                dependency_type = handle_not_known_man_opt_pos(first_Key_words_group, DependencyType.get_or()) #4 - OR
            elif re.match(r"^(NEEDS)", first_Key_words_group):
                dependencyType = DependencyType.get_mandatory() | DependencyType.get_and(); # 8 - AND | 64 - MANDATORY

            # the keyword of 'AND' or 'OR' should be removed individually.
            # it should NOT be removed by using firstToken string in Tokens.tokensList.get(0)
            # because firstToken string may have something else.
            # (e.g. string: 'AND NOT ALL Males' name should sound Male', then Token string will be 'UMLM', and 'U' contains 'AND NOT ALL'.
            # so if we used 'firstToken string' to remove 'AND' in this case as 'string.replace(firstTokenString)'
            # then it will remove 'AND NOT ALL' even we only need to remove 'AND'

            data = self.node_set.get_node_dictionary()[child_text]
            tokens = Tokenizer.get_tokens(child_text)

            if data is None:
                match_patterns = [LineMatcherConstant.VALUE_CONCLUSION_MATCHER, LineMatcherConstant.COMPARISON_MATCHER, LineMatcherConstant.ITERATE_MATCHER, LineMatcherConstant.EXPRESSION_CONCLUSION_MATCHER, LineMatcherConstant.WARNING_MATCHER]
                for pattern_index in range(len(match_patterns)):
                    pattern = match_patterns[pattern_index]
                    match = re.match(pattern, tokens.tokens_string)
                    if match:
                        if pattern_index == 4: # warning matcher
                            handle_warning(child_text)
                        elif pattern_index == 0: # value conclusion matcher
                            data = ValueConclusionLine(child_text, tokens)
                            temp_node = data
                            possible_child_node_key_list = list(filter(lambda key: re.match(r"^(" + temp_node.get_variable_name() + ")(\\s+(IS(?!(\\s+IN\\s+LIST))).*)*$", key), self.node_set.get_node_dictionary().keys()))
                            if len(possible_child_node_key_list) > 0:
                                for item in possible_child_node_key_list:
                                    self.dependency_list.append(Dependency(temp_node, self.node_set.get_node_dictionary()[item], DependencyType.get_or())) # Dependency Type: OR
                            if data.get_fact_value().get_value() == "WARNING":
                                handle_warning(child_text)
                        elif pattern_index == 1: #comparison matcher
                            data = ComparisonLine(child_text, tokens)
                            rhs_type = data.get_rhs().get_value_type()
                            rhs_string = data.get_rhs().get_value()
                            lhs_string = data.get_lhs()
                            temp_node = data
                            if rhs_type == FactValueType.STRING:
                                possible_child_node_key_list = list(filter(lambda key: re.match(r"^(" + lhs_string + ")(\s+(IS(?!(\s+IN\s+LIST))).*)*$", key)
                                                        or re.match(r"^(" + rhs_string + ")(\s+(IS(?!(\s+IN\s+LIST))).*)*$"), self.node_set.get_node_dictionary().keys()))
                            else:
                                possible_child_node_key_list = list(filter(lambda key: re.match(r"^(" + lhs_string + ")(\\s+(IS(?!(\\s+IN\\s+LIST))).*)*$",), self.node_set.get_node_dictionary().keys()))


                            if len(possible_child_node_key_list) > 0:
                                for item in possible_child_node_key_list:
                                    self.dependency_list.append(Dependency(temp_node, self.node_set.get_node_dictionary()[item], DependencyType.get_or())) # Dependency Type: OR

                            if data.get_fact_value().get_value_type() == FactValueType.WARNING:
                                handle_warning(parent_text)

                        elif pattern_index == 2: # iterate matcher
                            data = IterateLine(child_text, tokens)
                            if data.get_fact_value().get_fact_value_type() == FactValueType.WARNING:
                                handle_warning(parent_text)

HandleChild

                2: // comparisonMatcher
                case
                data = new
                IterateLine(childText, tokens);
                if (FactValue.GetValueInString(data.GetFactValue().GetFactValueType(), data.GetFactValue()).Equals(
                        "WARNING"))
                    {
                        HandleWarning(parentText);
                    }
                    break;
                    case
                    3: // exprConclusionMatcher
                    case
                    data = new
                    ExprConclusionLine(childText, tokens);

                    / *
                    *In
                    this
                    case, there is no
                    mechanism
                    to
                    find
                    possible
                    parent
                    nodes.
                    *I
                    have
                    brought
                    'local variable'
                    concept
                    for this case due to it may massed up with structuring node dependency tree with topological sort
                    *If
                    ExprConclusion
                    node is used as a
                    child, then
                    it
                    means
                    that
                    this
                    node is a
                    local
                    node
                    which
                    has
                    to
                    be
                    strictly
                    bound
                    to
                    its
                    parent
                    node
                    only.
                    * /

                    if (FactValue.GetValueInString(data.GetFactValue().GetFactValueType(), data.GetFactValue()).Equals(
                            "WARNING"))
                        {
                            HandleWarning(parentText);
                    }
                    break;

                    }
                    data.SetNodeLine(lineNumber);
                    this.nodeSet.GetNodeMap().Add(data.GetNodeName(), data);
                    this.nodeSet.GetNodeIdMap().Add(data.GetNodeId(), data.GetNodeName());
                    break;
                    }
                    }
                    }

                    this.dependencyList.Add(new
                    Dependency(this.nodeSet.GetNode(parentText), data, dependencyType));
                    }

                    }