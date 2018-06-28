class PostfixExpression(object):
    _expression = []

    def __init__(self, _expr: list):
        self._expression = _expr

    def __str__(self):
        return ','.join(self._expression)


class Converter(object):
    _input = ""

    def __init__(self, formula: str):
        self._input = formula

    def convert(self) -> PostfixExpression:
        return PostfixExpression([])


def convert_to_postfix(formula: str) -> PostfixExpression:
    converter = Converter(formula)
    return converter.convert()
