from node.Node import Node
from rule_parser.Tokens import Tokens
from node.NodeSet import NodeSet
from node.DependencyMatrix import DependencyMatrix
from node.LineType import LineType
from node.ValueConclusionLine import ValueConclusionLine
from node.ComparisonLine import ComparisonLine
from node.ExprConclusionLine import ExprConclusionLine
from node.Dependency import Dependency
from fact_value.FactValue import FactValue
from fact_value.FactValueType import FactValueType
import re


class IterateLine(Node):

    number_of_target = None
    iterate_node_set = None
    given_list_name = None
    given_list_size = 0
    iterate_IE = None

    def __init__(self, parent_text: str, tokens: Tokens):
        super().__init__(parent_text, tokens)


    def get_given_list_name(self):
        return self.given_list_name

    def get_number_of_target(self):
        return self.number_of_target

    def create_iterate_node_set(self, parent_node_set: NodeSet):
        parent_dependency_matrix: DependencyMatrix = parent_node_set.get_dependency_matrix()
        parent_node_dictionary = parent_node_set.get_node_dictionary()
        parent_node_id_dictionary = parent_node_set.get_node_id_dictionary()

        this_node_dictionary = dict()
        this_node_id_dictionary = dict()
        temp_dependency_list = list()
        new_node_set = NodeSet()

        this_node_dictionary[self.node_name] =  self
        this_node_id_dictionary[self.node_id] = self.node_name

        for nth in range(1, self.given_list_size):
            for item in parent_dependency_matrix.get_to_child_dependency_list():
                if self.get_node_id() + 1 != item: # not first question id
                    temp_child_node: Node = parent_node_dictionary[parent_node_id_dictionary[item]]
                    line_type = temp_child_node.get_line_type()
                    next_nth_in_string = self.Ordinal(nth)

                    if line_type == LineType.VALUE_CONCLUSION:
                        temp_node = ValueConclusionLine(next_nth_in_string + " " + self.get_variable_name() + " " + temp_child_node.get_node_name(), temp_child_node.get_tokens())
                    elif line_type == LineType.COMPARISON:
                        temp_node = ComparisonLine(next_nth_in_string + " " + self.get_variable_name() + " " + temp_child_node.get_node_name(), temp_child_node.GetTokens())
                        temp_node_fact_value = temp_node.get_rhs()
                        if temp_node_fact_value.get_value_type() == FactValueType.STRING:
                            temp_fact_value = FactValue(next_nth_in_string + " " + self.get_variable_name()+ " " + temp_node_fact_value.get_value())
                            temp_node.set_value(temp_fact_value)

                    elif line_type == LineType.EXPR_CONCLUSION:
                        temp_node = ExprConclusionLine(next_nth_in_string + " " + self.get_variable_name() + " " + temp_child_node.get_node_name(), temp_child_node.get_tokens())

                    this_node_dictionary[temp_node.get_node_name()] = temp_node
                    this_node_id_dictionary[temp_node.get_node_id()] = temp_node.get_node_name()
                    temp_dependency_list.append(Dependency(self, temp_node, parent_dependency_matrix.get_dependency_type(self.node_id, item)))

                    self.create_iterate_node_set_aux(parent_dependency_matrix, parent_node_dictionary,
                                                parent_node_id_dictionary, this_node_dictionary,
                                                this_node_id_dictionary, temp_dependency_list,
                                                item, temp_node.get_node_id(), next_nth_in_string)

                else: # first question id
                    first_iterate_question_node = parent_node_set.get_node_by_node_id(min(parent_node_set.get_dependency_matrix().get_to_child_dependency_list(self.get_node_id())))

                    if first_iterate_question_node.get_node_name() not in this_node_dictionary.keys():
                        this_node_dictionary[first_iterate_question_node.get_node_name()] = first_iterate_question_node
                        this_node_id_dictionary[item] = first_iterate_question_node.get_node_name()
                        temp_dependency_list.append(Dependency(self, first_iterate_question_node, parent_dependency_matrix.get_dependency_type(self.node_id, item)))

        number_of_rules = Node.get_static_node_id()
        dependency_matrix = [[0 for x in range(number_of_rules)] for y in range(number_of_rules)]
        for dp in temp_dependency_list:
            parent_id = dp.get_parent_node().get_node_id()
            child_id = dp.get_child_node().get_node_id()
            dependency_type = dp.get_dependency_type()
            dependency_matrix[parent_id][child_id] = dependency_type

        new_node_set.set_node_id_dictionary(this_node_id_dictionary)
        new_node_set.set_node_dictionary(this_node_dictionary)
        new_node_set.set_dependency_matrix(DependencyMatrix(dependency_matrix))
        new_node_set.set_fact_dictionary(parent_node_set.get_fact_dictionary())
        new_node_set.set_node_sorted_list(self.dfs_topological_sort())

        return  new_node_set

    def create_iterate_node_set_aux(self, parent_dependency_matrix: DependencyMatrix, parent_node_dictionary: dict, parent_node_id_dictionary: dict,
                                    this_node_dictionary: dict, this_node_id_dictionary: dict, temp_dependency_list: list,
                                    original_parent_id, modified_parent_id, next_nth_in_string):
        child_dependency_list = parent_dependency_matrix.get_to_child_dependency_list(original_parent_id)

        if len(child_dependency_list) > 0:
            for item in child_dependency_list:
                temp_child_node = parent_dependency_matrix[parent_node_id_dictionary[item]]
                line_type = temp_child_node.get_line_type()
                temp_node = this_node_dictionary[next_nth_in_string+" "+self.get_variable_name()+" "+temp_child_node.get_node_name()]
                if temp_child_node is None:
                    if line_type == LineType.VALUE_CONCLUSION:
                        temp_node = ValueConclusionLine(next_nth_in_string+" "+self.get_variable_name()+" "+temp_child_node.get_node_name(),
                                                        temp_child_node.get_tokens())
                        if parent_node_dictionary[parent_node_id_dictionary[original_parent_id]].get_line_type() == LineType.EXPR_CONCLUSION:
                            expr_temp_node: ExprConclusionLine = this_node_dictionary[this_node_id_dictionary[modified_parent_id]]
                            replaced_string = str(expr_temp_node.get_equation().get_value()).replace(temp_child_node.get_node_name(), next_nth_in_string+" "+self.get_variable_name()+" "+temp_child_node.get_node_name())
                            expr_temp_node.set_value(FactValue(replaced_string, FactValueType.STRING))
                            expr_temp_node.set_equation(FactValue(replaced_string, FactValueType.STRING))
                    elif line_type == LineType.COMPARISON:
                        temp_node = ComparisonLine(next_nth_in_string+" "+self.get_variable_name()+" "+temp_child_node.get_node_name(), temp_child_node.get_tokens())
                        temp_node_fv = temp_node.get_rhs()
                        if temp_node_fv.get_value_type() == FactValueType.STRING:
                            temp_fv = FactValue(next_nth_in_string+" "+self.get_variable_name()+" "+temp_node_fv, FactValueType.STRING)
                            temp_node.set_value(temp_fv)
                    elif line_type == LineType.EXPR_CONCLUSION:
                        temp_node = ExprConclusionLine(next_nth_in_string+" "+self.get_variable_name()+" "+temp_child_node.get_node_name(), temp_child_node.get_tokens())
                else:
                    if (line_type == LineType.VALUE_CONCLUSION) and \
                        (parent_node_dictionary[parent_node_id_dictionary[original_parent_id]].get_line_type() == LineType.EXPR_CONCLUSION):
                        expr_temp_node = this_node_dictionary[this_node_id_dictionary[modified_parent_id]]
                        replaced_string = str(expr_temp_node.get_equation()).replace(temp_child_node.get_node_name(), next_nth_in_string+" "+self.get_variable_name()+" "+temp_child_node.get_node_name())
                        expr_temp_node.set_value(FactValue(replaced_string, FactValueType.STRING))
                        expr_temp_node.set_equation(FactValue(replaced_string, FactValueType.STRING))

                if temp_node.get_node_name() not in this_node_dictionary:
                    this_node_dictionary[temp_node.get_node_name()] = temp_node
                    this_node_id_dictionary[temp_node.get_node_id()] = temp_node.get_node_name()
                    temp_dependency_list.append(Dependency(this_node_dictionary[this_node_id_dictionary[modified_parent_id]], temp_node, parent_dependency_matrix.get_dependency_type(original_parent_id, item)))

                    self.create_iterate_node_set_aux(parent_dependency_matrix, parent_node_dictionary, parent_node_id_dictionary, this_node_dictionary, this_node_id_dictionary, temp_dependency_list, item, temp_node.get_node_id(), next_nth_in_string)

    def get_iterate_nodeSet(self):
        return self.iterate_node_set

    # this method is used when a givenList exists as a string
    # this method uses JSON object via jackson library
    def iterate_feed_answers(given_json_string: str,  parent_node_set: NodeSet, parent_assessment_state: AssessmentState, assessment: Assessment)
        # givenJsonString has to be in same format as Example otherwise the engine would NOT be able to enable 'IterateLine' node
        # String givenJsonString = "{
        #    							\"iterateLineVariableName\":
        #							        [
        #								        {
        #       									\"1st iterateLineVariableName\":
        #       										{
        #       										  \"1st iterateLineVariableName ruleNme1\":\"..value..\",
        #       										  \"1st iterateLineVariableName ruleNme2\":\"..value..\"
        #       										}
        #       								 },
        #       								 {
        #       									\"2nd iterateLineVariableName\":
        #       										{
        #       										  \"2nd iterateLineVariableName ruleNme1\":\"..value..\",
        #       										  \"2nd iterateLineVariableName ruleNme2\":\"..value..\"
        #       										}
        #       								 },
        #										]
        #							}"
        #-----------------------------  "givenJsonString" Example ----------------------------
        #     String givenJsonString = "{
        #									\"service\":
        #									    [
        #										  {
        #											\"1st service\":
        #       										{
        #               								  \"1st service period\":\"..value..\",
        #												  \"1st service type\":\"..value..\"
        #												}
        #										  },
        #										  {
        #											\"2nd service\":
        #												{
        #												  \"2nd service period\":\"..value..\",
        #												  \"2nd service type\":\"..value..\"}
        #										  }
        #										]
        #								 }";






JObject
jObject = JObject.Parse(givenJsonString);
List < JToken > serviceList = jObject.Property(this.variableName).ToList();
this.givenListSize = serviceList.Count;

if (this.iterateNodeSet == null)
    {
        this.iterateNodeSet = CreateIterateNodeSet(parentNodeSet);
    this.iterateIE = new
    InferenceEngine(this.iterateNodeSet);
    if (this.iterateIE.GetAssessment() == null)
    {
    this.iterateIE.SetAssessment(new Assessment(this.iterateNodeSet, this.GetNodeName()));
    }
    }
while (!this.iterateIE.GetAssessmentState().GetWorkingMemory().ContainsKey(this.nodeName))
{
    Node
nextQuestionNode = GetIterateNextQuestion(parentNodeSet, parentAst);
string
answer = "";
Dictionary < string, FactValueType > questionFvtMap = this.iterateIE.FindTypeOfElementToBeAsked(nextQuestionNode);
foreach(string
question in this.iterateIE.GetQuestionsFromNodeToBeAsked(nextQuestionNode))
{
// answer = jObject.GetValue(this.variableName)
            //.SelectToken
               // jsonObj.get(this.variableName)
               //.get(nextQuestionNode.getVariableName().substring(0, nextQuestionNode.getVariableName().lastIndexOf(
    this.variableName) + this.variableName.length()))
                  //.get(nextQuestionNode.getVariableName())
                     //.asText().trim();

this.iterateIE.FeedAnswerToNode(nextQuestionNode, question, FactValue.Parse(answer), this.iterateIE.GetAssessment());
}

Dictionary < string, FactValue > iterateWorkingMemory = this.iterateIE.GetAssessmentState().GetWorkingMemory();
Dictionary < String, FactValue > parentWorkingMemory = parentAst.GetWorkingMemory();

TranseferFactValue(iterateWorkingMemory, parentWorkingMemory);

}
}

// / *
// *this
method is used
when
a
givenList
does
NOT
exist
// * /
public
void
IterateFeedAnswers(Node
targetNode, string
questionName, FactValue
nodeValue, NodeSet
parentNodeSet, AssessmentState
parentAst, Assessment
ass)
{

if (this.iterateNodeSet == null)
    {
        Node
    firstIterateQuestionNode = parentNodeSet.GetNodeByNodeId(
        parentNodeSet.GetDependencyMatrix().GetToChildDependencyList(this.GetNodeId()).Min());
    if (questionName.Equals(firstIterateQuestionNode.GetNodeName()))
    {
    this.givenListSize = Int32.Parse(FactValue.GetValueInString(nodeValue.GetFactValueType(), nodeValue));
    }
    this.iterateNodeSet = CreateIterateNodeSet(parentNodeSet);
    this.iterateIE = new InferenceEngine(this.iterateNodeSet);
    if (this.iterateIE.GetAssessment() == null)
    {
    this.iterateIE.SetAssessment(new Assessment(this.iterateNodeSet, this.GetNodeName()));
    }
    }
this.iterateIE.GetAssessment().SetNodeToBeAsked(targetNode);
this.iterateIE.FeedAnswerToNode(targetNode, questionName, nodeValue, this.iterateIE.GetAssessment());

Dictionary < string, FactValue > iterateWorkingMemory = this.iterateIE.GetAssessmentState().GetWorkingMemory();
Dictionary < string, FactValue > parentWorkingMemory = parentAst.GetWorkingMemory();

TranseferFactValue(iterateWorkingMemory, parentWorkingMemory);

}

public
void
TranseferFactValue(Dictionary < string, FactValue > workingMemory_one, Dictionary < string,
                   FactValue > workingMemory_two)
{
workingMemory_one.Keys.ToList().ForEach((key) = >
{
    FactValue
tempFv = workingMemory_one[key];
if (!workingMemory_two.ContainsKey(key))
{
    workingMemory_two.Add(key, tempFv);
}
});
}

public
Node
GetIterateNextQuestion(NodeSet
parentNodeSet, AssessmentState
parentAst)
{
if (this.iterateNodeSet == null & & this.givenListSize != 0)
    {
        this.iterateNodeSet = CreateIterateNodeSet(parentNodeSet);
    this.iterateIE = new
    InferenceEngine(this.iterateNodeSet);
    if (this.iterateIE.GetAssessment() == null)
    {
    this.iterateIE.SetAssessment(new Assessment(this.iterateNodeSet, this.GetNodeName()));
    }
    }

Node
firstIterateQuestionNode = parentNodeSet.GetNodeByNodeId(
    parentNodeSet.GetDependencyMatrix().GetToChildDependencyList(this.GetNodeId()).Min());
Node
questionNode = null;

if (!parentAst.GetWorkingMemory().ContainsKey(FactValue.GetValueInString(this.value.GetFactValueType(),
                                                                         this.value))) // a list is not given yet so that the engine needs to find out more info.
{

if (!parentAst.GetWorkingMemory().ContainsKey(firstIterateQuestionNode.GetNodeName()))
{
    questionNode = firstIterateQuestionNode;
}
else
{
if (!CanBeSelfEvaluated(parentAst.GetWorkingMemory()))
{
    questionNode = this.iterateIE.GetNextQuestion(this.iterateIE.GetAssessment());
}
}
}


return questionNode;
}


public
int
FindNTh(Dictionary < string, FactValue > workingMemory)
{
return Enumerable.Range(1, this.givenListSize)
.Where((item) = > workingMemory[Oridinal(item) + " " + this.variableName] != null)
.ToList().Count;
}

public
String
Oridinal(int
i)
{
String[]
sufixes = new
String[]
{"th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th"};
switch(i % 100)
{
    case
11:
case
12:
case
13:
return i + "th";
default:
return i + sufixes[i % 10];
}
}


public
override
void
Initialisation(string
parentText, Tokens
tokens) {
    this.nodeName = parentText;
this.numberOfTarget = tokens.tokensList[0];
this.variableName = tokens.tokensList[1];
int
tokensStringListSize = tokens.tokensStringList.Count;
string
lastToken = tokens.tokensList[tokensStringListSize - 1]; // this is a
givenListName.
    string
lastTokenString = tokens.tokensStringList[tokensStringListSize - 1];
this.SetValue(lastTokenString, lastToken);
this.givenListName = lastToken;

}

public
override
LineType
GetLineType()
{
return LineType.ITERATE;
}


public
bool
CanBeSelfEvaluated(Dictionary < string, FactValue > workingMemory)
{
bool
canBeSelfEvaluated = false;
if (this.iterateIE != null)
    {
        FactValue
    outFactValue = null;
    List < int > numberOfDeterminedSecondLevelNode = this.iterateIE.GetNodeSet().GetDependencyMatrix().GetToChildDependencyList(
        this.nodeId)
        .Where((i) = > i != this.nodeId + 1)
    .Where((id) = > workingMemory.TryGetValue(this.iterateIE.GetNodeSet().GetNodeIdMap()[id], out
    outFactValue) & & outFactValue != null & & FactValue.GetValueInString(outFactValue.GetFactValueType(),
                                                                          outFactValue) != null)
    .ToList();

    if (this.givenListSize == numberOfDeterminedSecondLevelNode.Count & & this.iterateIE.HasAllMandatoryChildAnswered(
            this.nodeId))
    {
    canBeSelfEvaluated = true;
    }
    }

return canBeSelfEvaluated;
}


public
override
FactValue
SelfEvaluate(Dictionary < string, FactValue > workingMemory, Jint.Engine
nashorn)
{

int
numberOfTrueChildren = NumberOfTrueChildren(workingMemory);
int
sizeOfGivenList = this.givenListSize;
FactBooleanValue
fbv = null;
switch(this.numberOfTarget)
{
    case
"ALL":
if (numberOfTrueChildren == sizeOfGivenList)
{
fbv = FactValue.Parse(true);
}
else
{
fbv = FactValue.Parse(false);
}
break;
case
"NONE":
if (numberOfTrueChildren == 0)
    {
        fbv = FactValue.Parse(true);
    }
    else
    {
        fbv = FactValue.Parse(false);
    }
    break;
    case
    "SOME":
    if (numberOfTrueChildren > 0)
        {
            fbv = FactValue.Parse(true);
        }
        else
        {
            fbv = FactValue.Parse(false);
        }
        break;
        default:
        if (numberOfTrueChildren == Int32.Parse(this.numberOfTarget))
            {
                fbv = FactValue.Parse(true);
            }
            else
            {
                fbv = FactValue.Parse(false);
            }
            break;
            }
            return fbv;
            }

            public
            int
            NumberOfTrueChildren(Dictionary < string, FactValue > workingMemory)
            {
            return this.iterateIE.GetNodeSet().GetDependencyMatrix().GetToChildDependencyList(this.nodeId)
            .Where((i) = > i != this.nodeId + 1)
            .Where((id) = > FactValue.GetValueInString(
                workingMemory[this.iterateIE.GetNodeSet().GetNodeIdMap()[id]].GetFactValueType(),
                workingMemory[this.iterateIE.GetNodeSet().GetNodeIdMap()[id]]).ToLower().Equals("true"))
            .ToList().Count;

            }
