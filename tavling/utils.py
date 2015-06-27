# Small utility functions for handling results and whatnot.
#
# Copyright 2015- Karl Mikaelsson <derfian@lysator.liu.se>

def add_results(h, a):
    if h is None or a is None:
        # Incomplete + anything = incomplete
        return None
    elif h[2] or a[2]:
        # Disqualified + anything = disqualified
        return (None, None, True)
    else:
        # Add penalties, time, not disqualified.
        return (h[0] + a[0], h[1] + a[1], False)

def combine_results(res):
    complete = filter(lambda x: x is not None and not x[2], res)
    incomplete = filter(lambda x: x is None, res)
    disqualified = filter(lambda x: x is not None and x[2], complete)

    # There needs to be at least three complete or incomplete results
    # for the team to avoid instant disqualification.
    if len(complete) + len(incomplete) - len(disqualified) < 3:
        return (None, None, True)


    if len(incomplete) + len(res) < 3:
        # Not enough results!
        return None

    sres = sorted(res, key=sortfunc_tuple)

    if len(sres) < 3:
        return (None, None, True)

    acc = (0, 0, False)
    # top 3 results
    for n in range(3):
        acc = add_results(acc, sres[n])
    return acc

def result_to_beat(leader, challenger):
    lr = leader.aggregate()
    cjr = challenger.hoppresultat()
    car = challenger.agilityresultat()
    cr = challenger.aggregate()


    # We need leader to have a complete result, and challenger to have
    # an incomplete result.

    # Leader needs to have a complete result for us to compare to it.
    if lr is None:
        return None

    # Challenger needs to have an incomplete result.
    if cr is not None:
        return None
    # If leader is disqualified, any result will do.
    if lr[2]:
        return (None, None, True)

    r = None
    if cjr and not cjr[2]:
        r = cjr
    elif car and not car[2]:
        r = car
    else:
        # incomplete + disqualified or something
        return None

    rt = (lr[0]-r[0], lr[1]-r[1], False)

    if rt[0] < 0:
        return None
    return rt

def sortfunc_tuple(x):
    # Valid results are sorted first
    if x is not None:
        return (0, x[2], x[0], x[1])
    # Disqualified, second to last
    elif x and x[2]:
        return (1, True, None, None)
    # Invalid results are sorted last.
    elif x is None:
        return (2, None, None, None)

def sortfunc_object(x):
    a = x.aggregate()
    return sortfunc_tuple(a)
