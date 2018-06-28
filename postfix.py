class PostfixExpression(object):
    _expression = []

    def __init__(self, _expr: list):
        self._expression = _expr

    def __str__(self):
        return ','.join(map(str, self._expression))


class Token(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class TokenVar(Token):
    def __init__(self, value: str):
        value = float(value)
        super(TokenVar, self).__init__(value)

    def __str__(self):
        return str(self.value)


class TokenOperator(Token):
    binary = True
    priority = 1


class TokenOperatorPlus(TokenOperator):
    priority = 2


class TokenOperatorMinus(TokenOperator):
    priority = 2


class Converter(object):
    OPERATORS = {
        '+': TokenOperatorPlus,
        '-': TokenOperatorMinus,
    }
    SPACES = {' ', "\n", "\t"}

    def __init__(self, formula: str):
        self._input = formula
        self._parse_pos = 0

    def _next_token(self):
        pos = self._parse_pos
        token_value = ""
        token = None

        while pos < len(self._input):
            ch = self._input[pos]
            if ch in self.SPACES:
                pos += 1
                continue

            if ch in self.OPERATORS:
                if token_value:
                    token = TokenVar(token_value)
                    break
                else:
                    token_value = self._input[pos]
                    op_class = self.OPERATORS[ch]
                    token = op_class(token_value)
                    pos += 1
                    break

            if ch.isdigit() or ch == '.':
                token_value += ch

            pos += 1

        self._parse_pos = pos

        if token is None and token_value:
            token = TokenVar(token_value)

        return token

    def _tokens_iterator(self):
        token = self._next_token()
        while token:
            yield token
            token = self._next_token()

    def convert(self) -> PostfixExpression:
        stack = []
        result = []
        for token in self._tokens_iterator():
            while token:
                if isinstance(token, TokenVar):
                    result.append(token)
                    break

                if isinstance(token, TokenOperator):
                    if stack:
                        stack_top = stack[-1]
                        if isinstance(stack_top, TokenOperator):
                            if stack_top.priority >= token.priority:
                                result.append(stack.pop())
                                continue

                    stack.append(token)
                    break

        if stack:
            for i in range(len(stack) -1, -1, -1):
                result.append(stack[i])

        return PostfixExpression(result)


def convert_to_postfix(formula: str) -> PostfixExpression:
    converter = Converter(formula)
    return converter.convert()
