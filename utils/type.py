class Variable:
    def __init__(self, name, think):
        self.name = name
        self.think = think

    def to_dict(self):
        return {
            'name': self.name,
            'think': self.think
        }

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) == str:
            return self.name == other
        return self.name == other.name
