class Denormaliser:
    def denormalise(self, theta_values, variables):
        new_theta_values = []
        theta0_delta = 0

        for v, t in zip(variables, theta_values):
            if v.scale == 0:
                new_theta_values.append(t)
            else:
                theta0_delta -= t * v.mean_offset / v.scale
                new_theta_values.append(t / v.scale)

        new_theta_values[0] += theta0_delta

        return new_theta_values