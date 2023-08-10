import modules as mod


def example_2_13():
    """
    Corresponds to figure 3 in the paper.
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0, 0), 0)
    c2 = mod.critical_val((7, 0), 0)
    c3 = mod.critical_val((0, 4), 0)
    c4 = mod.critical_val((7, 4), 0)
    c5 = mod.critical_val((0, 8), 0)
    c6 = mod.critical_val((7, 8), 0)
    c7 = mod.critical_val((0, 11), 0)
    c8 = mod.critical_val((7, 11), 0)

    d1 = mod.critical_val((0, 0), 1)
    d2 = mod.critical_val((7, 0), 1)
    d3 = mod.critical_val((0, 4), 1)
    d4 = mod.critical_val((7, 4), 1)
    d5 = mod.critical_val((0, 8), 1)
    d6 = mod.critical_val((7, 8), 1)
    d7 = mod.critical_val((0, 11), 1)
    d8 = mod.critical_val((7, 11), 1)

    CritPts = [c1, c2, c3, c4, c5, c7, d1, d2, d3, d4, d5, d7]
    return CritPts


def example_2_11():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0, 0), 0)
    c2 = mod.critical_val((7, 0), 0)
    c3 = mod.critical_val((0, 4), 0)
    c4 = mod.critical_val((7, 4), 0)
    c5 = mod.critical_val((0, 7), 0)
    c6 = mod.critical_val((7, 7), 0)
    c7 = mod.critical_val((0, 11), 0)
    c8 = mod.critical_val((7, 11), 0)

    d1 = mod.critical_val((0, 0), 1)
    d2 = mod.critical_val((7, 0), 1)
    d3 = mod.critical_val((0, 4), 1)
    d4 = mod.critical_val((7, 4), 1)
    d5 = mod.critical_val((0, 7), 1)
    d6 = mod.critical_val((7, 7), 1)
    d7 = mod.critical_val((0, 11), 1)
    d8 = mod.critical_val((7, 11), 1)

    CritPts = [c1, c2, c3, c4, c5, c7, d1, d2, d3, d4, d5, d7]

    return CritPts


def example_1():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0, 0), 0)
    c2 = mod.critical_val((7, 0), 0)
    c3 = mod.critical_val((0, 8), 0)
    c4 = mod.critical_val((7, 8), 0)

    d1 = mod.critical_val((1, 1), 1)
    d2 = mod.critical_val((8, 1), 1)
    d3 = mod.critical_val((1, 9), 1)
    d4 = mod.critical_val((8, 9), 1)

    CritPts = [c1, c2, c3, d1, d2, d3]
    return CritPts


def example_2():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0, 0), 0)
    c2 = mod.critical_val((4, 0), 0)
    c3 = mod.critical_val((0, 4), 0)
    c4 = mod.critical_val((4, 4), 0)

    d1 = mod.critical_val((1, 0), 1)
    d2 = mod.critical_val((3, 0), 1)
    d3 = mod.critical_val((1, 4), 1)
    d4 = mod.critical_val((3, 4), 1)

    CritPts = [c1, c2, c3, d1, d2, d3]
    return CritPts
