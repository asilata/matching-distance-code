import modules as mod
from scipy.stats import qmc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import random as rnd
import modules as mod

def make_1dim_MN_example(tl_m, tr_m, bl_m, br_m, tl_n, tr_n, bl_n, br_n):

    #######################
    a1 = (bl_m, 0)
    a2 = (br_m, 0)
    a3 = (tl_m, 0)

    b1 = (bl_n, 1)
    b2 = (tl_n, 1)
    b3 = (br_n, 1)

    ############## make them into crit vals 
    c1 = mod.critical_val(bl_m, 0)
    c2 = mod.critical_val(br_m, 0)
    c3 = mod.critical_val(tl_m, 0)

    d1 = mod.critical_val(bl_n, 1)
    d2 = mod.critical_val(tl_n, 1)
    d3 = mod.critical_val(br_n, 1)

    crits_no_lub = [a1, a2, a3, b1, b2, b3]
    critpts = [c1, c2, c3, d1, d2, d3]

   #(self, top_left,top_right, bottom_left, 
    # bottom_right, dim = 1, parent = 1):

    m1 = mod.Rectangle(tl_m, tr_m, bl_m, br_m, 1, 0)
    n1 = mod.Rectangle(tl_n, tr_n, bl_n, br_n, 1, 1)   

    M = mod.RectangleModule([m1])
    N = mod.RectangleModule([n1])

    return critpts, crits_no_lub, M, N