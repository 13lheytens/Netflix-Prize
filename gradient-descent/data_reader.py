
class DataReader(object):
    def __init__(self, lines, test_proportion):
        inputs   = []
        outputs  = []
        rejected = []
        ok_count = 0
        n = None
        
        def is_comment(line):
            return line[0] == '#'

        for line in map(str.strip, lines):
            if is_comment(line):
                continue

            line_err = False
            parts = line.split(':')

            if len(parts) != 2:
                line_err = True
            else:
                try:
                    result_part, data_part = parts
                    data_parts = data_part.split(',')

                    if n is None:
                        n = len(data_parts)

                    output_value = float(result_part)
                    if n == len(data_parts) and self.check_output_value(output_value):
                        inputs.append(map(float, data_parts))
                        outputs.append(output_value)

                    else:
                        line_err = True    

                except ValueError:
                    line_err = True

            if line_err:
                rejected.append(line)
            else:
                ok_count += 1

        t = int(round(ok_count * (1 - test_proportion)))

        self.training_input_values  = inputs[:t]
        self.training_output_values = outputs[:t]
        self.testing_input_values  = inputs[t:]
        self.testing_output_values  = outputs[t:]

        self.accepted_count  = ok_count
        self.rejected_lines  = rejected
        self.input_var_count = n

class LinearRegressionDataReader(DataReader):
    def check_output_value(self, value):
        return True

class LogisticRegressionDataReader(DataReader):
    def check_output_value(self, value):
        return value in (0,1)