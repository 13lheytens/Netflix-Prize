from __future__ import division

import math
from log import Log

class Hypothesis(object):
    def __init__(self, n):
        self.n = n
        self.theta_values = [1] * n

    def apply_deltas(self, deltas):
        self.theta_values = map(lambda t: t[0] - t[1], zip(self.theta_values, deltas))

    def sum_of_products(self, values):
        return sum(map(lambda t : t[0] * t[1], zip(values, self.theta_values)))

class LinearHypothesis(Hypothesis):
    def __init__(self, n):
        super(LinearHypothesis, self).__init__(n)

    def calculate(self, values):
        return super(LinearHypothesis, self).sum_of_products(values)

class LogisticHypothesis(Hypothesis):
    def __init__(self, n):
        super(LogisticHypothesis, self).__init__(n)

    def calculate(self, values):
        exp_value = None
        try:
            exp_value = math.exp(-super(LogisticHypothesis, self).sum_of_products(values))
        except OverflowError:
            Log().warn('OverflowError for values: ' + str(values))
            return 1

        return 1 / (1 + exp_value)