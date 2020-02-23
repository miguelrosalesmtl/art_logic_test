

class AMaximumValueError(Exception):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return str(self.message)
