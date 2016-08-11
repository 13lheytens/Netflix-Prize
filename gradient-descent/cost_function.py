from __future__ import division

import math, sys

class CostFunction(object):
    def __init__(self, results, alpha, lambda_term):
        self.results     = results
        self.alpha       = alpha
        self.lambda_term = lambda_term
        self.m           = len(results)

    def cost(self, predicted_results):
        cost = 0

        for predicted, actual in zip(predicted_results, self.results):
            cost += self.cost_delta(predicted, actual, self.m)

        return cost / self.m

    def calculate_deltas(self, normalised_variables, predicted_results, thetas):
        deltas = []

        for i in range(len(thetas)):
            delta = 0
            for j in range(self.m):
                delta += (predicted_results[j] - self.results[j]) * normalised_variables[i].data[j]

            if i == 0:
                lambda_term = 0
            else:
                lambda_term = self.lambda_term

            deltas.append((delta - lambda_term * thetas[i]) * self.alpha / self.m)

        return deltas

class LinearCostFunction(CostFunction):
    def __init__(self, results, alpha, lambda_term):
        super(LinearCostFunction, self).__init__(results, alpha, lambda_term)

    def cost_delta(self, predicted, actual, m):
        diff = predicted - actual
        return diff * diff / (2 * m)

class LogisticCostFunction(CostFunction):
    def __init__(self, results, alpha, lambda_term):
        super(LogisticCostFunction, self).__init__(results, alpha, lambda_term)

    def cost_delta(self, predicted, actual, m):
        if actual == 1:
            val = predicted
        else:
            val = 1 - predicted

        if val == 0:
            return -sys.maxint - 1
        return -math.log(val)