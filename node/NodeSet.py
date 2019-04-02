from node import DependencyMatrix
from node.Node import Node


class NodeSet:

    def __init__(self):
        self.node_set_name = None
        self.input_dictionary = {}
        self.fact_dictionary = {}
        self.node_dictionary = {}
        self.node_id_dictionary = {}
        self.sorted_node_list = []
        self.default_goal_node = None
        self.dependency_matrix = None

    def get_dependency_matrix(self):
        return self.dependency_matrix

    def set_dependency_matrix(self, dependency_matrix):

        if isinstance(dependency_matrix, list):
            self.dependency_matrix = DependencyMatrix(dependency_matrix)
        elif isinstance(dependency_matrix, DependencyMatrix.DependencyMatrix):
            self.dependency_matrix = dependency_matrix

    def get_node_set_name(self):
        return self.node_set_name

    def set_node_set_name(self, node_set_name):
        self.node_set_name = node_set_name

    def set_node_id_dictionary(self, node_id_dictionary):
        self.node_id_dictionary = node_id_dictionary

    def get_node_id_dictionary(self):
        return self.node_id_dictionary

    def set_node_dictionary(self, node_dictionary):
        self.node_dictionary = node_dictionary

    def get_node_dictionary(self):
        return self.node_dictionary

    def set_sorted_node_list(self, sorted_node_list):
        self.sorted_node_list = sorted_node_list

    def get_sorted_node_list(self):
        return self.sorted_node_list

    def get_input_dictionary(self):
        return self.input_dictionary

    def set_fact_dictionary(self, fact_dictionary):
        self.fact_dictionary = fact_dictionary

    def get_fact_dictionary(self):
        return self.fact_dictionary

    def get_node(self, node_index):
        return self.sorted_node_list[node_index]

    def get_node(self, node_name):
        return self.node_dictionary[node_name]

    def get_node_by_node_id(self, node_id):
        return self.get_node(self.get_node_id_dictionary()[node_id])

    def find_node_index(self, node_name):

        for node_index in range(len(self.get_sorted_node_list())):
            if Node(self.get_sorted_node_list()[node_index]).get_node_name() == node_name:
                return node_index

    def set_default_goal_node(self, name):
        self.default_goal_node = self.get_node_dictionary(name)

    def get_default_goal_node(self):
        return self.default_goal_node

    def transfer_fact_dictionary_to_working_memory(self, working_memory):
        for key in self.input_dictionary:
            working_memory[key] = self.input_dictionary[key]

        return working_memory
