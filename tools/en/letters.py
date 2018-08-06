def count_letters(expr):
    return sum([len(x) for x in expr.replace('-','').split(' ')])
