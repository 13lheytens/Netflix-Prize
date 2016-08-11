from __future__ import division

from log import Log

class GradientDescent:
    def __init__(self, initial_hypothesis, cost_function, normalised_variables, output_values):
        self.cost_function  = cost_function
        self.hypothesis     = initial_hypothesis
        self.variables      = normalised_variables
        self.output_values  = output_values
        self.iterations     = 0

        self.error_checking = False
        self.last_err = None
        self.set_iterations(1000)

        self.interrupted = False

    def calculate(self):
        for i in range(self.max_iterations):
            if self.interrupted:
                return
            predicted_values = []
            var_data = map(lambda v : v.data, self.variables)
            for data in zip(*var_data):
                predicted_values.append(self.hypothesis.calculate(data))

            self.error_check(predicted_values)
            self.update_hypothesis(predicted_values)
            self.show_progress(i, predicted_values)
            self.iterations += 1

    def update_hypothesis(self, predicted_values):
        deltas = self.cost_function.calculate_deltas(self.variables, predicted_values, self.hypothesis.theta_values)
        self.hypothesis.apply_deltas(deltas)

    def error_check(self, predicted_values):
        if self.error_checking:
            this_err = self.cost_function.cost(predicted_values)
            if self.last_err is None:
                self.last_err = this_err

            elif this_err > self.last_err:
                raise ValueError('Error increased, try reducing alpha')

            else:
                self.last_err = this_err

    def show_progress(self, count, predicted_values):
        if count % self.one_percent == 0:
            err = self.cost_function.cost(predicted_values)
            percentage = int(100 * count / self.max_iterations)
            percentage_txt = "{0:>4}".format(percentage)
            Log().info('{0:>4}% complete ... Error={1:.8f}'.format(percentage, err))

    def set_iterations(self, iterations):
        self.one_percent = int(iterations / 100)
        self.max_iterations = iterations

    def set_error_checking(self):
        self.error_checking = True

    def interrupt(self, _1, _2):
        self.interrupted = True
