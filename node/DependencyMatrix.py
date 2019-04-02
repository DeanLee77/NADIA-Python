from node import DependencyType


class DependencyMatrix:

    def __init__(self, dependency_two_dimension_list):
        self.dependency_two_dimension_list = dependency_two_dimension_list
        self.dependency_list_size = len(dependency_two_dimension_list)

    def get_dependency_two_dimension_list(self):
        return self.dependency_two_dimension_list

    def get_dependency_type(self, parent_rule_id, child_rule_id):
        return self.dependency_two_dimension_list[parent_rule_id][child_rule_id]

    def get_to_child_dependency_list(self, node_id):

        to_child_dependency_list = []
        target_node_dependency_list = self.dependency_two_dimension_list[node_id]

        for child_index in range(len(target_node_dependency_list)):
            if (target_node_dependency_list[child_index] != 0) and (child_index != node_id):
                to_child_dependency_list.append(self, child_index)

        return to_child_dependency_list

    def get_or_to_child_dependency_list(self, node_id):
        or_to_child_dependency_list = []
        target_node_dependency_list = self.dependency_two_dimension_list[node_id]
        or_dependency = DependencyType.DependencyType.get_or()

        for child_index in range(len(target_node_dependency_list)):
            if (child_index != node_id) and ((target_node_dependency_list[child_index] and or_dependency) is or_dependency):
                or_to_child_dependency_list.append(self, child_index)

        return or_to_child_dependency_list

    def get_and_to_child_dependency_list(self, node_id):
        and_to_child_dependency_list = []
        target_node_dependency_list = self.dependency_two_dimension_list[node_id]
        and_dependency = DependencyType.DependencyType.get_and()

        for child_index in range(len(target_node_dependency_list)):
            if (child_index != node_id) and ((target_node_dependency_list[child_index] and and_dependency) is and_dependency):
                and_to_child_dependency_list.append(self, child_index)

        return and_to_child_dependency_list

    def get_mandatory_to_child_dependency_list(self, node_id):
        mandatory_child_dependency_list = []
        target_node_dependency_list = self.dependency_two_dimension_list[node_id]
        mandatory_dependency = DependencyType.DependencyType.get_mandatory()

        for child_index in range(len(target_node_dependency_list)):
            if (child_index != node_id) and ((target_node_dependency_list[child_index] and mandatory_dependency) is mandatory_dependency):
                mandatory_child_dependency_list.append(self, child_index)

        return mandatory_child_dependency_list

    def get_from_parent_dependency_list(self, node_id):

        from_parent_dependency_list = []

        for parent_index in range(len(self.dependency_two_dimension_list)):
            if (parent_index != node_id) and (self.dependency_two_dimension_list[parent_index][node_id] != 0):
                from_parent_dependency_list.append(self, parent_index)

        return from_parent_dependency_list

    def has_mandatory_child_node(self, node_id):

        return self.get_mandatory_to_child_dependency_list(node_id)
