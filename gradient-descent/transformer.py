class Variable:
    def __init__(self, name, data):
        self.name = name
        self.data = data

class Transformer:
    def __init__(self, data):
        self.data = data
        self.variables = []

        self.add_new_term('x0', lambda l : 1)

    def add_new_term(self, name, fn):
        d = map(fn, self.data)
        v = Variable(name, d)
        self.variables.append(v)

    def add_linear_terms(self):
        n = len(self.data[0])
        for i in range(n):
            self.add_new_term('x' + str(i+1), lambda l : l[i])
