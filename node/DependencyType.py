class DependencyType:

    def __init__(self): pass

    mandatory_dependency = 64  # 1000000
    optional_dependency = 32   # 0100000
    possible_dependency = 16   # 0010000
    and_dependency = 8         # 0001000
    or_dependency = 4          # 0000100
    not_dependency = 2         # 0000010
    known_dependency = 1       # 0000001

    @staticmethod
    def get_mandatory(self):
        return self.mandatory_dependency

    @staticmethod
    def get_optional(self):
        return self.optional_dependency

    @staticmethod
    def get_possible(self):
        return self.possible_dependency

    @staticmethod
    def get_and(self):
        return self.and_dependency

    @staticmethod
    def get_or(self):
        return self.or_dependency

    @staticmethod
    def get_not(self):
        return self.not_dependency

    @staticmethod
    def get_known(self):
        return self.known_dependency
