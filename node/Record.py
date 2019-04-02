class Record:
    name = None
    type = None
    true_count = 0
    false_count = 0

    def __init__(self, name=None, type=None, true_count=None, false_count=None):
        self.name = name
        self.type = type
        self.true_count = true_count
        self.false_count = false_count

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_type(self, type):
        self.type = type
    def get_type(self):
        return self.type

    def set_true_count(self, true_count):
        self.true_count = true_count
    def get_true_count(self):
        return self.true_count

    def add_true_count(self, true_count):
        self.true_count+= true_count
    def increment_true_count(self):
        self.true_count += self.true_count
    def get_true_count(self):
        self.true_count

    def set_false_count(self, false_count):
        self.false_count = false_count
    def add_false_count(self, false_count):
        self.false_count += false_count
    def increment_false_count(self):
        self.false_count += self.false_count
    def get_false_count(self):
        return self.false_count
