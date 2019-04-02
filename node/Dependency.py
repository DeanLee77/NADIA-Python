class Dependency:
    dependency_type = None # this variable is to store 'AND/OR' DependencyType between Nodes
    parent = None # this variable is to store a parent Node of this dependency
    child = None # this variable is to store a child Node of this dependency

    def __init__(self, parent, child, dependency_type):
        self.parent = parent
        self.child = child
        self.dependency_type = dependency_type

    def get_parent_node(self):
        return self.parent

    def set_parent_node(self, parent):
        self.parent = parent

    def get_child_node(self):
        return self.child

    def set_child_node(self, child):
        self.child = child

    def get_dependency_type(self):
        return self.dependency_type
