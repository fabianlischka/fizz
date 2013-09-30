def pairwiseRound(iterable):
    """for 'abcd' returns (a,b), (b,c), (c,d), (d,a)"""
    a, b = it.tee(iterable)
    first = next(b, None)
    return zip(a, it.chain(b,[first]))