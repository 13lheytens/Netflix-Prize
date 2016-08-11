class Log:
    def __init__(self):
        self.indent_level = 0
        self.previous_output = ''

    def bar(self):
        self.__print('-' * 80, False)

    def info(self, txt):
        self.__print(txt, True)

    def warn(self, txt):
        self.__print('WARN:  ' + txt, False)

    def error(self, txt):
        self.__print('ERROR: ' + txt, False)

    def set_indent(self, level):
        self.indent_level = level

    def underline(self):
        print '-' * len(self.previous_output)

    def __print(self, value, respect_indent):
        indent = ''
        if respect_indent:
            indent = '    ' * self.indent_level

        output = indent + value
        print output
        self.previous_output = output