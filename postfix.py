class PostfixExpression(object):
    _expression = []

    def __init__(self, _expr: list):
        self._expression = _expr

    def eval(self) -> float:
        stack = []
        for item in self._expression:
            if isinstance(item, TokenVar):
                stack.append(item.value)
                continue
            if isinstance(item, TokenOperatorNegative):
                stack[-1] = -stack[-1]
                continue
            if isinstance(item, TokenOperatorPositive):
                continue
            if isinstance(item, (TokenOperatorPlus, TokenOperatorMinus, TokenOperatorMultiply, TokenOperatorDivide)):
                b = stack.pop()
                a = stack.pop()
                if isinstance(item, TokenOperatorPlus):
                    stack.append(a + b)
                    continue
                if isinstance(item, TokenOperatorMinus):
                    stack.append(a - b)
                    continue
                if isinstance(item, TokenOperatorMultiply):
                    stack.append(a * b)
                    continue
                if isinstance(item, TokenOperatorDivide):
                    stack.append(a / b)
                    continue

        return stack[-1]

    def __str__(self):
        return ','.join(map(str, self._expression))


class Token(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.value))


class TokenVar(Token):
    def __init__(self, value: str):
        value = float(value)
        super(TokenVar, self).__init__(value)


class TokenParenthOpen(Token):
    pass


class TokenParenthClose(Token):
    pass


class TokenOperator(Token):
    binary = True
    priority = 1


class TokenOperatorPlus(TokenOperator):
    priority = 2


class TokenOperatorMinus(TokenOperator):
    priority = 2


class TokenOperatorMultiply(TokenOperator):
    priority = 3


class TokenOperatorDivide(TokenOperator):
    priority = 3


class TokenOperatorNegative(TokenOperator):
    binary = False
    priority = 10

    def __str__(self):
        return '(%s)' % str(self.value)


class TokenOperatorPositive(TokenOperator):
    binary = False
    priority = 10

    def __str__(self):
        return '(%s)' % str(self.value)


class Converter(object):
    OPERATORS = {
        '+': TokenOperatorPlus,
        '-': TokenOperatorMinus,
        '*': TokenOperatorMultiply,
        '/': TokenOperatorDivide,
    }
    SPACES = {' ', "\n", "\t"}
    PARENTHESIS = {
        '(': TokenParenthOpen,
        ')': TokenParenthClose,
    }

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

            if ch in self.OPERATORS or ch in self.PARENTHESIS:
                if token_value:
                    token = TokenVar(token_value)
                    break
                else:
                    token_value = self._input[pos]
                    if ch in self.OPERATORS:
                        op_class = self.OPERATORS[ch]
                    else:
                        op_class = self.PARENTHESIS[ch]
                    token = op_class(token_value)
                    pos += 1
                    break

            if ch.isdigit() or ch == '.':
                token_value += ch
            else:
                raise ValueError('Unknown symbol {0}'.format(ch))

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
        prev_token = None
        for token in self._tokens_iterator():
            while token:
                if isinstance(token, TokenVar):
                    result.append(token)
                    break

                if isinstance(token, TokenParenthOpen):
                    stack.append(token)
                    break

                if isinstance(token, TokenParenthClose):
                    while stack and not isinstance(stack[-1], TokenParenthOpen):
                        result.append(stack.pop())
                    if not stack or not isinstance(stack[-1], TokenParenthOpen):
                        raise ValueError('Closing parenthesis without opening')
                    stack.pop()
                    break

                if isinstance(token, TokenOperator):
                    if prev_token is None or isinstance(prev_token, TokenOperator):
                        if not isinstance(token, (TokenOperatorPositive, TokenOperatorNegative)):
                            if not isinstance(token, (TokenOperatorMinus, TokenOperatorPlus)):
                                raise ValueError('Got unknown unar operator {0}'.format(token))
                            if isinstance(token, TokenOperatorPlus):
                                token = TokenOperatorPositive(token.value)
                            else:
                                token = TokenOperatorNegative(token.value)
                            continue

                    if stack:
                        stack_top = stack[-1]
                        if isinstance(stack_top, TokenOperator):
                            if stack_top.priority >= token.priority:
                                result.append(stack.pop())
                                continue

                    stack.append(token)
                    break

            prev_token = token

        if stack:
            for i in range(len(stack) - 1, -1, -1):
                if not isinstance(stack[i], TokenOperator):
                    raise ValueError('Missing closing parenthesis')
                result.append(stack[i])

        return PostfixExpression(result)


def convert_to_postfix(formula: str) -> PostfixExpression:
    converter = Converter(formula)
    return converter.convert()
