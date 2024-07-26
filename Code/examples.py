import modules as mod
# from scipy.stats import qmc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import random as rnd
import modules as mod



#################### EXAMPLES CURRENTLY WORKING

def small_socg_ex_M_N():
    # usage as of 26 July 2024:
    # example = ex.small_socg_ex_M_N()
    
    # these are the points we'll graph
    # bottom left
    a1 = ((0.0, 0.0), 0)
    # bottom right
    a2 = ((6.0, 0.0), 0)
    # top left
    a3 = ((0.0, 6.0), 0)

    b1 = ((4.0, 2.0), 1)
    b2 = ((4.0, 4.0), 1)
    b3 = ((8.0, 2.0), 1)

    b4 = ((1.0, 5.0), 1)
    b5 = ((1.0, 10.0), 1)
    b6 = ((2.0, 5.0), 1)
    ############## make them into crit vals 
    c1 = mod.critical_val(a1[0], 0)
    c2 = mod.critical_val(a2[0], 0)
    c3 = mod.critical_val(a3[0], 0)

    d1 = mod.critical_val(b1[0], 1)
    d2 = mod.critical_val(b2[0], 1)
    d3 = mod.critical_val(b3[0], 1)

    d4 = mod.critical_val(b4[0], 1)
    d5 = mod.critical_val(b5[0], 1)
    d6 = mod.critical_val(b6[0], 1)
    #bl, br, tl, tr
    crits_no_lub = [a1, a2, a3, b1, b2, b3, b4, b5, b6]
    critpts = [c1, c2, c3, d1, d2, d3, d4, d5, d6]


   #(self, top_left,top_right, bottom_left, bottom_right, dim = 1, parent = 1):

    m1 = mod.Rectangle(a3[0], (6.0, 6.0), a1[0], a2[0], 1, 0)
    n1 = mod.Rectangle(b2[0], (8.0, 4.0), b1[0], b3[0], 1, 1)   
    n2 = mod.Rectangle(b5[0], (2.0, 10.0), b4[0], b6[0], 1, 1)

    M = mod.RectangleModule([m1])
    N = mod.RectangleModule([n2,n1])


    return critpts, crits_no_lub, M, N

################# BELOW ARE OLD EXAMPLES NEEDING UPDATES


def example_2_12():
    #module M
    c1 = mod.critical_val((2.0,2.0),0)
    c2 = mod.critical_val((2.0,7.0),0)

    #module N
    d1 = mod.critical_val((2.0,2.0),1)
    d2 = mod.critical_val((2.0,10.0),1)
    CritPts = [c1, c2, d1, d2]
    
    return CritPts



def example_2_13():
    """
    Corresponds to figure 3 in the paper.
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((7.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 4.0), 0)
    c4 = mod.critical_val((7.0, 4.0), 0)
    c5 = mod.critical_val((0.0, 8.0), 0)
    c6 = mod.critical_val((7.0, 8.0), 0)
    c7 = mod.critical_val((0.0, 11.0), 0)
    c8 = mod.critical_val((7.0, 11.0), 0)

    d1 = mod.critical_val((0.0, 0.0), 1)
    d2 = mod.critical_val((7.0, 0.0), 1)
    d3 = mod.critical_val((0.0, 4.0), 1)
    d4 = mod.critical_val((7.0, 4.0), 1)
    d5 = mod.critical_val((0.0, 8.0), 1)
    d6 = mod.critical_val((7.0, 8.0), 1)
    d7 = mod.critical_val((0.0, 11.0), 1)
    d8 = mod.critical_val((7.0, 11.0), 1)

    CritPts = [c1, c2, c3, c4, c5, c7, d1, d2, d3, d4, d5, d7]
    return CritPts


def small_socg_ex():
    # note: this doesn't work in the new code version. 
    # saving for archival reasons.
    a1 = ((0.0, 0.0), 0)
    a2 = ((6.0, 0.0), 0)
    a3 = ((0.0, 6.0), 0)

    b1 = ((4.0, 2.0), 1)
    b2 = ((4.0, 4.0), 1)
    b3 = ((8.0, 2.0), 1)

    b4 = ((1.0, 5.0), 1)
    b5 = ((1.0, 10.0), 1)
    b6 = ((2.0, 5.0), 1)
    ############## make them into crit vals
    c1 = mod.critical_val(a1[0], 0)
    c2 = mod.critical_val(a2[0], 0)
    c3 = mod.critical_val(a3[0], 0)

    d1 = mod.critical_val(b1[0], 1)
    d2 = mod.critical_val(b2[0], 1)
    d3 = mod.critical_val(b3[0], 1)

    d4 = mod.critical_val(b4[0], 1)
    d5 = mod.critical_val(b5[0], 1)
    d6 = mod.critical_val(b6[0], 1)
    crits_no_lub = [a1, a2, a3, b1, b2, b3, b4, b5, b6]
    critpts = [c1, c2, c3, d1, d2, d3, d4, d5, d6]
    return critpts, crits_no_lub

def small_rectangle_example():
    a1 = ((0.0, 0.0), 0)
    a2 = ((6.0, 0.0), 0)
    a3 = ((0.0, 6.0), 0)

    b1 = ((4.0, 2.0), 1)
    b2 = ((4.0, 4.0), 1)
    b3 = ((8.0, 2.0), 1)

    
    ############## make them into crit vals 
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((6.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 6.0), 0)

    d1 = mod.critical_val((4.0, 2.0), 1)
    d2 = mod.critical_val((4.0, 4.0), 1)
    d3 = mod.critical_val((8.0, 2.0), 1)

    crits_no_lub = [a1, a2, a3, b1, b2, b3]
    critpts = [c1, c2, c3, d1, d2, d3]


   #(self, top_left,top_right, bottom_left, 
    # bottom_right, dim = 1, parent = 1):

    m1 = mod.Rectangle(a3[0], (6.0, 6.0), a1[0], a2[0], 1, 0)
    n1 = mod.Rectangle(b2[0], (8.0, 4.0), b1[0], b3[0], 1, 1)   


    M = mod.RectangleModule([m1])
    N = mod.RectangleModule([n1])


    return critpts, crits_no_lub, M, N


def small_rectangle_example_cleaner_maybe():
    # input
    tl_m = (0.0, 6.0)
    tr_m = (6.0, 6.0)
    bl_m = (0.0, 0.0)
    br_m = (6.0, 0.0)

    tl_n = (4.0, 4.0)
    tr_n = (8.0, 4.0)
    bl_n = (4.0, 2.0)
    br_n = (8.0, 2.0)

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


def example_2_11():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((7.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 4.0), 0)
    c4 = mod.critical_val((7.0, 4.0), 0)
    c5 = mod.critical_val((0.0, 7.0), 0)
    c6 = mod.critical_val((7.0, 7.0), 0)
    c7 = mod.critical_val((0.0, 11.0), 0)
    c8 = mod.critical_val((7.0, 11.0), 0)

    d1 = mod.critical_val((0.0, 0.0), 1)
    d2 = mod.critical_val((7.0, 0.0), 1)
    d3 = mod.critical_val((0.0, 4.0), 1)
    d4 = mod.critical_val((7.0, 4.0), 1)
    d5 = mod.critical_val((0.0, 7.0), 1)
    d6 = mod.critical_val((7.0, 7.0), 1)
    d7 = mod.critical_val((0.0, 11.0), 1)
    d8 = mod.critical_val((7.0, 11.0), 1)

    CritPts = [c1, c2, c3, c4, c5, c7, d1, d2, d3, d4, d5, d7]

    return CritPts


def example_1():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((7.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 8.0), 0)
    c4 = mod.critical_val((7.0, 8.0), 0)

    d1 = mod.critical_val((1.0, 1.0), 1)
    d2 = mod.critical_val((8.0, 1.0), 1)
    d3 = mod.critical_val((1.0, 9.0), 1)
    d4 = mod.critical_val((8.0, 9.0), 1)

    CritPts = [c1, c2, c3, d1, d2, d3]

    #(self, top_left,top_right, bottom_left, bottom_right, dim = 1, parent = 1):
    m1= mod.Rectangle(c3.coords, c4.coords, c1.coords, c2.coords, 1, 0)

    n1 = mod.Rectangle(d3.coords, d4.coords, d1.coords, d2.coords, 1, 1)

    M = mod.RectangleModule([m1])
    N = mod.RectangleModule([n1])

    return CritPts, M, N


def example_2():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((4.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 4.0), 0)
    c4 = mod.critical_val((4.0, 4.0), 0)

    d1 = mod.critical_val((1.0, 0.0), 1)
    d2 = mod.critical_val((3.0, 0.0), 1)
    d3 = mod.critical_val((1.0, 4.0), 1)
    d4 = mod.critical_val((3.0, 4.0), 1)

    CritPts = [c1, c2, c3, d1, d2, d3]
    return CritPts


def rectangle_example(numpts=4, display=False):
    # note: this goes in cw order, hopefully not an issue
    # parameters for rectangle shape and sampling density
    width = 8
    height = 4

    # calculate points on the boundary of the rectangle
    x1 = np.linspace(-width / 2, width / 2, num=numpts // 4 + 1)[:-1]
    y1 = np.full_like(x1, height / 2)

    x2 = np.full_like(y1, width / 2)
    y2 = np.linspace(height / 2, -height / 2, num=numpts // 4 + 1)[:-1]

    x3 = np.linspace(width / 2, -width / 2, num=numpts // 4 + 1)[:-1]
    y3 = np.full_like(x3, -height / 2)

    x4 = np.full_like(y3, -width / 2)
    y4 = np.linspace(-height / 2, height / 2, num=numpts // 4 + 1)[:-1]

    x = np.concatenate([x1, x2, x3, x4])
    y = np.concatenate([y1, y2, y3, y4])
    points = np.array(list(zip(x, y)))

    if display:
        # plot rectangle
        fig, ax1 = plt.subplots(figsize=(10, 4))
        ax1.set_xlim(-width / 2 - 1, width / 2 + 1)
        ax1.set_ylim(-height / 2 - 1, height / 2 + 1)
        ax1.set_aspect("equal")
        ax1.plot(x, y, "o", linewidth=2)
        plt.show()

    return points


def make_poisson(
    inputpts=rectangle_example(), llama=30, radius=0.000001, seed=0, display=False
):
    # inputpts should be column vec of x,y coords in 2D
    xMin = np.min(inputpts[:, 0])
    xMax = np.max(inputpts[:, 0])
    yMin = np.min(inputpts[:, 1])
    yMax = np.max(inputpts[:, 1])

    # rectangle dims
    xDelta = xMax - xMin
    yDelta = yMax - yMin
    areaTotal = xDelta * yDelta

    # note: llama/lambda is intensity (ie mean density)
    # of the Poisson pt process

    # this fixes a seed for reproducability (so it's not random)
    seed = 0
    g = np.random.default_rng(seed)
    numbPoints = g.poisson(llama * areaTotal)

    # Simulate a Poisson point process
    xx = xDelta * g.uniform(0, 1, numbPoints) + xMin
    yy = yDelta * g.uniform(0, 1, numbPoints) + yMin

    points = np.column_stack([xx.ravel(), yy.ravel()])
    # below is the tricksy blue noise thing
    scale = max(xDelta, yDelta)
    rng = g
    # radius = 1/(2*(math.sqrt(llama)))

    engine = qmc.PoissonDisk(d=2, radius=radius, seed=rng)
    # these are in [0,1]
    sample = engine.random(4 * llama)
    # print(radius, llama, sample.shape)
    scaledsample = sample * scale + np.array(
        [xMin + xDelta / 2 - scale / 2, yMin + yDelta / 2 - scale / 2]
    )
    # return points
    if display:
        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        ax.plot(scaledsample[:, 0], scaledsample[:, 1], "o", color="orange")
    return scaledsample


def make_rects(poisson_intensity, seed=0, dpi=150):
    radius = 1 / (2 * (math.sqrt(poisson_intensity)))
    poissonpts = make_poisson(
        inputpts=rectangle_example(),
        llama=poisson_intensity,
        radius=radius,
        seed=seed,
        display=False,
    )
    rectangle_lengths = []
    rectangle_widths = []

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    # np.random.seed(seed)
    rnd.seed(seed)
    critical_pts = []
    crits_no_lub = []
    for x in range(len(poissonpts)):
        width = float(rnd.randint(2, 10))
        length = float(rnd.randint(2, 10))
        rectangle_lengths.append(length)
        rectangle_widths.append(width)
        # we only need the first four points for math,
        # but we need to repeat the initial point at the
        # end for plotting
        outpt_xs = [
            poissonpts[x][0],
            poissonpts[x][0],
            poissonpts[x][0] + width,
            poissonpts[x][0] + width,
        ]
        outpt_ys = [
            poissonpts[x][1],
            poissonpts[x][1] + length,
            poissonpts[x][1] + length,
            poissonpts[x][1],
        ]
        # added the init pt at the end for plotting
        xs = [
            poissonpts[x][0],
            poissonpts[x][0],
            poissonpts[x][0] + width,
            poissonpts[x][0] + width,
            poissonpts[x][0],
        ]
        ys = [
            poissonpts[x][1],
            poissonpts[x][1] + length,
            poissonpts[x][1] + length,
            poissonpts[x][1],
            poissonpts[x][1],
        ]

        color = rnd.randint(0, 1)
        if color == 0:
            ax.plot(xs, ys, "--", color="black")
            for x in xs:
                for y in ys:
                    ax.plot(x, y, "o", color="black", markersize=5)
        else:
            ax.plot(xs, ys, "--", color="orange")
            for x in xs:
                for y in ys:
                    ax.plot(x, y, "o", color="orange", markersize=5)
        for i in range(len(outpt_xs)):
            critpt = mod.critical_val((outpt_xs[i], outpt_ys[i]), color)
            critical_pts.append(critpt)
            c_no_lub = ((outpt_xs[i], outpt_ys[i]), color)
            crits_no_lub.append(c_no_lub)

    black_patch = mpatches.Patch(color="black", label="M")
    orange_patch = mpatches.Patch(color="orange", label="N")
    ax.legend(
        handles=[black_patch, orange_patch],
        loc="upper right",
    )
    fig.dpi = dpi
    return critical_pts, crits_no_lub


def critvals_poisson(poisson_intensity, seed):
    radius = 1 / (2 * (math.sqrt(poisson_intensity)))
    poissonpts = make_poisson(
        llama=poisson_intensity, radius=radius, seed=seed, display=False
    )

    # turn poiss points into critvals
    critvals = []
    no_lub = []
    for p in poissonpts:
        r = rnd.randint(0, 1)
        c = mod.critical_val((p[0], p[1]), r)
        no_lub.append(((p[0], p[1]), r))
        critvals.append(c)

    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    for c in critvals:
        if c.parent_module == 0:
            ax.plot(c.coords[0], c.coords[1], "o", color="red")
        else:
            ax.plot(c.coords[0], c.coords[1], "o", color="blue")
    return critvals, no_lub


def bunny_into_critvals(bunnypoints, seed):
    rnd.seed(seed)
    critvals = []
    for row in bunnypoints:
        c = mod.critical_val((row[0], row[1]), rnd.randint(0, 1))
        critvals.append(c)

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    for c in critvals:
        if c.parent_module == 0:
            ax.plot(c.coords[0], c.coords[1], "o", color="red")
        else:
            ax.plot(c.coords[0], c.coords[1], "o", color="blue")
    return critvals


def test_example():
    """
    an input crit val c_i needs x,y coords and a parent rectangle module.
    """
    c1 = mod.critical_val((0.0, 0.0), 0)
    c2 = mod.critical_val((7.0, 0.0), 0)
    c3 = mod.critical_val((0.0, 4.0), 0)

    d1 = mod.critical_val((3.0, 2.0), 1)
    d2 = mod.critical_val((3.0, 6.0), 1)
    d3 = mod.critical_val((10.0, 2.0), 1)

    CritPts = [c1, c2, c3, d1, d2, d3]

    return CritPts


def make_rects_balanced(poisson_intensity, seed=0, exact_num=2):
    radius = 1 / (2 * (math.sqrt(poisson_intensity)))
    poissonpts = make_poisson(
        inputpts=rectangle_example(),
        llama=poisson_intensity,
        radius=radius,
        seed=seed,
        display=False,
    )

    while len(poissonpts) < 2 * exact_num:
        print("not enought points try again")
        poisson_intensity = poisson_intensity + 1
        radius = 1 / (2 * (math.sqrt(poisson_intensity)))
        poissonpts = make_poisson(
            inputpts=rectangle_example(),
            llama=poisson_intensity,
            radius=radius,
            seed=seed,
            display=False,
        )

    if len(poissonpts) > 2 * exact_num:
        poissonpts = poissonpts[: 2 * exact_num]

    rectangle_lengths = []
    rectangle_widths = []
    colors = []
    for i in range(exact_num):
        color = 0
        colors.append(color)
    for i in range(exact_num, exact_num * 2):
        color = 1
        colors.append(color)

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    # np.random.seed(seed)
    rnd.seed(seed)
    critical_pts = []
    for x in range(len(poissonpts)):
        width = float(rnd.randint(2, 10))
        length = float(rnd.randint(2, 10))
        rectangle_lengths.append(length)
        rectangle_widths.append(width)
        # we only need the first four points for math,
        # but we need to repeat the initial point at the
        # end for plotting
        outpt_xs = [
            poissonpts[x][0],
            poissonpts[x][0],
            poissonpts[x][0] + width,
        ]
        outpt_ys = [
            poissonpts[x][1],
            poissonpts[x][1] + length,
            poissonpts[x][1],
        ]
        # added the init pt at the end for plotting
        xs = [
            poissonpts[x][0],
            poissonpts[x][0],
            poissonpts[x][0] + width,
            poissonpts[x][0] + width,
            poissonpts[x][0],
        ]
        ys = [
            poissonpts[x][1],
            poissonpts[x][1] + length,
            poissonpts[x][1] + length,
            poissonpts[x][1],
            poissonpts[x][1],
        ]
        color = colors[x]

        if color == 0:
            ax.plot(xs, ys, "--", color="red")
            for x in xs:
                for y in ys:
                    ax.plot(x, y, "o", color="red", markersize=5)
        else:
            ax.plot(xs, ys, "--", color="blue")
            for x in xs:
                for y in ys:
                    ax.plot(x, y, "o", color="blue", markersize=5)
        for i in range(len(outpt_xs)):
            critpt = mod.critical_val((outpt_xs[i], outpt_ys[i]), color)
            critical_pts.append(critpt)

    return critical_pts
