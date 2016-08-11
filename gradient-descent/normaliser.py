class NormalisedVariable:
    def __init__(self, variable, normalised_data, mean_offset, scale):
        self.variable    = variable
        self.data        = normalised_data
        self.mean_offset = mean_offset
        self.scale       = scale


class Normaliser:
    def normalise(self, variable):
        data = variable.data

        data_mean  = sum(data) / len(data)
        data_range = max(data) - min(data)

        if data_range != 0:
            normalised_data = map(lambda v : (v - data_mean) / data_range, data)
        else:
            normalised_data = data

        return NormalisedVariable(variable, normalised_data, data_mean, data_range)
