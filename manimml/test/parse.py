def parse_kwargs(expr: str, data: dict = {}) -> tuple:
    """
    Examples:
        "5" -> [5], {}
        "1, 2, num=3" -> [1, 2], {'num': 3}
    """
    if not isinstance(expr, str):
        return [], {}
    # return eval('[' + expr + ']', None, self.data), {}

    comma_indices = []
    index = len(expr)
    depth = 0
    arr = ''
    dic = ''
    is_literal = False # TODO: case when delimiters contained in string literal

    # break string into arr (args part) and dict (kw part)
    for i, c in enumerate(expr):
        if c in '([{' and not is_literal:
            depth += 1
        elif c in ')]}' and not is_literal:
            depth -= 1
        elif c == ',' and depth == 0:
            comma_indices.append(i)
        elif c == '=' and depth == 0 and i > 0 and expr[i-1] not in '!><=+-*/%^':
            index = comma_indices[-1] if len(comma_indices) else -1
            break
    if index == -1:
        arr, dic = '', expr
    else:
        arr, dic = expr[:index], expr[index+1:]

    # parse dict
    dic_buf = []
    i = 0
    while i < len(dic):
        c = dic[i]
        if c in '([{' and not is_literal:
            depth += 1
            dic_buf.append(c)
        elif c in ')]}' and not is_literal:
            depth -= 1
            dic_buf.append(c)
        elif c == ',' and depth == 0:
            comma_indices.append(i)
            dic_buf.append(c)
        elif c == '=' and depth == 0 and expr[i-1] not in '!><=+-*/%^':
            dic_buf[-1] = '"' + dic_buf[-1] + '"'
            dic_buf.append(':')
        elif c.isalpha() or c == '_':
            buf = [c]
            for d in dic[i+1:]:
                if d.isalnum() or d == '_':
                    buf.append(d)
                else:
                    break
            identifier = ''.join(buf)
            dic_buf.append(identifier)
            i += len(identifier) - 1
        else:
            dic_buf.append(c)
        i += 1

    dic = ''.join(dic_buf)
    return eval('[' + arr + '], {' + dic + '}', None, data)

if __name__ == '__main__':
    # print(parse_kwargs('1, 2, num=3, test=a', {'a': 114514}))
    # print(parse_kwargs('geometry["sphere"], material["sun"]', {
    #     'geometry': { 'sphere': 1111 },
    #     'material': { 'sun': 2222 },
    # }))
    # print(parse_kwargs('font_size=24'))
    print(parse_kwargs(''))
